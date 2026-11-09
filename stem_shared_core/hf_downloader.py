# -*- coding: utf-8 -*-
"""
stem_shared_core.hf_downloader - Tải mô hình GGUF từ Hugging Face bằng một cú nhấp.

Chỉ dùng thư viện chuẩn (urllib, threading, tkinter).

    from stem_shared_core.hf_downloader import ask_download_model
    path = ask_download_model(parent=root)   # Path tới file .gguf, hoặc None nếu bỏ qua/lỗi

Tính năng: luồng nền, tạm dừng/tiếp tục (HTTP Range), tự thử lại khi rớt mạng,
kiểm tra dung lượng ổ đĩa, xác minh kích thước + magic "GGUF" + SHA-256 (nếu lấy được từ HF).
"""
from __future__ import annotations

import errno
import hashlib
import http.client
import json
import os
import queue
import re
import shutil
import socket
import threading
import time
import urllib.error
import urllib.request
from collections import deque
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

try:  # dùng i18n chung nếu có
    from .i18n import t as _i18n_t
except Exception:  # noqa: BLE001
    try:
        from stem_shared_core.i18n import t as _i18n_t
    except Exception:  # noqa: BLE001
        _i18n_t = None

__all__ = [
    "HFModelDownloader", "ModelDownloadDialog", "DownloadState", "DownloadError",
    "ProgressInfo", "ask_download_model", "get_models_dir",
]

# Kiểm tra lại repo/tên tệp trên huggingface.co nếu muốn dùng nguồn khác.
DEFAULT_REPO = "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"
DEFAULT_FILENAME = "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"
APPROX_SIZE = int(1.12 * 1024 ** 3)       # ~1.1 GB, dùng khi chưa biết kích thước thật
DISK_MARGIN = 200 * 1024 ** 2             # chừa thêm 200 MB
CHUNK = 256 * 1024
MB = 1024 * 1024


def _get_ssl_context():
    """Tạo SSLContext kế thừa chứng chỉ hệ thống Windows và bổ sung CA bundle certifi."""
    import ssl
    ctx = ssl.create_default_context()
    try:
        import certifi
        ca = certifi.where()
        if os.path.isfile(ca):
            ctx.load_verify_locations(cafile=ca)
    except Exception:
        pass
    return ctx


def get_models_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    root = Path(base) if base else Path.home() / ".local" / "share"
    return root / "AIMathHub" / "models"


class DownloadState(str, Enum):
    IDLE = "idle"
    CONNECTING = "connecting"
    DOWNLOADING = "downloading"
    RETRYING = "retrying"
    PAUSED = "paused"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


class DownloadError(Exception):
    """code: network | disk_full | integrity | http | permission | unknown"""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


class _Transient(Exception):
    """Lỗi tạm thời (mạng) -> được phép thử lại."""


@dataclass
class ProgressInfo:
    state: DownloadState = DownloadState.IDLE
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed_bps: float = 0.0
    eta_seconds: Optional[float] = None

    @property
    def percent(self) -> float:
        return (self.downloaded_bytes / self.total_bytes * 100.0) if self.total_bytes else 0.0

    @property
    def downloaded_mb(self) -> float:
        return self.downloaded_bytes / MB

    @property
    def total_mb(self) -> float:
        return self.total_bytes / MB

    @property
    def speed_mbps(self) -> float:
        return self.speed_bps / MB


