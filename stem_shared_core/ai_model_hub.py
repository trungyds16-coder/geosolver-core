# -*- coding: utf-8 -*-
"""
ai_model_hub.py
===============

Module độc lập quản lý suy luận AI cho hệ sinh thái phần mềm giáo dục STEM
trên Windows (Python 3.10+).

Hai nguồn suy luận
------------------
1. LOCAL (offline): DeepSeek-R1-Distill-Qwen-1.5B (GGUF Q4_K_M)
   * Ưu tiên ``llama-cpp-python`` nếu tìm thấy file ``.gguf`` trong
     ``%LOCALAPPDATA%\\AIMathHub\\models\\`` (và thư viện đã được cài).
   * Nếu không, dùng dịch vụ Ollama cục bộ (http://localhost:11434).
2. CLOUD (online): Google Gemini API (mặc định ``gemini-2.0-flash``, tự lùi về
   ``gemini-1.5-flash`` nếu model không tồn tại). Chỉ dùng khi có API Key.

Đặc điểm chính
--------------
* Lazy loading: KHÔNG nạp mô hình khi khởi động / khi tạo ``AIModelHub``.
  Mô hình chỉ được nạp ở lần suy luận đầu tiên, được giữ trong cache một
  khoảng "nhàn rỗi" (mặc định 120 giây) rồi tự giải phóng RAM.
* Streaming: ``AIModelHub.stream()`` là generator trả về từng mảnh
  (``StreamChunk``) theo thời gian thực. ``TkStreamBridge`` chạy suy luận ở luồng
  nền và đẩy kết quả về luồng giao diện Tkinter an toàn, không làm đơ UI.
* Tách chuỗi suy nghĩ ``<think>...</think>`` khỏi lời giải chính thức ngay
  trong lúc streaming (xử lý cả trường hợp thẻ bị cắt giữa hai token).
* Bắt lỗi rõ ràng: timeout, thiếu model, sai/thiếu API Key, hết quota, mất mạng,
  Ollama chưa chạy, không đủ RAM để nạp model...
* Chỉ dùng thư viện chuẩn của Python cho phần HTTP (urllib). ``llama-cpp-python``
  là phụ thuộc tùy chọn và chỉ được import khi thật sự cần.

Cách dùng nhanh
---------------
>>> from ai_model_hub import AIModelHub, ChunkKind
>>> hub = AIModelHub()                      # chưa nạp gì vào RAM
>>> for chunk in hub.stream("Giải phương trình x^2 - 5x + 6 = 0"):
...     if chunk.kind is ChunkKind.THINKING:
...         print(chunk.text, end="")       # chuỗi suy nghĩ
...     elif chunk.kind is ChunkKind.ANSWER:
...         print(chunk.text, end="")       # lời giải chính thức

Chạy thử giao diện Tkinter:   ``python ai_model_hub.py``
Chạy thử dòng lệnh:           ``python ai_model_hub.py --cli "2+2 bằng mấy?"``
Xem trạng thái các nguồn:     ``python ai_model_hub.py --status``
"""

from __future__ import annotations

import argparse
import enum
import gc
import http.client
import importlib.util
import json
import logging
import os
import queue
import re
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator

__all__ = [
    "AIModelHub",
    "HubConfig",
    "GenerationConfig",
    "ModelSource",
    "ChunkKind",
    "StreamChunk",
    "InferenceResult",
    "ThinkTagParser",
    "TkStreamBridge",
    "AIModelHubError",
    "ModelNotFoundError",
    "ModelLoadError",
    "ApiKeyError",
    "QuotaExceededError",
    "ConnectionTimeoutError",
    "BackendUnavailableError",
    "AllSourcesFailedError",
    "default_models_dir",
]

logger = logging.getLogger("ai_model_hub")

# --------------------------------------------------------------------------- #
# Hằng số
# --------------------------------------------------------------------------- #

APP_FOLDER_NAME = "AIMathHub"
OLLAMA_DEFAULT_URL = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "deepseek-r1:1.5b"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_DEFAULT_MODELS = (
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
)

THINK_OPEN = "<think>"
THINK_CLOSE = "</think>"

# Định dạng prompt của DeepSeek-R1-Distill-Qwen (dùng ký tự full-width theo
# chuẩn của mô hình). Không thêm BOS thủ công vì llama.cpp / Ollama tự thêm.
_DS_USER = "<\uff5cUser\uff5c>"
_DS_ASSISTANT = "<\uff5cAssistant\uff5c>"
_DS_EOS = "<\uff5cend\u2581of\u2581sentence\uff5c>"

DEFAULT_SYSTEM_PROMPT = (
    "Bạn là chuyên gia tính toán và giải tích STEM (Toán, Lý, Hóa, Tin học). "
    "Hãy suy luận logic, ngắn gọn, trực diện, chính xác theo Ground Truth, "
    "trình bày tối giản theo quy chuẩn kỹ thuật. Kết thúc bằng câu 'Đáp số:' "
    "nếu bài toán có đáp số."
)

_GEMINI_THINK_HINT = (
    "\n\nĐịnh dạng bắt buộc: trước tiên viết phần suy nghĩ nháp ngắn gọn bên "
    "trong cặp thẻ <think>...</think>, sau đó viết lời giải chính thức bên "
    "ngoài thẻ."
)


# --------------------------------------------------------------------------- #
# Ngoại lệ
# --------------------------------------------------------------------------- #

class AIModelHubError(Exception):
    """Lớp cơ sở cho mọi lỗi phát sinh từ ``ai_model_hub``."""


class ModelNotFoundError(AIModelHubError):
    """Không tìm thấy file mô hình / mô hình Ollama / mô hình Gemini."""


class ModelLoadError(AIModelHubError):
    """Có file mô hình nhưng nạp thất bại (hỏng file, thiếu RAM...)."""


class ApiKeyError(AIModelHubError):
    """Thiếu, sai hoặc không đủ quyền với API Key."""


class QuotaExceededError(AIModelHubError):
    """Vượt hạn mức (HTTP 429) của dịch vụ đám mây."""


class ConnectionTimeoutError(AIModelHubError):
    """Hết thời gian chờ khi kết nối hoặc chờ dữ liệu."""


class BackendUnavailableError(AIModelHubError):
    """Không kết nối được tới dịch vụ (Ollama chưa chạy, mất mạng, lỗi 5xx)."""


class AllSourcesFailedError(AIModelHubError):
    """Tất cả các nguồn suy luận khả dụng đều thất bại."""

    def __init__(self, errors: list[tuple[str, Exception]]) -> None:
        self.errors = errors
        lines = [f"- {name}: {exc}" for name, exc in errors]
        super().__init__("Mọi nguồn suy luận đều thất bại:\n" + "\n".join(lines))


# Các lỗi cho phép tự động chuyển sang nguồn dự phòng (khi chưa có output).
_FALLBACK_ERRORS = (
    ModelNotFoundError,
    ModelLoadError,
    ApiKeyError,
    QuotaExceededError,
    ConnectionTimeoutError,
    BackendUnavailableError,
)


# --------------------------------------------------------------------------- #
# Kiểu dữ liệu công khai
# --------------------------------------------------------------------------- #

class ModelSource(enum.Enum):
    """Nguồn suy luận mà người gọi muốn dùng."""

    AUTO = "auto"
    LOCAL = "local"
    CLOUD = "cloud"


class ChunkKind(enum.Enum):
    """Loại mảnh dữ liệu trong luồng streaming."""

    THINKING = "thinking"   # chuỗi suy nghĩ (trong <think>...</think>)
    ANSWER = "answer"       # lời giải chính thức
    INFO = "info"           # thông báo trạng thái (nguồn đang dùng, fallback...)
    DONE = "done"           # kết thúc, ``result`` chứa kết quả đầy đủ


@dataclass(frozen=True)
class StreamChunk:
    """Một mảnh dữ liệu được trả về trong lúc streaming."""

    kind: ChunkKind
    text: str = ""
    result: "InferenceResult | None" = None


@dataclass
class InferenceResult:
    """Kết quả đầy đủ của một lần suy luận."""

    thinking: str = ""
    answer: str = ""
    source_label: str = ""
    elapsed_seconds: float = 0.0
    cancelled: bool = False
    incomplete_thinking: bool = False  # kết thúc khi còn đang "suy nghĩ"
    fallback_used: bool = False


@dataclass
class GenerationConfig:
    """Tham số sinh văn bản toán học bám sát dữ liệu (temperature = 0.1 chống bịa đặt)."""

    max_tokens: int = 4096
    temperature: float = 0.1
    top_p: float = 0.95
    stop: tuple[str, ...] = (_DS_EOS, _DS_USER)


def default_models_dir() -> Path:
    """Trả về thư mục chứa model trên ổ D (D:\\AI DATA\\STEM_APP\\models\\gguf) nếu khả dụng."""
    d_dir = Path(r"D:\AI DATA\STEM_APP\models\gguf")
    if d_dir.exists():
        return d_dir
    d_parent = Path(r"D:\AI DATA\STEM_APP\models")
    if d_parent.exists():
        return d_parent
    base = os.environ.get("LOCALAPPDATA")
    root = Path(base) if base else Path.home() / "AppData" / "Local"
    return root / APP_FOLDER_NAME / "models"


def is_valid_gemini_key(key: str | None) -> bool:
    """Kiểm tra tính hợp lệ của Gemini API Key (loại trừ chuỗi lệnh, khoảng trắng, ký tự điều khiển)."""
    if not key or not isinstance(key, str):
        return False
    k = key.strip()
    if any(c in k for c in (" ", "\n", "\r", "\t", '"', "'", "\\", "/", "=")):
        return False
    if len(k) < 20 or len(k) > 100:
        return False
    return True


def _default_gemini_key() -> str | None:
    """Tự động tải Gemini API Key từ biến môi trường hoặc tệp lưu trữ cục bộ (chỉ nhận key hợp lệ)."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if is_valid_gemini_key(key):
        return key.strip()
    try:
        d_key = Path(r"D:\AI DATA\STEM_APP\models\gemini_api_key.txt")
        if d_key.is_file():
            content = d_key.read_text("utf-8").strip()
            if is_valid_gemini_key(content):
                return content
            elif content:
                # Xóa tệp nếu chứa chuỗi rác hoặc lệnh terminal
                d_key.write_text("", encoding="utf-8")
        key_file = default_models_dir().parent / "gemini_api_key.txt"
        if key_file.is_file():
            content = key_file.read_text("utf-8").strip()
            if is_valid_gemini_key(content):
                return content
    except Exception:
        pass
    return None


@dataclass
class HubConfig:
    """Cấu hình tổng của ``AIModelHub``."""

    models_dir: Path = field(default_factory=default_models_dir)
    gguf_filename: str | None = None          # None: tự dò file phù hợp
    ollama_url: str = OLLAMA_DEFAULT_URL
    ollama_model: str = OLLAMA_DEFAULT_MODEL
    gemini_api_key: str | None = field(default_factory=_default_gemini_key)
    gemini_models: tuple[str, ...] = GEMINI_DEFAULT_MODELS
    gemini_request_think_tags: bool = True    # yêu cầu Gemini xuất <think>
    idle_unload_seconds: float = 120.0        # tự giải phóng RAM sau N giây rảnh
    n_ctx: int = 8192
    n_threads: int | None = None              # None: tự chọn theo số lõi CPU
    n_gpu_layers: int = 0
    local_timeout: float = 180.0              # chờ dữ liệu từ Ollama (giây)
    cloud_timeout: float = 60.0               # chờ dữ liệu từ Gemini (giây)
    auto_prefer_local: bool = False           # AUTO: ưu tiên local dù có API Key
    system_prompt: str = DEFAULT_SYSTEM_PROMPT


# --------------------------------------------------------------------------- #
# Bộ tách <think>...</think> theo luồng
# --------------------------------------------------------------------------- #

class ThinkTagParser:
    """Tách chuỗi suy nghĩ và lời giải từ luồng văn bản, từng mảnh một.

    Xử lý đúng cả khi thẻ bị cắt giữa hai token (ví dụ ``"</th"`` rồi
    ``"ink>"``). Có thể bắt đầu ở trạng thái "đang suy nghĩ" (``start_in_thinking``)
    cho các prompt đã kết thúc bằng ``<think>\\n``.

    Cách dùng::

        parser = ThinkTagParser(start_in_thinking=True)
        for piece in stream:
            for kind, text in parser.feed(piece):
                ...
        for kind, text in parser.flush():
            ...
    """

    def __init__(self, start_in_thinking: bool = False) -> None:
        self._in_thinking = start_in_thinking
        self._buf = ""
        self._strip_leading = False

    @property
    def in_thinking(self) -> bool:
        """True nếu hiện đang ở bên trong khối suy nghĩ."""
        return self._in_thinking

    @staticmethod
    def _partial_suffix_len(buf: str, tags: tuple[str, ...]) -> int:
        """Độ dài lớn nhất của phần đuôi ``buf`` có thể là đầu của một thẻ."""
        best = 0
        for tag in tags:
            limit = min(len(tag) - 1, len(buf))
            for k in range(limit, best, -1):
                if buf.endswith(tag[:k]):
                    best = k
                    break
        return best

    def feed(self, text: str) -> list[tuple[ChunkKind, str]]:
        """Nạp thêm một mảnh văn bản và trả về các đoạn đã xác định loại."""
        out: list[tuple[ChunkKind, str]] = []
        if not text:
            return out
        self._buf += text
        tags = (THINK_OPEN, THINK_CLOSE)

        while self._buf:
            if not self._in_thinking and self._strip_leading:
                stripped = self._buf.lstrip()
                self._buf = stripped
                if not self._buf:
                    break
                self._strip_leading = False

            open_idx = self._buf.find(THINK_OPEN)
            close_idx = self._buf.find(THINK_CLOSE)

            if self._in_thinking:
                if close_idx >= 0 and (open_idx < 0 or close_idx < open_idx):
                    seg = self._buf[:close_idx]
                    self._buf = self._buf[close_idx + len(THINK_CLOSE):]
                    if seg:
                        out.append((ChunkKind.THINKING, seg))
                    self._in_thinking = False
                    self._strip_leading = True
                    continue
                if open_idx >= 0:
                    # Thẻ mở thừa khi đang suy nghĩ: bỏ qua thẻ, giữ nội dung.
                    seg = self._buf[:open_idx]
                    self._buf = self._buf[open_idx + len(THINK_OPEN):]
                    if seg:
                        out.append((ChunkKind.THINKING, seg))
                    continue
                hold = self._partial_suffix_len(self._buf, tags)
                emit = self._buf[: len(self._buf) - hold]
                self._buf = self._buf[len(self._buf) - hold:]
                if emit:
                    out.append((ChunkKind.THINKING, emit))
                break

            # Đang ở phần lời giải
            if open_idx >= 0 and (close_idx < 0 or open_idx < close_idx):
                seg = self._buf[:open_idx]
                self._buf = self._buf[open_idx + len(THINK_OPEN):]
                if seg:
                    out.append((ChunkKind.ANSWER, seg))
                self._in_thinking = True
                continue
            if close_idx >= 0:
                # Thẻ đóng thừa ngoài khối suy nghĩ: bỏ thẻ, giữ nội dung.
                seg = self._buf[:close_idx]
                self._buf = self._buf[close_idx + len(THINK_CLOSE):]
                if seg:
                    out.append((ChunkKind.ANSWER, seg))
                continue
            hold = self._partial_suffix_len(self._buf, tags)
            emit = self._buf[: len(self._buf) - hold]
            self._buf = self._buf[len(self._buf) - hold:]
            if emit:
                out.append((ChunkKind.ANSWER, emit))
            break

        return out

    def flush(self) -> list[tuple[ChunkKind, str]]:
        """Xả phần còn trong bộ đệm khi luồng đã kết thúc."""
        out: list[tuple[ChunkKind, str]] = []
        rest = self._buf
        self._buf = ""
        if not self._in_thinking and self._strip_leading:
            rest = rest.lstrip()
        if rest:
            kind = ChunkKind.THINKING if self._in_thinking else ChunkKind.ANSWER
            out.append((kind, rest))
        return out


# --------------------------------------------------------------------------- #
# Bộ lọc ngôn ngữ: Chặn triệt để ký tự ngoại lai (chữ Hán, Ả Rập, Nga...) rò rỉ từ LLM
# --------------------------------------------------------------------------- #

_EXOTIC_SCRIPT_PATTERN = re.compile(
    r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3040-\u30ff'  # CJK (Trung, Nhật, Hàn)
    r'\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff\ufb50-\ufdff\ufe70-\ufeff'  # Ả Rập, Ba Tư
    r'\u0400-\u04ff'  # Cyrillic (Nga)
    r'\u0e00-\u0e7f\u0900-\u097f]'  # Thái, Hindi
)

def _filter_cjk_characters(text: str) -> str:
    """Lọc bỏ toàn bộ ký tự ngoại lai rò rỉ từ mô hình pre-trained (Ả Rập, Trung, v.v.)."""
    if not text:
        return ""
    return _EXOTIC_SCRIPT_PATTERN.sub("", text)


# --------------------------------------------------------------------------- #
# Tiện ích HTTP
# --------------------------------------------------------------------------- #

def _build_local_opener() -> urllib.request.OpenerDirector:
    """Opener không đi qua proxy hệ thống (tránh proxy chặn localhost)."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _read_http_error(exc: urllib.error.HTTPError) -> tuple[int, str, str]:
    """Đọc thân lỗi HTTP, trả về ``(status, message, api_status)``."""
    body = ""
    try:
        body = exc.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 - không để lỗi phụ che lỗi chính
        pass
    message = body.strip()
    api_status = ""
    try:
        data = json.loads(body)
        err = data.get("error", data) if isinstance(data, dict) else {}
        if isinstance(err, dict):
            message = str(err.get("message", message))
            api_status = str(err.get("status", ""))
            details = err.get("details")
            if isinstance(details, list):
                for item in details:
                    if isinstance(item, dict) and item.get("reason"):
                        api_status = f"{api_status} {item['reason']}".strip()
        elif isinstance(err, str):
            message = err
    except (ValueError, TypeError):
        pass
    return exc.code, message[:500], api_status