# =============================================================== Downloader
class HFModelDownloader:
    def __init__(
        self,
        repo_id: str = DEFAULT_REPO,
        filename: str = DEFAULT_FILENAME,
        dest_dir: Optional[os.PathLike] = None,
        on_progress: Optional[Callable[[ProgressInfo], None]] = None,
        on_state: Optional[Callable[[DownloadState, str], None]] = None,
        expected_sha256: Optional[str] = None,
        token: Optional[str] = None,
        max_retries: int = 5,
        timeout: float = 30.0,
    ) -> None:
        self.repo_id = repo_id
        self.filename = filename
        self.dest_dir = Path(dest_dir) if dest_dir else get_models_dir()
        self.on_progress = on_progress
        self.on_state = on_state
        self.expected_sha256 = expected_sha256.lower() if expected_sha256 else None
        self.token = token or os.environ.get("HF_TOKEN")
        self.max_retries = max_retries
        self.timeout = timeout

        self.url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
        self.state = DownloadState.IDLE
        self.last_error: Optional[DownloadError] = None

        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._cancel = False
        self._lock = threading.Lock()
        self._total = 0
        self._downloaded = 0
        self._samples: deque = deque()
        self._last_emit = 0.0

    # ------------------------------------------------------------ paths
    @property
    def final_path(self) -> Path:
        return self.dest_dir / self.filename

    @property
    def part_path(self) -> Path:
        return self.dest_dir / (self.filename + ".part")

    def is_downloaded(self) -> bool:
        """File cuối chỉ được tạo (os.replace) sau khi đã xác minh nên tồn tại = hợp lệ."""
        try:
            return self.final_path.is_file() and self.final_path.stat().st_size > 0 and not self.part_path.exists()
        except OSError:
            return False

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    # ---------------------------------------------------------- control
    def start(self) -> None:
        """Bắt đầu, hoặc tiếp tục từ file .part nếu có."""
        with self._lock:
            if self.is_running:
                return
            self._stop.clear()
            self._cancel = False
            self.last_error = None
            self._thread = threading.Thread(target=self._run, name="HFModelDownloader", daemon=True)
            self._thread.start()

    resume = start

    def pause(self) -> None:
        self._stop.set()

    def cancel(self, delete_partial: bool = True) -> None:
        self._cancel = delete_partial
        self._stop.set()

    def join(self, timeout: Optional[float] = None) -> None:
        if self._thread:
            self._thread.join(timeout)

    # --------------------------------------------------------- emitters
    def _set_state(self, state: DownloadState, message: str = "") -> None:
        self.state = state
        if self.on_state:
            try:
                self.on_state(state, message)
            except Exception:  # noqa: BLE001
                pass

    def _snapshot(self) -> ProgressInfo:
        speed = 0.0
        if len(self._samples) >= 2:
            (t0, b0), (t1, b1) = self._samples[0], self._samples[-1]
            if t1 > t0:
                speed = (b1 - b0) / (t1 - t0)
        eta = None
        if speed > 1 and self._total:
            eta = max(0.0, (self._total - self._downloaded) / speed)
        return ProgressInfo(self.state, self._downloaded, self._total, speed, eta)

    def _emit_progress(self, force: bool = False) -> None:
        now = time.monotonic()
        self._samples.append((now, self._downloaded))
        while self._samples and now - self._samples[0][0] > 3.0:
            self._samples.popleft()
        if not force and now - self._last_emit < 0.2:
            return
        self._last_emit = now
        if self.on_progress:
            try:
                self.on_progress(self._snapshot())
            except Exception:  # noqa: BLE001
                pass

    # ------------------------------------------------------------ worker
    def _run(self) -> None:
        try:
            self._set_state(DownloadState.CONNECTING)
            try:
                self.dest_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise self._map_os_error(exc) from exc

            if self.is_downloaded():
                size = self.final_path.stat().st_size
                self._downloaded = self._total = size
                self._emit_progress(force=True)
                self._set_state(DownloadState.COMPLETED)
                return

            self._downloaded = self.part_path.stat().st_size if self.part_path.exists() else 0
            if not self._total:
                self._fetch_meta()

            attempts = 0
            while True:
                before = self._downloaded
                try:
                    self._stream_once()
                    break
                except _Transient as exc:
                    if self._stop.is_set():
                        break
                    if self._downloaded > before:
                        attempts = 0
                    attempts += 1
                    if attempts > self.max_retries:
                        raise DownloadError("network", str(exc)) from exc
                    self._set_state(DownloadState.RETRYING, f"{attempts}/{self.max_retries}")
                    deadline = time.monotonic() + min(2 ** attempts, 30)
                    while time.monotonic() < deadline and not self._stop.is_set():
                        time.sleep(0.2)
                    if self._stop.is_set():
                        break

            if self._stop.is_set():
                if self._cancel:
                    self.part_path.unlink(missing_ok=True)
                    self._set_state(DownloadState.CANCELLED)
                else:
                    self._set_state(DownloadState.PAUSED)
                return

            self._verify()
            try:
                os.replace(self.part_path, self.final_path)
            except OSError as exc:
                raise self._map_os_error(exc) from exc
            self._emit_progress(force=True)
            self._set_state(DownloadState.COMPLETED)

        except DownloadError as exc:
            self.last_error = exc
            self._set_state(DownloadState.ERROR, exc.detail)
        except Exception as exc:  # noqa: BLE001
            self.last_error = DownloadError("unknown", f"{type(exc).__name__}: {exc}")
            self._set_state(DownloadState.ERROR, str(exc))

    # --------------------------------------------------------- metadata
    def _headers(self) -> dict:
        h = {"User-Agent": "AIMathHub/1.0"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _fetch_meta(self) -> None:
        """Lấy kích thước + SHA-256 từ API của HF. Thất bại thì bỏ qua (không chặn tải)."""
        api = f"https://huggingface.co/api/models/{self.repo_id}/tree/main"
        try:
            req = urllib.request.Request(api, headers=self._headers())
            with urllib.request.urlopen(req, timeout=15, context=_get_ssl_context()) as resp:
                items = json.load(resp)
            for item in items:
                if item.get("path") == self.filename:
                    lfs = item.get("lfs") or {}
                    self._total = int(lfs.get("size") or item.get("size") or 0)
                    if not self.expected_sha256 and lfs.get("oid"):
                        self.expected_sha256 = str(lfs["oid"]).lower()
                    break
        except Exception:  # noqa: BLE001
            pass

    # ----------------------------------------------------------- stream
    def _stream_once(self) -> None:
        existing = self.part_path.stat().st_size if self.part_path.exists() else 0
        if self._total and existing > self._total:
            self.part_path.unlink()
            existing = 0
        if self._total and existing == self._total:
            self._downloaded = existing
            return

        headers = self._headers()
        if existing:
            headers["Range"] = f"bytes={existing}-"
        req = urllib.request.Request(self.url, headers=headers)

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout, context=_get_ssl_context())
        except urllib.error.HTTPError as exc:
            if exc.code == 416:  # Range sai -> làm lại từ đầu
                self.part_path.unlink(missing_ok=True)
                self._downloaded = 0
                raise _Transient("range reset") from exc
            if exc.code in (401, 403):
                raise DownloadError("http", f"HTTP {exc.code} (cần quyền truy cập / token)") from exc
            if exc.code == 404:
                raise DownloadError("http", "HTTP 404 (không tìm thấy tệp trên Hugging Face)") from exc
            if exc.code == 429 or exc.code >= 500:
                raise _Transient(f"HTTP {exc.code}") from exc
            raise DownloadError("http", f"HTTP {exc.code}") from exc
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError,
                http.client.HTTPException, OSError) as exc:
            raise _Transient(str(getattr(exc, "reason", exc))) from exc

        with resp:
            status = getattr(resp, "status", None) or resp.getcode()
            if status == 206:
                m = re.match(r"bytes (\d+)-(\d+)/(\d+|\*)", resp.headers.get("Content-Range", ""))
                if m and m.group(3) != "*":
                    total = int(m.group(3))
                else:
                    total = existing + int(resp.headers.get("Content-Length") or 0)
                mode = "ab"
            else:  # server không hỗ trợ Range -> tải lại từ đầu
                existing = 0
                mode = "wb"
                cl = resp.headers.get("Content-Length")
                total = int(cl) if cl else self._total
            if total:
                self._total = total

            self._check_disk((self._total or APPROX_SIZE) - existing)
            self._downloaded = existing
            self._samples.clear()
            self._set_state(DownloadState.DOWNLOADING)

            try:
                fh = open(self.part_path, mode)
            except OSError as exc:
                raise self._map_os_error(exc) from exc
            with fh:
                while True:
                    if self._stop.is_set():
                        return
                    try:
                        chunk = resp.read(CHUNK)
                    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError,
                            http.client.HTTPException, OSError) as exc:
                        raise _Transient(str(getattr(exc, "reason", exc))) from exc
                    if not chunk:
                        break
                    try:
                        fh.write(chunk)
                    except OSError as exc:
                        raise self._map_os_error(exc) from exc
                    self._downloaded += len(chunk)
                    self._emit_progress()

        self._emit_progress(force=True)
        if self._total and self._downloaded < self._total:
            raise _Transient("kết nối bị ngắt giữa chừng")

    # ----------------------------------------------------------- checks
    def _check_disk(self, needed: int) -> None:
        try:
            free = shutil.disk_usage(self.dest_dir).free
        except OSError:
            return
        need = max(needed, 0) + DISK_MARGIN
        if free < need:
            raise DownloadError(
                "disk_full",
                f"cần thêm ~{need / 1024 ** 3:.2f} GB, ổ đĩa chỉ còn {free / 1024 ** 3:.2f} GB",
            )

    @staticmethod
    def _map_os_error(exc: OSError) -> DownloadError:
        if exc.errno == errno.ENOSPC or getattr(exc, "winerror", None) == 112:
            return DownloadError("disk_full", "ổ đĩa đã đầy trong lúc ghi tệp")
        if isinstance(exc, PermissionError) or exc.errno in (errno.EACCES, errno.EPERM):
            return DownloadError("permission", str(exc))
        return DownloadError("unknown", str(exc))

    def _verify(self) -> None:
        self._set_state(DownloadState.VERIFYING)
        size = self.part_path.stat().st_size
        if self._total and size != self._total:
            self.part_path.unlink(missing_ok=True)
            raise DownloadError("integrity", f"kích thước {size} B khác dự kiến {self._total} B")
        with open(self.part_path, "rb") as fh:
            magic = fh.read(4)
        if magic != b"GGUF":
            self.part_path.unlink(missing_ok=True)
            raise DownloadError("integrity", "không phải tệp GGUF hợp lệ")
        if not self.expected_sha256:
            self.part_path.unlink(missing_ok=True)
            raise DownloadError("integrity", "thiếu mã băm SHA-256 để xác thực mô hình")
        sha = hashlib.sha256()
        done = 0
        with open(self.part_path, "rb") as fh:
            while True:
                block = fh.read(4 * MB)
                if not block:
                    break
                sha.update(block)
                done += len(block)
                self._downloaded = done  # hiển thị tiến độ kiểm tra
                self._emit_progress()
        self._downloaded = size
        if sha.hexdigest().lower() != self.expected_sha256.lower():
            self.part_path.unlink(missing_ok=True)
            raise DownloadError("integrity", "SHA-256 không khớp")