def _is_timeout(exc: BaseException) -> bool:
    """Nhận diện lỗi timeout dù được bọc trong ``URLError`` hay không."""
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return True
    if isinstance(exc, urllib.error.URLError):
        return isinstance(exc.reason, (socket.timeout, TimeoutError)) or (
            "timed out" in str(exc.reason).lower()
        )
    return False


def _iter_lines(resp: Any) -> Iterator[bytes]:
    """Duyệt từng dòng của phản hồi HTTP đang streaming."""
    for raw in resp:
        yield raw


# --------------------------------------------------------------------------- #
# Engine LOCAL 1: llama-cpp-python
# --------------------------------------------------------------------------- #

class _LlamaCppEngine:
    """Gọi GGUF trực tiếp bằng ``llama-cpp-python`` với lazy load + tự giải phóng."""

    label_prefix = "Local (llama-cpp)"

    def __init__(self, cfg: HubConfig, model_path: Path) -> None:
        self._cfg = cfg
        self._path = model_path
        self._llm: Any = None
        self._lock = threading.Lock()   # llama.cpp không an toàn đa luồng
        self._timer: threading.Timer | None = None
        self._last_used = time.monotonic()

    @property
    def label(self) -> str:
        return f"{self.label_prefix}: {self._path.name}"

    @property
    def is_loaded(self) -> bool:
        return self._llm is not None

    # -- nạp / giải phóng ---------------------------------------------------- #

    def _ensure_loaded(self) -> Any:
        if self._llm is not None:
            return self._llm
        if not self._path.is_file():
            raise ModelNotFoundError(f"Không thấy file mô hình: {self._path}")
        try:
            from llama_cpp import Llama  # import trễ: thư viện khá nặng
        except ImportError as exc:
            raise ModelLoadError(
                "Chưa cài llama-cpp-python. Chạy: pip install llama-cpp-python"
            ) from exc

        n_threads = self._cfg.n_threads
        if n_threads is None:
            cpu = os.cpu_count() or 2
            n_threads = max(2, min(cpu, cpu // 2 + 1))
        logger.info("Đang nạp mô hình %s vào RAM...", self._path.name)
        try:
            self._llm = Llama(
                model_path=str(self._path),
                n_ctx=self._cfg.n_ctx,
                n_threads=n_threads,
                n_gpu_layers=self._cfg.n_gpu_layers,
                use_mmap=True,
                verbose=False,
            )
        except MemoryError as exc:
            raise ModelLoadError("Không đủ RAM để nạp mô hình.") from exc
        except Exception as exc:  # noqa: BLE001 - llama-cpp ném nhiều loại lỗi
            raise ModelLoadError(
                f"Nạp mô hình thất bại (file hỏng hoặc thiếu RAM?): {exc}"
            ) from exc
        return self._llm

    def _cancel_timer(self) -> None:
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _schedule_unload(self) -> None:
        self._cancel_timer()
        delay = self._cfg.idle_unload_seconds
        if delay <= 0:
            return
        self._last_used = time.monotonic()
        timer = threading.Timer(delay, self._idle_unload)
        timer.daemon = True
        self._timer = timer
        timer.start()

    def _idle_unload(self) -> None:
        """Gọi bởi Timer: giải phóng nếu thật sự đã rảnh đủ lâu."""
        if not self._lock.acquire(blocking=False):
            self._schedule_unload()  # đang suy luận, hẹn lại
            return
        try:
            idle = time.monotonic() - self._last_used
            if self._llm is not None and idle >= self._cfg.idle_unload_seconds:
                logger.info("Mô hình rảnh %.0fs, giải phóng RAM.", idle)
                self._free_locked()
        finally:
            self._lock.release()

    def _free_locked(self) -> None:
        llm, self._llm = self._llm, None
        if llm is not None:
            try:
                llm.close()
            except Exception:  # noqa: BLE001
                pass
            del llm
        gc.collect()

    def unload(self) -> bool:
        """Giải phóng mô hình ngay. Trả về False nếu đang bận suy luận."""
        self._cancel_timer()
        if not self._lock.acquire(timeout=5):
            return False
        try:
            self._free_locked()
            return True
        finally:
            self._lock.release()

    close = unload

    # -- suy luận ------------------------------------------------------------ #

    def stream(
        self,
        prompt: str,
        gen: GenerationConfig,
        cancel: threading.Event | None,
    ) -> Iterator[tuple[str, bool]]:
        """Sinh từng token; trả về ``(text, is_thought)`` (luôn False ở đây)."""
        self._cancel_timer()
        with self._lock:
            try:
                llm = self._ensure_loaded()
                iterator = llm.create_completion(
                    prompt=prompt,
                    max_tokens=gen.max_tokens,
                    temperature=gen.temperature,
                    top_p=gen.top_p,
                    stop=list(gen.stop),
                    repeat_penalty=1.2,
                    stream=True,
                )
                try:
                    for chunk in iterator:
                        if cancel is not None and cancel.is_set():
                            break
                        text = chunk["choices"][0].get("text", "")
                        if text:
                            yield text, False
                finally:
                    close = getattr(iterator, "close", None)
                    if callable(close):
                        close()
            except AIModelHubError:
                raise
            except ValueError as exc:
                raise AIModelHubError(
                    f"Prompt quá dài so với cửa sổ ngữ cảnh ({self._cfg.n_ctx} token): {exc}"
                ) from exc
            except MemoryError as exc:
                self._free_locked()
                raise ModelLoadError("Hết RAM khi suy luận.") from exc
            finally:
                self._last_used = time.monotonic()
                self._schedule_unload()


# --------------------------------------------------------------------------- #
# Engine LOCAL 2: Ollama
# --------------------------------------------------------------------------- #

class _OllamaEngine:
    """Gọi mô hình qua dịch vụ Ollama cục bộ. Ollama tự quản lý RAM bằng keep_alive."""

    label_prefix = "Local (Ollama)"

    def __init__(self, cfg: HubConfig) -> None:
        self._cfg = cfg
        self._base = cfg.ollama_url.rstrip("/")
        self._opener = _build_local_opener()
        self._model_name: str | None = None
        self._used = False

    @property
    def label(self) -> str:
        return f"{self.label_prefix}: {self._model_name or self._cfg.ollama_model}"

    @property
    def is_loaded(self) -> bool:
        return self._used

    def list_models(self, timeout: float = 5.0) -> list[str]:
        """Danh sách tên mô hình đang có trong Ollama (ném lỗi nếu không kết nối được)."""
        req = urllib.request.Request(f"{self._base}/api/tags", method="GET")
        try:
            with self._opener.open(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as exc:
            raise BackendUnavailableError(f"Ollama trả về lỗi HTTP {exc.code}.") from exc
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            if _is_timeout(exc):
                raise ConnectionTimeoutError("Ollama không phản hồi (timeout).") from exc
            raise BackendUnavailableError(
                f"Không kết nối được Ollama tại {self._base}. "
                "Hãy cài và chạy Ollama (https://ollama.com)."
            ) from exc
        except ValueError as exc:
            raise BackendUnavailableError("Phản hồi của Ollama không hợp lệ.") from exc
        return [str(m.get("name", "")) for m in data.get("models", []) if isinstance(m, dict)]

    def resolve_model_name(self) -> str:
        """Xác định tên mô hình có thật trong Ollama, hoặc ném ModelNotFoundError."""
        names = self.list_models()
        wanted = self._cfg.ollama_model.lower()
        for name in names:
            if name.lower() == wanted:
                return name
        for name in names:
            if name.lower().startswith(wanted):
                return name
        for name in names:
            low = name.lower()
            if "deepseek-r1" in low and ("7b" in low or "1.5b" in low):
                return name
        for name in names:
            low = name.lower()
            if "deepseek" in low or "qwen" in low:
                return name
        if names:
            return names[0]
        raise ModelNotFoundError(
            f"Ollama đang chạy nhưng chưa có mô hình '{self._cfg.ollama_model}'. "
            f"Hãy chạy: ollama pull {self._cfg.ollama_model}"
        )

    def unload(self) -> bool:
        """Yêu cầu Ollama giải phóng mô hình khỏi RAM (keep_alive = 0)."""
        if not self._used or self._model_name is None:
            return True
        body = json.dumps({"model": self._model_name, "keep_alive": 0}).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with self._opener.open(req, timeout=5) as resp:
                resp.read()
            self._used = False
            return True
        except Exception:  # noqa: BLE001 - giải phóng là "cố gắng hết sức"
            return False

    close = unload

    def stream(
        self,
        prompt: str,
        gen: GenerationConfig,
        cancel: threading.Event | None,
    ) -> Iterator[tuple[str, bool]]:
        """Streaming NDJSON từ ``/api/generate`` ở chế độ raw."""
        if self._model_name is None:
            self._model_name = self.resolve_model_name()

        keep_alive = max(1, int(self._cfg.idle_unload_seconds))
        is_qwen = bool(self._model_name and "qwen" in self._model_name.lower())
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "raw": not is_qwen,           # Qwen dùng template native, DeepSeek dùng raw
            "stream": True,
            "keep_alive": f"{keep_alive}s",
            "options": {
                "temperature": gen.temperature,
                "top_p": gen.top_p,
                "num_predict": gen.max_tokens,
                "num_ctx": self._cfg.n_ctx,
                "stop": list(gen.stop),
                "repeat_penalty": 1.2,
                "repeat_last_n": 64,
            },
        }
        req = urllib.request.Request(
            f"{self._base}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = None
        try:
            resp = self._opener.open(req, timeout=self._cfg.local_timeout)
            self._used = True
            for raw in _iter_lines(resp):
                if cancel is not None and cancel.is_set():
                    break
                line = raw.decode("utf-8", "replace").strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except ValueError:
                    continue
                if "error" in data:
                    msg = str(data["error"])
                    if "not found" in msg.lower():
                        raise ModelNotFoundError(
                            f"Ollama báo thiếu mô hình: {msg}. "
                            f"Hãy chạy: ollama pull {self._cfg.ollama_model}"
                        )
                    raise AIModelHubError(f"Ollama báo lỗi: {msg}")
                text = data.get("response", "")
                if text:
                    yield text, False
                if data.get("done"):
                    break
        except urllib.error.HTTPError as exc:
            status, message, _ = _read_http_error(exc)
            if status == 404:
                raise ModelNotFoundError(
                    f"Ollama không tìm thấy mô hình '{self._model_name}'. "
                    f"Hãy chạy: ollama pull {self._cfg.ollama_model}"
                ) from exc
            raise BackendUnavailableError(f"Ollama lỗi HTTP {status}: {message}") from exc
        except AIModelHubError:
            raise
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            if _is_timeout(exc):
                raise ConnectionTimeoutError(
                    f"Ollama không trả dữ liệu trong {self._cfg.local_timeout:.0f}s "
                    "(mô hình có thể đang nạp lâu hoặc máy quá tải)."
                ) from exc
            raise BackendUnavailableError(
                f"Mất kết nối tới Ollama tại {self._base}: {exc}"
            ) from exc
        finally:
            if resp is not None:
                try:
                    resp.close()
                except Exception:  # noqa: BLE001
                    pass


# --------------------------------------------------------------------------- #
# Backend LOCAL: chọn llama-cpp hay Ollama
# --------------------------------------------------------------------------- #

def _build_deepseek_prompt(user_prompt: str, system_prompt: str) -> str:
    """Dựng prompt đúng định dạng DeepSeek-R1-Distill, kết thúc bằng ``<think>\\n``.

    Việc ép ``<think>\\n`` ở cuối giúp mô hình luôn đưa phần suy nghĩ vào khối
    suy nghĩ; bộ tách sẽ bắt đầu ở trạng thái "đang suy nghĩ".
    """
    system = system_prompt.strip()
    head = f"{system}" if system else ""
    return f"{head}{_DS_USER}{user_prompt.strip()}{_DS_ASSISTANT}<think>\n"


class _LocalBackend:
    """Chọn và giữ engine cục bộ phù hợp (GGUF + llama-cpp, hoặc Ollama)."""

    starts_in_thinking = True

    def __init__(self, cfg: HubConfig) -> None:
        self._cfg = cfg
        self._engine: _LlamaCppEngine | _OllamaEngine | None = None
        self._engine_key: tuple[str, str] | None = None

    # -- dò file mô hình ----------------------------------------------------- #

    def find_gguf(self) -> Path | None:
        """Tìm file GGUF DeepSeek-R1-Distill-Qwen-1.5B Q4_K_M trong thư mục mô hình."""
        folder = Path(self._cfg.models_dir)
        if not folder.is_dir():
            return None
        if self._cfg.gguf_filename:
            candidate = folder / self._cfg.gguf_filename
            return candidate if candidate.is_file() else None
        try:
            files = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".gguf")
        except OSError:
            return None
        for path in files:
            low = path.name.lower()
            if "deepseek" in low and "1.5b" in low and "q4_k_m" in low:
                return path
        for path in files:
            low = path.name.lower()
            if "1.5b" in low and "q4_k_m" in low:
                return path
        return None

    @staticmethod
    def llama_cpp_installed() -> bool:
        """Kiểm tra rẻ (không import) xem llama-cpp-python đã được cài chưa."""
        try:
            return importlib.util.find_spec("llama_cpp") is not None
        except (ImportError, ValueError):
            return False

    # -- chọn engine --------------------------------------------------------- #

    def prepare(self) -> None:
        """Chọn engine; ném lỗi hướng dẫn rõ ràng nếu không có nguồn local nào."""
        gguf = self.find_gguf()
        problems: list[str] = []

        if gguf is not None:
            if self.llama_cpp_installed():
                self._set_engine(("llama", str(gguf)), lambda: _LlamaCppEngine(self._cfg, gguf))
                return
            problems.append(
                f"Có file {gguf.name} nhưng chưa cài llama-cpp-python "
                "(pip install llama-cpp-python)."
            )
        else:
            problems.append(f"Không thấy file GGUF trong {self._cfg.models_dir}.")

        ollama = _OllamaEngine(self._cfg)
        try:
            ollama.resolve_model_name()
        except ModelNotFoundError as exc:
            problems.append(str(exc))
            raise ModelNotFoundError(
                "Không có mô hình cục bộ khả dụng.\n- " + "\n- ".join(problems)
            ) from exc
        except (BackendUnavailableError, ConnectionTimeoutError) as exc:
            problems.append(str(exc))
            raise ModelNotFoundError(
                "Không có mô hình cục bộ khả dụng.\n- " + "\n- ".join(problems)
            ) from exc
        self._set_engine(("ollama", self._cfg.ollama_url), lambda: ollama)

    def _set_engine(self, key: tuple[str, str], factory: Callable[[], Any]) -> None:
        if self._engine is not None and self._engine_key == key:
            return
        if self._engine is not None:
            self._engine.unload()
        self._engine = factory()
        self._engine_key = key

    @property
    def label(self) -> str:
        return self._engine.label if self._engine is not None else "Local"

    @property
    def is_loaded(self) -> bool:
        return bool(self._engine is not None and self._engine.is_loaded)

    def stream(
        self,
        prompt: str,
        system_prompt: str,
        gen: GenerationConfig,
        cancel: threading.Event | None,
    ) -> Iterator[tuple[str, bool]]:
        if self._engine is None:
            self.prepare()
        assert self._engine is not None
        is_qwen = bool(self._cfg.ollama_model and "qwen" in self._cfg.ollama_model.lower())
        if is_qwen:
            full_prompt = f"{system_prompt.strip()}\n\n{prompt.strip()}" if system_prompt.strip() else prompt.strip()
        else:
            full_prompt = _build_deepseek_prompt(prompt, system_prompt)
        return self._engine.stream(full_prompt, gen, cancel)

    def unload(self) -> bool:
        return self._engine.unload() if self._engine is not None else True

    def close(self) -> None:
        if self._engine is not None:
            self._engine.close()


# --------------------------------------------------------------------------- #
# Backend CLOUD: Gemini
# --------------------------------------------------------------------------- #

class _GeminiBackend:
    """Gọi Google Gemini API qua REST + Server-Sent Events (không cần SDK)."""

    starts_in_thinking = False

    def __init__(self, cfg: HubConfig) -> None:
        self._cfg = cfg
        self._active_model: str | None = None

    @property
    def api_key(self) -> str:
        key = (
            self._cfg.gemini_api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )
        return key.strip()

    @property
    def has_key(self) -> bool:
        return bool(self.api_key)

    @property
    def label(self) -> str:
        model = self._active_model or (self._cfg.gemini_models[0] if self._cfg.gemini_models else "?")
        return f"Cloud (Gemini): {model}"

    @property
    def is_loaded(self) -> bool:
        return False  # không có gì nằm trong RAM cục bộ

    def prepare(self) -> None:
        """Kiểm tra điều kiện tối thiểu trước khi gọi mạng."""
        if not self.has_key:
            raise ApiKeyError(
                "Chưa có Gemini API Key. Hãy nhập key (lấy tại https://aistudio.google.com/apikey)."
            )
        if not self._cfg.gemini_models:
            raise ModelNotFoundError("Chưa cấu hình tên mô hình Gemini nào.")

    def unload(self) -> bool:
        return True

    def close(self) -> None:
        return None

    def stream(
        self,
        prompt: str,
        system_prompt: str,
        gen: GenerationConfig,
        cancel: threading.Event | None,
    ) -> Iterator[tuple[str, bool]]:
        """Thử lần lượt các mô hình cấu hình; chỉ lùi sang mô hình sau khi gặp 404."""
        self.prepare()
        last_error: ModelNotFoundError | None = None
        for model in self._cfg.gemini_models:
            emitted = False
            try:
                for item in self._stream_one(model, prompt, system_prompt, gen, cancel):
                    emitted = True
                    yield item
                return
            except ModelNotFoundError as exc:
                if emitted:
                    raise
                last_error = exc
                logger.warning("Mô hình Gemini '%s' không khả dụng, thử mô hình kế tiếp.", model)
                continue
        raise last_error or ModelNotFoundError("Không có mô hình Gemini nào khả dụng.")

    def _stream_one(
        self,
        model: str,
        prompt: str,
        system_prompt: str,
        gen: GenerationConfig,
        cancel: threading.Event | None,
    ) -> Iterator[tuple[str, bool]]:
        system_text = system_prompt.strip()
        if self._cfg.gemini_request_think_tags:
            system_text += _GEMINI_THINK_HINT
        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": gen.temperature,
                "topP": gen.top_p,
                "maxOutputTokens": gen.max_tokens,
            },
        }
        if system_text.strip():
            payload["systemInstruction"] = {"parts": [{"text": system_text}]}

        url = f"{GEMINI_BASE_URL}/models/{model}:streamGenerateContent?alt=sse&key={self.api_key}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,  # key nằm cả ở header và URL để bảo đảm tương thích
            },
            method="POST",
        )
        resp = None
        try:
            resp = urllib.request.urlopen(req, timeout=self._cfg.cloud_timeout)
            self._active_model = model
            for raw in _iter_lines(resp):
                if cancel is not None and cancel.is_set():
                    break
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                body = line[5:].strip()
                if not body or body == "[DONE]":
                    continue
                try:
                    data = json.loads(body)
                except ValueError:
                    continue
                if isinstance(data, dict) and "error" in data:
                    err = data["error"] if isinstance(data["error"], dict) else {}
                    raise AIModelHubError(f"Gemini báo lỗi: {err.get('message', data['error'])}")
                feedback = data.get("promptFeedback", {}) if isinstance(data, dict) else {}
                if feedback.get("blockReason"):
                    raise AIModelHubError(
                        f"Gemini từ chối nội dung yêu cầu (lý do: {feedback['blockReason']})."
                    )
                for cand in data.get("candidates", []) or []:
                    content = cand.get("content", {}) or {}
                    for part in content.get("parts", []) or []:
                        text = part.get("text", "")
                        if text:
                            yield text, bool(part.get("thought"))
        except urllib.error.HTTPError as exc:
            # Nếu SSE streaming báo 404, thử fallback sang generateContent tiêu chuẩn (100% tài khoản hỗ trợ)
            if exc.code == 404:
                try:
                    fb_url = f"{GEMINI_BASE_URL}/models/{model}:generateContent?key={self.api_key}"
                    fb_req = urllib.request.Request(
                        fb_url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json", "x-goog-api-key": self.api_key},
                        method="POST",
                    )
                    with urllib.request.urlopen(fb_req, timeout=self._cfg.cloud_timeout) as fb_resp:
                        data = json.loads(fb_resp.read().decode("utf-8", "replace"))
                        self._active_model = model
                        for cand in data.get("candidates", []) or []:
                            content = cand.get("content", {}) or {}
                            for part in content.get("parts", []) or []:
                                text = part.get("text", "")
                                if text:
                                    yield text, False
                        return
                except Exception:
                    pass
            raise self._map_http_error(exc, model) from exc
        except AIModelHubError:
            raise
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            if _is_timeout(exc):
                raise ConnectionTimeoutError(
                    f"Gemini không phản hồi trong {self._cfg.cloud_timeout:.0f}s."
                ) from exc
            raise BackendUnavailableError(
                f"Không kết nối được Gemini (kiểm tra mạng/proxy/tường lửa): {exc}"
            ) from exc
        finally:
            if resp is not None:
                try:
                    resp.close()
                except Exception:  # noqa: BLE001
                    pass

    @staticmethod
    def _map_http_error(exc: urllib.error.HTTPError, model: str) -> AIModelHubError:
        status, message, api_status = _read_http_error(exc)
        blob = f"{message} {api_status}".lower()
        if status == 400 and ("api key" in blob or "api_key" in blob):
            return ApiKeyError("Gemini API Key không hợp lệ. Hãy kiểm tra lại key.")
        if status in (401, 403):
            return ApiKeyError(
                f"Gemini từ chối quyền truy cập (HTTP {status}). Key sai, bị thu hồi, "
                f"chưa bật API hoặc khu vực không được hỗ trợ. Chi tiết: {message}"
            )
        if status == 404:
            return ModelNotFoundError(f"Mô hình Gemini '{model}' không khả dụng (Lỗi 404 từ Google: {message}).")
        if status == 429:
            return QuotaExceededError(
                "Đã vượt hạn mức Gemini API (HTTP 429). Hãy chờ một lúc rồi thử lại."
            )
        if status >= 500:
            return BackendUnavailableError(f"Máy chủ Gemini đang gặp sự cố (HTTP {status}).")
        return AIModelHubError(f"Gemini trả về lỗi HTTP {status}: {message}")