# ============================================================ Tkinter dialog
_VI = {
    "title": "Tải mô hình AI ngoại tuyến",
    "intro": "Ứng dụng cần tải một mô hình AI về máy để hoạt động ngoại tuyến.",
    "row_name": "Tên mô hình", "row_size": "Dung lượng file", "row_privacy": "Bảo mật",
    "row_ram": "Yêu cầu RAM", "row_license": "Giấy phép", "row_total_req": "Tổng tài nguyên",
    "value_size": "~1.1 GB (Tệp trọng số GGUF)",
    "value_total_req": "~2.5 - 3 GB (Bao gồm file 1.1 GB + Runtime Ollama ~1 GB + RAM hoạt động ~1.5 GB).",
    "value_privacy": "Chạy 100% ngoại tuyến sau khi cấu hình Runtime; dữ liệu không rời khỏi máy bạn.",
    "value_ram": "Tối thiểu 4 GB (hệ thống nạp mô hình dùng ~1.5 GB), khuyến nghị 8 GB trở lên.",
    "value_license": "Mã nguồn mở: MIT (DeepSeek-R1), nền Qwen2.5 theo Apache-2.0.",
    "accept": "Chấp nhận & Bắt đầu tải", "skip": "Bỏ qua", "pause": "Tạm dừng",
    "resume": "Tiếp tục", "retry": "Thử lại", "stop_close": "Dừng & đóng",
    "status_connecting": "Đang kết nối tới Hugging Face...",
    "status_downloading": "Đang tải...",
    "status_paused": "Đã tạm dừng. Có thể tiếp tục bất cứ lúc nào.",
    "status_retrying": "Mất kết nối, đang thử lại ({detail})...",
    "status_verifying": "Đang kiểm tra tính toàn vẹn của tệp...",
    "status_completed": "Tải xong và đã xác minh.",
    "done_message": "Đã tải xong mô hình:\n{path}",
    "confirm_close": "Đang tải. Dừng lại và đóng? Tiến trình được giữ để tiếp tục lần sau.",
    "error_network": "Mất kết nối mạng: {detail}. Hãy kiểm tra Internet rồi bấm Thử lại (tải tiếp từ chỗ dừng).",
    "error_disk_full": "Ổ đĩa không đủ dung lượng: {detail}.",
    "error_integrity": "Tệp tải về bị lỗi hoặc không toàn vẹn: {detail}. Vui lòng tải lại.",
    "error_http": "Máy chủ từ chối yêu cầu: {detail}",
    "error_permission": "Không có quyền ghi vào thư mục lưu: {detail}",
    "error_unknown": "Lỗi không xác định: {detail}",
}