# --------------------------------------------------------------------------- #
# AIModelHub: lớp điều phối chính
# --------------------------------------------------------------------------- #

class AIModelHub:
    """Điểm vào duy nhất để suy luận từ nguồn Local hoặc Cloud.

    * Tạo đối tượng rất nhẹ: không nạp mô hình, không mở kết nối mạng.
    * ``stream()`` trả về generator ``StreamChunk`` để cập nhật giao diện theo
      thời gian thực; ``generate()`` chạy đồng bộ và trả về ``InferenceResult``.
    * ``unload()`` giải phóng RAM ngay; ``close()`` dọn dẹp khi thoát ứng dụng.
    * Có thể dùng như context manager: ``with AIModelHub() as hub: ...``.
    """

    def __init__(self, config: HubConfig | None = None, *, api_key: str | None = None) -> None:
        self.config = config or HubConfig()
        if api_key:
            self.config.gemini_api_key = api_key
        self._local = _LocalBackend(self.config)
        self._cloud = _GeminiBackend(self.config)

    # -- quản lý vòng đời ----------------------------------------------------- #

    def __enter__(self) -> "AIModelHub":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def set_api_key(self, api_key: str | None) -> None:
        """Đặt/xóa Gemini API Key và tự động lưu vào đĩa để duy trì phiên làm việc."""
        k = (api_key or "").strip() or None
        self.config.gemini_api_key = k
        try:
            key_file = self.config.models_dir.parent / "gemini_api_key.txt"
            key_file.parent.mkdir(parents=True, exist_ok=True)
            if k:
                key_file.write_text(k, "utf-8")
            elif key_file.exists():
                key_file.unlink()
        except Exception as e:
            logger.warning("Không thể lưu API Key vào đĩa: %s", e)

    def set_ollama_model(self, model_name: str) -> None:
        """Đặt tên mô hình Ollama cần dùng (ví dụ 'deepseek-r1:7b' hoặc 'deepseek-r1:1.5b')."""
        self.config.ollama_model = model_name.strip()
        self._local.close()
        self._local = _LocalBackend(self.config)

    def unload(self) -> bool:
        """Giải phóng mô hình cục bộ khỏi RAM ngay lập tức."""
        return self._local.unload()

    def close(self) -> None:
        """Giải phóng toàn bộ tài nguyên (gọi khi đóng ứng dụng)."""
        self._local.close()
        self._cloud.close()

    # -- trạng thái ----------------------------------------------------------- #

    def status(self) -> dict[str, Any]:
        """Báo cáo nhanh khả năng của từng nguồn (không nạp mô hình)."""
        gguf = self._local.find_gguf()
        ollama_ok = False
        ollama_model: str | None = None
        ollama_error = ""
        ollama_installed: list[str] = []
        engine = _OllamaEngine(self.config)
        try:
            ollama_installed = engine.list_models()
            ollama_model = engine.resolve_model_name()
            ollama_ok = True
        except AIModelHubError as exc:
            ollama_error = str(exc)
        return {
            "models_dir": str(self.config.models_dir),
            "gguf_file": str(gguf) if gguf else None,
            "llama_cpp_installed": self._local.llama_cpp_installed(),
            "ollama_ready": ollama_ok,
            "ollama_model": ollama_model,
            "ollama_installed": ollama_installed,
            "ollama_error": ollama_error,
            "gemini_key_present": self._cloud.has_key,
            "gemini_models": list(self.config.gemini_models),
            "local_model_in_ram": self._local.is_loaded,
        }

    # -- chọn thứ tự nguồn ----------------------------------------------------- #

    def _resolve_order(self, source: ModelSource) -> list[tuple[ModelSource, Any]]:
        if source is ModelSource.LOCAL:
            return [(ModelSource.LOCAL, self._local)]
        if source is ModelSource.CLOUD:
            return [(ModelSource.CLOUD, self._cloud)]
        # AUTO
        if self._cloud.has_key and not self.config.auto_prefer_local:
            return [(ModelSource.CLOUD, self._cloud), (ModelSource.LOCAL, self._local)]
        if self._cloud.has_key:
            return [(ModelSource.LOCAL, self._local), (ModelSource.CLOUD, self._cloud)]
        return [(ModelSource.LOCAL, self._local)]

    # -- suy luận -------------------------------------------------------------- #

    def stream(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        config: GenerationConfig | None = None,
        source: ModelSource | str = ModelSource.AUTO,
        cancel_event: threading.Event | None = None,
    ) -> Iterator[StreamChunk]:
        """Suy luận dạng streaming.

        Trả về generator các ``StreamChunk``:
        ``INFO`` (nguồn đang dùng) -> nhiều ``THINKING`` / ``ANSWER`` -> ``DONE``.
        Ở chế độ ``AUTO``, nếu nguồn đầu thất bại *trước khi* có output thì tự
        động chuyển sang nguồn dự phòng.

        Args:
            prompt: câu hỏi của người dùng.
            system_prompt: ghi đè prompt hệ thống (mặc định lấy từ ``HubConfig``).
            config: tham số sinh văn bản.
            source: ``ModelSource`` hoặc chuỗi ``"auto" | "local" | "cloud"``.
            cancel_event: ``threading.Event``; đặt cờ này để dừng giữa chừng.

        Raises:
            ValueError: prompt rỗng.
            AIModelHubError: (và các lớp con) khi mọi nguồn đều thất bại.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt không được để trống.")
        if isinstance(source, str):
            source = ModelSource(source.lower())
        gen = config or GenerationConfig()
        system = self.config.system_prompt if system_prompt is None else system_prompt

        order = self._resolve_order(source)
        errors: list[tuple[str, Exception]] = []
        started = time.monotonic()

        for index, (src, backend) in enumerate(order):
            parser = ThinkTagParser(start_in_thinking=backend.starts_in_thinking)
            thinking_parts: list[str] = []
            answer_parts: list[str] = []
            emitted = False
            try:
                backend.prepare()
                note = f"Nguồn suy luận: {backend.label}"
                if index > 0:
                    note = f"Chuyển sang nguồn dự phòng. {note}"
                yield StreamChunk(ChunkKind.INFO, note)

                for text, is_thought in backend.stream(prompt, system, gen, cancel_event):
                    if is_thought:
                        pieces = [(ChunkKind.THINKING, text)]
                    else:
                        pieces = parser.feed(text)
                    for kind, piece in pieces:
                        piece = _filter_cjk_characters(piece)
                        if not piece:
                            continue
                        emitted = True
                        (thinking_parts if kind is ChunkKind.THINKING else answer_parts).append(piece)
                        yield StreamChunk(kind, piece)

                for kind, piece in parser.flush():
                    piece = _filter_cjk_characters(piece)
                    if not piece:
                        continue
                    emitted = True
                    (thinking_parts if kind is ChunkKind.THINKING else answer_parts).append(piece)
                    yield StreamChunk(kind, piece)

                cancelled = bool(cancel_event is not None and cancel_event.is_set())
                incomplete = parser.in_thinking and not cancelled
                result = InferenceResult(
                    thinking="".join(thinking_parts).strip(),
                    answer="".join(answer_parts).strip(),
                    source_label=backend.label,
                    elapsed_seconds=time.monotonic() - started,
                    cancelled=cancelled,
                    incomplete_thinking=incomplete,
                    fallback_used=index > 0,
                )
                if incomplete:
                    yield StreamChunk(
                        ChunkKind.INFO,
                        "Mô hình dừng khi còn đang suy nghĩ (hết max_tokens). "
                        "Hãy tăng max_tokens hoặc rút gọn câu hỏi.",
                    )
                yield StreamChunk(ChunkKind.DONE, "", result)
                return

            except _FALLBACK_ERRORS as exc:
                errors.append((backend.label, exc))
                logger.warning("Nguồn %s thất bại: %s", src.value, exc)
                can_fall_back = (
                    source is ModelSource.AUTO and not emitted and index + 1 < len(order)
                )
                if not can_fall_back:
                    if len(errors) == 1:
                        raise
                    raise AllSourcesFailedError(errors) from exc
                continue

        # Không bao giờ tới đây (vòng lặp luôn return/raise), giữ để an toàn.
        raise AllSourcesFailedError(errors)

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        config: GenerationConfig | None = None,
        source: ModelSource | str = ModelSource.AUTO,
        cancel_event: threading.Event | None = None,
        on_chunk: Callable[[StreamChunk], None] | None = None,
    ) -> InferenceResult:
        """Suy luận đồng bộ, trả về ``InferenceResult`` đầy đủ.

        ``on_chunk`` (tùy chọn) được gọi cho từng mảnh ngay trong luồng gọi hàm.
        Với giao diện Tkinter hãy dùng ``TkStreamBridge`` thay vì gọi trực tiếp
        ở luồng chính.
        """
        final: InferenceResult | None = None
        for chunk in self.stream(
            prompt,
            system_prompt=system_prompt,
            config=config,
            source=source,
            cancel_event=cancel_event,
        ):
            if on_chunk is not None:
                on_chunk(chunk)
            if chunk.kind is ChunkKind.DONE:
                final = chunk.result
        if final is None:
            raise AIModelHubError("Luồng suy luận kết thúc bất thường, không có kết quả.")
        return final


# --------------------------------------------------------------------------- #
# Cầu nối Tkinter: chạy suy luận ở luồng nền, cập nhật UI ở luồng chính
# --------------------------------------------------------------------------- #

class TkStreamBridge:
    """Chạy ``AIModelHub.stream`` ở luồng nền và chuyển kết quả an toàn về Tkinter.

    Các callback luôn được gọi ở luồng giao diện (thông qua ``root.after``), nên
    có thể thao tác trực tiếp lên widget mà không làm đơ cửa sổ.

    Ví dụ::

        bridge = TkStreamBridge(
            root, hub,
            on_thinking=lambda t: think_box.insert("end", t),
            on_answer=lambda t: answer_box.insert("end", t),
            on_info=status_var.set,
            on_done=lambda r: print(r.elapsed_seconds),
            on_error=lambda e: messagebox.showerror("Lỗi", str(e)),
        )
        bridge.start("Giải hệ phương trình ...", source="auto")
        # nút Dừng:  bridge.cancel()
    """

    def __init__(
        self,
        root: Any,
        hub: AIModelHub,
        *,
        on_thinking: Callable[[str], None] | None = None,
        on_answer: Callable[[str], None] | None = None,
        on_info: Callable[[str], None] | None = None,
        on_done: Callable[[InferenceResult], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        poll_ms: int = 25,
    ) -> None:
        self._root = root
        self._hub = hub
        self._on_thinking = on_thinking
        self._on_answer = on_answer
        self._on_info = on_info
        self._on_done = on_done
        self._on_error = on_error
        self._poll_ms = poll_ms
        self._queue: queue.Queue[tuple[str, Any]] = queue.Queue()
        self._cancel = threading.Event()
        self._thread: threading.Thread | None = None
        self._running = False

    @property
    def is_running(self) -> bool:
        """True nếu đang có một lượt suy luận chạy."""
        return self._running

    def start(self, prompt: str, **kwargs: Any) -> None:
        """Bắt đầu suy luận. ``kwargs`` chuyển thẳng cho ``AIModelHub.stream``."""
        if self._running:
            raise RuntimeError("Đang có một lượt suy luận chạy, hãy dừng hoặc chờ xong.")
        kwargs.pop("cancel_event", None)
        self._cancel.clear()
        self._running = True
        self._thread = threading.Thread(
            target=self._worker, args=(prompt, kwargs), name="AIModelHubWorker", daemon=True
        )
        self._thread.start()
        self._root.after(self._poll_ms, self._poll)

    def cancel(self) -> None:
        """Yêu cầu dừng sinh văn bản (có hiệu lực ở token kế tiếp)."""
        self._cancel.set()

    def _worker(self, prompt: str, kwargs: dict[str, Any]) -> None:
        try:
            for chunk in self._hub.stream(prompt, cancel_event=self._cancel, **kwargs):
                self._queue.put(("chunk", chunk))
        except Exception as exc:  # noqa: BLE001 - chuyển mọi lỗi về UI
            self._queue.put(("error", exc))
        finally:
            self._queue.put(("end", None))

    def _poll(self) -> None:
        finished = False
        for _ in range(200):  # giới hạn mỗi lượt để UI luôn mượt
            try:
                tag, payload = self._queue.get_nowait()
            except queue.Empty:
                break
            if tag == "chunk":
                self._dispatch(payload)
            elif tag == "error":
                if self._on_error is not None:
                    self._on_error(payload)
            elif tag == "end":
                finished = True
                break
        if finished:
            self._running = False
        else:
            self._root.after(self._poll_ms, self._poll)

    def _dispatch(self, chunk: StreamChunk) -> None:
        if chunk.kind is ChunkKind.THINKING and self._on_thinking:
            self._on_thinking(chunk.text)
        elif chunk.kind is ChunkKind.ANSWER and self._on_answer:
            self._on_answer(chunk.text)
        elif chunk.kind is ChunkKind.INFO and self._on_info:
            self._on_info(chunk.text)
        elif chunk.kind is ChunkKind.DONE and self._on_done and chunk.result is not None:
            self._on_done(chunk.result)


# --------------------------------------------------------------------------- #
# Chương trình chạy thử: giao diện Tkinter + dòng lệnh
# --------------------------------------------------------------------------- #

def _run_demo_gui() -> None:
    """Giao diện Tkinter mẫu minh họa streaming không gây đơ cửa sổ."""
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk

    root = tk.Tk()
    root.title("AI Math Hub - Demo")
    root.geometry("900x720")

    hub = AIModelHub()

    top = ttk.Frame(root, padding=8)
    top.pack(fill="x")
    ttk.Label(top, text="Nguồn:").grid(row=0, column=0, sticky="w")
    source_var = tk.StringVar(value="auto")
    ttk.Combobox(
        top, textvariable=source_var, values=("auto", "local", "cloud"), width=8, state="readonly"
    ).grid(row=0, column=1, padx=6)
    ttk.Label(top, text="Gemini API Key:").grid(row=0, column=2, sticky="w", padx=(12, 0))
    key_var = tk.StringVar(value=os.environ.get("GEMINI_API_KEY", ""))
    ttk.Entry(top, textvariable=key_var, show="*", width=40).grid(row=0, column=3, padx=6)

    ttk.Label(root, text="Câu hỏi:", padding=(8, 4)).pack(anchor="w")
    prompt_box = scrolledtext.ScrolledText(root, height=5, wrap="word")
    prompt_box.pack(fill="x", padx=8)
    prompt_box.insert("1.0", "Giải phương trình x^2 - 5x + 6 = 0 và giải thích từng bước.")

    status_var = tk.StringVar(value="Sẵn sàng (chưa nạp mô hình nào vào RAM).")
    btns = ttk.Frame(root, padding=8)
    btns.pack(fill="x")

    ttk.Label(root, text="Suy nghĩ của mô hình:", padding=(8, 4)).pack(anchor="w")
    think_box = scrolledtext.ScrolledText(root, height=10, wrap="word", foreground="#666666")
    think_box.pack(fill="both", expand=True, padx=8)
    ttk.Label(root, text="Lời giải:", padding=(8, 4)).pack(anchor="w")
    answer_box = scrolledtext.ScrolledText(root, height=12, wrap="word")
    answer_box.pack(fill="both", expand=True, padx=8)
    ttk.Label(root, textvariable=status_var, padding=8).pack(fill="x")

    def append(box: scrolledtext.ScrolledText, text: str) -> None:
        box.insert("end", text)
        box.see("end")

    def on_done(result: InferenceResult) -> None:
        tag = " (đã dừng)" if result.cancelled else ""
        status_var.set(f"Xong{tag} trong {result.elapsed_seconds:.1f}s - {result.source_label}")
        send_btn.config(state="normal")
        stop_btn.config(state="disabled")

    def on_error(exc: Exception) -> None:
        status_var.set(f"Lỗi: {type(exc).__name__}")
        send_btn.config(state="normal")
        stop_btn.config(state="disabled")
        messagebox.showerror("Lỗi suy luận", str(exc))

    bridge = TkStreamBridge(
        root,
        hub,
        on_thinking=lambda t: append(think_box, t),
        on_answer=lambda t: append(answer_box, t),
        on_info=status_var.set,
        on_done=on_done,
        on_error=on_error,
    )

    def send() -> None:
        question = prompt_box.get("1.0", "end").strip()
        if not question:
            messagebox.showwarning("Thiếu câu hỏi", "Hãy nhập câu hỏi.")
            return
        hub.set_api_key(key_var.get())
        think_box.delete("1.0", "end")
        answer_box.delete("1.0", "end")
        status_var.set("Đang xử lý...")
        send_btn.config(state="disabled")
        stop_btn.config(state="normal")
        bridge.start(question, source=source_var.get())

    def unload() -> None:
        ok = hub.unload()
        status_var.set("Đã giải phóng RAM." if ok else "Đang bận, chưa thể giải phóng.")

    send_btn = ttk.Button(btns, text="Gửi", command=send)
    send_btn.pack(side="left")
    stop_btn = ttk.Button(btns, text="Dừng", command=bridge.cancel, state="disabled")
    stop_btn.pack(side="left", padx=6)
    ttk.Button(btns, text="Giải phóng RAM", command=unload).pack(side="left")

    def on_close() -> None:
        bridge.cancel()
        hub.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def _run_cli(args: argparse.Namespace) -> int:
    """Chế độ dòng lệnh: in luồng suy nghĩ và lời giải ra console."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console Windows

    hub = AIModelHub(api_key=args.api_key)
    if args.status:
        print(json.dumps(hub.status(), ensure_ascii=False, indent=2))
        return 0

    gen = GenerationConfig(max_tokens=args.max_tokens, temperature=args.temperature)
    mode: ChunkKind | None = None
    try:
        for chunk in hub.stream(args.cli, source=args.source, config=gen):
            if chunk.kind is ChunkKind.INFO:
                print(f"[{chunk.text}]", file=sys.stderr)
            elif chunk.kind in (ChunkKind.THINKING, ChunkKind.ANSWER):
                if chunk.kind is not mode:
                    header = "\n--- SUY NGHĨ ---\n" if chunk.kind is ChunkKind.THINKING else "\n--- LỜI GIẢI ---\n"
                    print(header, end="")
                    mode = chunk.kind
                print(chunk.text, end="", flush=True)
            elif chunk.kind is ChunkKind.DONE and chunk.result is not None:
                print(f"\n\n[Hoàn tất trong {chunk.result.elapsed_seconds:.1f}s]", file=sys.stderr)
        return 0
    except AIModelHubError as exc:
        print(f"\nLỖI ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nĐã dừng.", file=sys.stderr)
        return 130
    finally:
        hub.close()


def main(argv: list[str] | None = None) -> int:
    """Điểm vào chương trình: GUI mặc định, hoặc ``--cli`` / ``--status``."""
    parser = argparse.ArgumentParser(description="AI Model Hub - demo")
    parser.add_argument("--cli", metavar="PROMPT", help="chạy một câu hỏi ở chế độ dòng lệnh")
    parser.add_argument("--status", action="store_true", help="in trạng thái các nguồn rồi thoát")
    parser.add_argument("--source", choices=("auto", "local", "cloud"), default="auto")
    parser.add_argument("--api-key", default=None, help="Gemini API Key (hoặc biến GEMINI_API_KEY)")
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.6)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    if args.cli or args.status:
        return _run_cli(args)
    _run_demo_gui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