def _tr(key: str, **kw: object) -> str:
    full = f"model_dialog.{key}"
    text = _i18n_t(full, **kw) if _i18n_t else full
    if text == full:  # chưa có trong locale -> mặc định tiếng Việt
        text = _VI.get(key, key)
        try:
            text = text.format(**kw)
        except (KeyError, IndexError, ValueError):
            pass
    return text


def _fmt_eta(sec: Optional[float]) -> str:
    if sec is None:
        return "--"
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


class ModelDownloadDialog:
    """Hộp thoại modal. Dùng .show() -> Path | None."""

    def __init__(self, parent=None, downloader: Optional[HFModelDownloader] = None) -> None:
        import tkinter as tk
        from tkinter import messagebox, ttk

        self._tk, self._ttk, self._mb = tk, ttk, messagebox
        self._own_root = None
        if parent is None:
            self._own_root = tk.Tk()
            self._own_root.withdraw()
            parent = self._own_root
        self.parent = parent

        self.top = tk.Toplevel(parent)

        try:

            p_top = parent.winfo_toplevel()

            if hasattr(p_top, '_app_icon_photo') and p_top._app_icon_photo:

                self.top.iconphoto(False, p_top._app_icon_photo)

            if hasattr(p_top, 'ico_path') and p_top.ico_path:

                self.top.iconbitmap(p_top.ico_path)

        except Exception:

            pass

        self.dl = downloader or HFModelDownloader()
        self.dl.on_progress = lambda info: self._q.put(("progress", info))
        self.dl.on_state = lambda st, msg: self._q.put(("state", st, msg))
        self.result_path: Optional[Path] = None
        self._q: "queue.Queue" = queue.Queue()
        self._mode = "start"   # start | pause | resume | retry
        self._closing = False

        self._build_ui()
        self.top.protocol("WM_DELETE_WINDOW", self._on_skip_or_close)
        self.top.resizable(False, False)
        if self._own_root is None:
            self.top.transient(parent)
        self.top.after(100, self._poll)

    # ------------------------------------------------------------- UI
    def _build_ui(self) -> None:
        tk, ttk = self._tk, self._ttk
        self.top.title(_tr("title"))
        outer = ttk.Frame(self.top, padding=16)
        outer.grid(sticky="nsew")

        ttk.Label(outer, text=_tr("title"), font=("Segoe UI", 13, "bold")).grid(sticky="w")
        ttk.Label(outer, text=_tr("intro"), wraplength=440).grid(sticky="w", pady=(4, 10))

        box = ttk.LabelFrame(outer, padding=10)
        box.grid(sticky="ew")
        size_gb = self._approx_size_text()
        rows = [
            (_tr("row_name"), self.dl.filename),
            (_tr("row_size"), f"{size_gb} (Tệp trọng số GGUF)"),
            ("Tổng tài nguyên Offline", "~2.5 - 3 GB (File 1.1 GB + Ollama Engine ~1 GB + RAM ~1.5 GB)"),
            (_tr("row_privacy"), _tr("value_privacy")),
            (_tr("row_ram"), _tr("value_ram")),
            (_tr("row_license"), _tr("value_license")),
            ("Tùy chọn Cloud (0 MB)", "Dùng Gemini API: 0 MB đĩa, 0 MB RAM, không cần Ollama"),
        ]
        for i, (k, v) in enumerate(rows):
            ttk.Label(box, text=k + ":", font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="nw", padx=(0, 10), pady=2)
            ttk.Label(box, text=v, wraplength=320, justify="left").grid(row=i, column=1, sticky="w", pady=2)

        # Vị trí lưu trữ mô hình (Cho phép người dùng chọn bất kỳ ổ đĩa nào: C:, D:, E:...)
        dest_box = ttk.Frame(outer)
        dest_box.grid(sticky="ew", pady=(6, 2))
        self.lbl_dest_path = ttk.Label(dest_box, text=f"Lưu tại: {str(self.dl.dest_dir)}", font=("Segoe UI", 8), wraplength=330)
        self.lbl_dest_path.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def _on_choose_dest():
            from tkinter import filedialog
            chosen = filedialog.askdirectory(parent=self.top, title="Chọn thư mục lưu mô hình AI (bất kỳ ổ đĩa nào)")
            if chosen:
                self.dl.dest_dir = Path(chosen)
                self.lbl_dest_path.config(text=f"Lưu tại: {str(self.dl.dest_dir)}")

        self.btn_choose_dest = ttk.Button(dest_box, text="📁 Chọn ổ đĩa...", command=_on_choose_dest)
        self.btn_choose_dest.pack(side=tk.RIGHT, padx=(4, 0))

        self.prog_frame = ttk.Frame(outer)
        self.status_var = tk.StringVar()
        self.detail_var = tk.StringVar()
        ttk.Label(self.prog_frame, textvariable=self.status_var, wraplength=440).grid(sticky="w")
        self.bar = ttk.Progressbar(self.prog_frame, orient="horizontal", length=440, mode="determinate", maximum=100)
        self.bar.grid(sticky="ew", pady=4)
        ttk.Label(self.prog_frame, textvariable=self.detail_var).grid(sticky="w")
        self.err_label = tk.Label(self.prog_frame, fg="#c0392b", wraplength=440, justify="left")

        self.btns = ttk.Frame(outer)
        self.btns.grid(sticky="e", pady=(12, 0), row=99)
        self.accept_btn = ttk.Button(self.btns, text=_tr("accept"), command=self._on_primary)
        self.accept_btn.grid(row=0, column=0, padx=(0, 8))
        self.skip_btn = ttk.Button(self.btns, text=_tr("skip"), command=self._on_skip_or_close)
        self.skip_btn.grid(row=0, column=1)

    def _approx_size_text(self) -> str:
        size = self.dl._total or APPROX_SIZE
        return f"~{size / 1024 ** 3:.1f} GB"

    # -------------------------------------------------------- actions
    def _on_primary(self) -> None:
        if self._mode == "start":
            self.prog_frame.grid(sticky="ew", pady=(12, 0), row=50)
            self.skip_btn.configure(text=_tr("stop_close"))
            self.status_var.set(_tr("status_connecting"))
            self.dl.start()
        elif self._mode == "pause":
            self.accept_btn.state(["disabled"])
            self.dl.pause()
        elif self._mode in ("resume", "retry"):
            self.err_label.grid_forget()
            self.status_var.set(_tr("status_connecting"))
            self.dl.start()

    def _on_skip_or_close(self) -> None:
        if self.dl.is_running:
            if not self._mb.askyesno(_tr("title"), _tr("confirm_close"), parent=self.top):
                return
            self.dl.pause()
        self.result_path = None
        self._close()

    def _close(self) -> None:
        self._closing = True
        try:
            self.top.grab_release()
        except Exception:  # noqa: BLE001
            pass
        self.top.destroy()

    # ----------------------------------------------------------- poll
    def _poll(self) -> None:
        if self._closing:
            return
        try:
            while True:
                item = self._q.get_nowait()
                if item[0] == "progress":
                    self._on_progress(item[1])
                else:
                    self._on_state(item[1], item[2])
                if self._closing:
                    return
        except queue.Empty:
            pass
        self.top.after(100, self._poll)

    def _on_progress(self, info: ProgressInfo) -> None:
        self.bar["value"] = info.percent
        if info.total_bytes:
            self.detail_var.set(
                f"{info.percent:.1f}%  |  {info.downloaded_mb:,.0f} / {info.total_mb:,.0f} MB  |  "
                f"{info.speed_mbps:.2f} MB/s  |  ETA {_fmt_eta(info.eta_seconds)}"
            )
        else:
            self.detail_var.set(f"{info.downloaded_mb:,.0f} MB  |  {info.speed_mbps:.2f} MB/s")

    def _on_state(self, state: DownloadState, msg: str) -> None:
        S = DownloadState
        enable = lambda text, mode: (self.accept_btn.configure(text=_tr(text)),
                                     self.accept_btn.state(["!disabled"]), setattr(self, "_mode", mode))
        if state == S.CONNECTING:
            self.status_var.set(_tr("status_connecting"))
            self.accept_btn.state(["disabled"])
        elif state == S.DOWNLOADING:
            self.status_var.set(_tr("status_downloading"))
            enable("pause", "pause")
        elif state == S.RETRYING:
            self.status_var.set(_tr("status_retrying", detail=msg))
        elif state == S.PAUSED:
            self.status_var.set(_tr("status_paused"))
            enable("resume", "resume")
            if self._closing:
                return
        elif state == S.VERIFYING:
            self.status_var.set(_tr("status_verifying"))
            self.accept_btn.state(["disabled"])
            self.skip_btn.state(["disabled"])
        elif state == S.COMPLETED:
            self.status_var.set(_tr("status_completed"))
            self.bar["value"] = 100
            self.result_path = self.dl.final_path
            self._mb.showinfo(_tr("title"), _tr("done_message", path=str(self.result_path)), parent=self.top)
            self._close()
        elif state == S.ERROR:
            err = self.dl.last_error or DownloadError("unknown", msg)
            self.err_label.configure(text=_tr(f"error_{err.code}", detail=err.detail))
            self.err_label.grid(sticky="w", pady=(6, 0))
            self.status_var.set("")
            self.skip_btn.state(["!disabled"])
            enable("retry", "retry")

    # ----------------------------------------------------------- show
    def show(self) -> Optional[Path]:
        top = self.top
        top.update_idletasks()
        w, h = top.winfo_reqwidth(), top.winfo_reqheight()
        x = (top.winfo_screenwidth() - w) // 2
        y = (top.winfo_screenheight() - h) // 3
        top.geometry(f"+{x}+{y}")
        top.wait_visibility()
        top.grab_set()
        top.focus_force()
        top.wait_window()
        if self._own_root is not None:
            self._own_root.destroy()
        return self.result_path


def ask_download_model(parent=None, downloader: Optional[HFModelDownloader] = None) -> Optional[Path]:
    """Nếu mô hình đã có thì trả về luôn; nếu chưa thì mở hộp thoại tải."""
    dl = downloader or HFModelDownloader()
    if dl.is_downloaded():
        return dl.final_path
    dlg = ModelDownloadDialog(parent, dl)
    return dlg.show()


if __name__ == "__main__":
    print("Kết quả:", ask_download_model())
