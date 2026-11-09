# -*- coding: utf-8 -*-
"""
ai_local_manager.py
===================

Trình quản lý AI cục bộ cho STEM_APP (Neuro-Symbolic Co-Pilot cho bài toán hình học).

Vị trí đặt file:
    D:\\AI DATA\\STEM_APP\\stem_shared_core\\ai_local_manager.py

Chạy bộ kiểm thử tích hợp (từ thư mục D:\\AI DATA\\STEM_APP):
    python -m unittest stem_shared_core.ai_local_manager

Tính năng chính:
    1. Định tuyến toàn bộ mô hình về ổ D (Ollama, GGUF, khóa API Gemini).
    2. Theo dõi RAM khả dụng, thu hồi bộ nhớ Ollama bằng keep_alive = 0,
       tự động giải phóng sau thời gian rảnh rỗi (idle auto-unload).
    3. Suy luận hybrid: Python CAS (Ground Truth) + LLM phân tích logic.
    4. Bộ lọc ký tự rác (CJK, Ả Rập, Kirin), bộ ngắt chuỗi lặp vô tận,
       bộ tách luồng <think>...</think> theo thời gian thực.
    5. Bốn profile: Python thuần, Gemini Cloud, DeepSeek-R1 7B, DeepSeek-R1 1.5B.

Chỉ dùng thư viện chuẩn; psutil và llama_cpp là tùy chọn.
"""

import base64
import ctypes
import gc
import json
import os
import re
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# =============================================================================
# HẰNG SỐ ĐỊNH TUYẾN Ổ ĐĨA D
# =============================================================================

DEFAULT_MODELS_ROOT: str = r"D:\AI DATA\STEM_APP\models"
OLLAMA_SUBDIR: str = "ollama"
GGUF_SUBDIR: str = "gguf"
GEMINI_KEY_FILENAME: str = "gemini_api_key.txt"
DEFAULT_OLLAMA_HOST: str = "http://127.0.0.1:11434"
GEMINI_API_BASE: str = "https://generativelanguage.googleapis.com/v1beta/models"

# Dung lượng RAM tối thiểu còn lại (MB) sau khi nạp mô hình để hệ thống không bị nghẹt.
RAM_SAFETY_MARGIN_MB: int = 1024


class LocalAIError(Exception):
    """Lỗi chung của trình quản lý AI cục bộ."""


# =============================================================================
# QUẢN LÝ ĐƯỜNG DẪN
# =============================================================================

class AIPaths:
    """Quản lý và dò tìm các thư mục mô hình trên ổ D."""

    def __init__(self, models_root: str | os.PathLike[str] | None = None) -> None:
        root_text = str(models_root) if models_root is not None else DEFAULT_MODELS_ROOT
        self.models_root: Path = Path(root_text)
        self.ollama_dir: Path = self.models_root / OLLAMA_SUBDIR
        self.gguf_dir: Path = self.models_root / GGUF_SUBDIR
        self.api_key_file: Path = self.models_root / GEMINI_KEY_FILENAME

    def drive_available(self) -> bool:
        """Trả về True nếu ổ đĩa của thư mục gốc tồn tại (luôn True trên hệ điều hành không có ký tự ổ)."""
        drive = self.models_root.drive
        if not drive:
            return True
        return Path(drive + "\\").exists()

    def ensure_directories(self) -> bool:
        """Tạo đầy đủ cây thư mục mô hình. Trả về False nếu ổ đĩa không tồn tại."""
        if not self.drive_available():
            return False
        self.models_root.mkdir(parents=True, exist_ok=True)
        self.ollama_dir.mkdir(parents=True, exist_ok=True)
        self.gguf_dir.mkdir(parents=True, exist_ok=True)
        return True

    def detect_layout(self) -> dict[str, bool]:
        """Phát hiện thư mục/tệp nào đã tồn tại thực sự."""
        return {
            "drive": self.drive_available(),
            "models_root": self.models_root.is_dir(),
            "ollama_dir": self.ollama_dir.is_dir(),
            "gguf_dir": self.gguf_dir.is_dir(),
            "api_key_file": self.api_key_file.is_file(),
        }

    def list_gguf_files(self) -> list[Path]:
        """Liệt kê tất cả tệp .gguf trong thư mục GGUF (sắp xếp theo tên)."""
        if not self.gguf_dir.is_dir():
            return []
        return sorted(self.gguf_dir.glob("*.gguf"), key=lambda item: item.name.lower())

    def find_gguf(self, size_hint: str) -> Path | None:
        """Tìm tệp GGUF phù hợp với gợi ý kích thước (ví dụ '1.5b'). Ưu tiên tệp có 'r1' trong tên."""
        hint = size_hint.lower()
        candidates = [item for item in self.list_gguf_files() if hint in item.name.lower()]
        if not candidates:
            return None
        for item in candidates:
            if "r1" in item.name.lower():
                return item
        return candidates[0]

    def configure_environment(self) -> None:
        """Ép Ollama lưu/đọc mô hình tại ổ D."""
        os.environ["OLLAMA_MODELS"] = str(self.ollama_dir)


# =============================================================================
# KHÓA API GEMINI
# =============================================================================

class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.c_ulong), ("pbData", ctypes.POINTER(ctypes.c_byte))]

if os.name == "nt":
    try:
        ctypes.windll.crypt32.CryptProtectData.argtypes = [
            ctypes.POINTER(_DATA_BLOB), ctypes.c_wchar_p, ctypes.POINTER(_DATA_BLOB),
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
        ]
        ctypes.windll.crypt32.CryptProtectData.restype = ctypes.c_int

        ctypes.windll.crypt32.CryptUnprotectData.argtypes = [
            ctypes.POINTER(_DATA_BLOB), ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(_DATA_BLOB),
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
        ]
        ctypes.windll.crypt32.CryptUnprotectData.restype = ctypes.c_int

        ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        ctypes.windll.kernel32.LocalFree.restype = ctypes.c_void_p
    except Exception:
        pass

def _dpapi_encrypt(data: bytes) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI chỉ khả dụng trên hệ điều hành Windows.")
    # FIX Use-After-Free: Gán buffer vào biến 'buf' để giữ reference trong suốt thời gian gọi API
    buf = ctypes.create_string_buffer(data)
    blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    blob_out = _DATA_BLOB()
    if ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(blob_in), "STEM_AI_KEY", None, None, None, 0, ctypes.byref(blob_out)
    ):
        out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return out
    raise ctypes.WinError()

def _dpapi_decrypt(data: bytes) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI chỉ khả dụng trên hệ điều hành Windows.")
    # FIX Use-After-Free: Gán buffer vào biến 'buf' để giữ reference trong suốt thời gian gọi API
    buf = ctypes.create_string_buffer(data)
    blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    blob_out = _DATA_BLOB()
    if ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
    ):
        out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return out
    raise ctypes.WinError()

_LOGGER_INITIALIZED = False

def _init_logger():
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return
    import logging
    from logging.handlers import RotatingFileHandler
    try:
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / ".local" / "share"
        log_dir = root / "AIMathHub" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "geosolver.log"
        handler = RotatingFileHandler(str(log_file), maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger = logging.getLogger("geosolver")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            logger.addHandler(handler)
        _LOGGER_INITIALIZED = True
    except Exception:
        pass

def _log_warning(msg: str, *args):
    """Ghi log cảnh báo an toàn ra rotating file log cục bộ của geosolver."""
    _init_logger()
    import logging
    try:
        logging.getLogger("geosolver").warning(msg, *args)
    except Exception:
        pass

def _log_info(msg: str, *args):
    """Ghi log thông tin an toàn ra rotating file log cục bộ của geosolver."""
    _init_logger()
    import logging
    try:
        logging.getLogger("geosolver").info(msg, *args)
    except Exception:
        pass


class GeminiKeyStore:
    """Đọc và lưu gemini_api_key.txt an toàn với Windows DPAPI (CryptProtectData)."""

    def __init__(self, key_file: Path) -> None:
        self.key_file: Path = key_file
        self.last_warning: str | None = None

    def read(self) -> str | None:
        """Đọc khóa API (giải mã Windows DPAPI hoặc nâng cấp khóa cũ).
        Nguyên tắc fail-soft tại ranh giới người dùng: Bắt lỗi khi tệp bị sao chép sang máy khác
        (SID khác), tài khoản Windows thay đổi hoặc dữ liệu bị hỏng; ghi log warning ra file và fallback
        về biến môi trường thay vì làm sập ứng dụng lúc khởi động.
        """
        self.last_warning = None
        if self.key_file.is_file():
            try:
                content = self.key_file.read_text(encoding="utf-8").strip()
                if content.startswith("DPAPI:"):
                    raw_b64 = content[6:]
                    encrypted_bytes = base64.b64decode(raw_b64)
                    decrypted = _dpapi_decrypt(encrypted_bytes).decode("utf-8").strip()
                    return decrypted or None
                elif content:
                    # Nâng cấp khóa văn bản thường cũ lên DPAPI tự động trên Windows
                    # Lưu ý đa nền tảng: Chỉ tự nâng cấp khi chạy trên Windows NT
                    if os.name == "nt":
                        try:
                            self.save(content)
                            _log_info("Tự động nâng cấp khóa API plaintext sang Windows DPAPI thành công.")
                        except Exception as e:
                            _log_warning("Không thể nâng cấp khóa plaintext sang DPAPI (%s); khóa vẫn lưu ở dạng thô.", e)
                    return content
            except Exception as e:
                self.last_warning = f"DPAPI decryption failed ({e}); falling back to environment variable"
                _log_warning("%s", self.last_warning)
        env_value = os.environ.get("GEMINI_API_KEY", "").strip()
        return env_value or None

    def save(self, api_key: str) -> None:
        """Lưu khóa API an toàn bằng Windows DPAPI (CryptProtectData).
        Sử dụng cơ chế ghi nguyên tử (atomic write qua file tạm có f.flush() + os.fsync())
        để chống hỏng file khi mất nguồn đột ngột, và áp dụng chmod 0o600 trên nền tảng POSIX.
        """
        cleaned = api_key.strip()
        if not cleaned:
            raise ValueError("Khóa API rỗng, không thể lưu.")
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            enc = _dpapi_encrypt(cleaned.encode("utf-8"))
            payload = "DPAPI:" + base64.b64encode(enc).decode("ascii")
        else:
            payload = cleaned

        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.key_file.parent, prefix="gemini_key_", suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())  # Flush xuống đĩa vật lý trước khi rename
            if os.name != "nt":
                try:
                    os.chmod(tmp_path, 0o600)
                except Exception:
                    pass
            os.replace(tmp_path, self.key_file)
            if os.name != "nt":
                try:
                    os.chmod(self.key_file, 0o600)
                except Exception:
                    pass
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass


# =============================================================================
# THEO DÕI RAM
# =============================================================================

class _MemoryStatusEx(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


class MemoryMonitor:
    """Theo dõi RAM khả dụng bằng psutil, ctypes (Windows) hoặc /proc/meminfo (Linux)."""

    @staticmethod
    def available_ram_mb() -> float | None:
        """Trả về RAM khả dụng (MB) hoặc None nếu không đo được."""
        try:
            import psutil  # type: ignore[import-not-found]

            return float(psutil.virtual_memory().available) / (1024.0 * 1024.0)
        except Exception:
            pass
        if os.name == "nt":
            try:
                status = _MemoryStatusEx()
                status.dwLength = ctypes.sizeof(_MemoryStatusEx)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
                    return float(status.ullAvailPhys) / (1024.0 * 1024.0)
            except Exception:
                return None
            return None
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("MemAvailable:"):
                        parts = line.split()
                        return float(parts[1]) / 1024.0
        except OSError:
            return None
        return None

    @staticmethod
    def total_ram_mb() -> float | None:
        """Trả về tổng RAM vật lý (MB) hoặc None nếu không đo được."""
        try:
            import psutil  # type: ignore[import-not-found]

            return float(psutil.virtual_memory().total) / (1024.0 * 1024.0)
        except Exception:
            pass
        if os.name == "nt":
            try:
                status = _MemoryStatusEx()
                status.dwLength = ctypes.sizeof(_MemoryStatusEx)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
                    return float(status.ullTotalPhys) / (1024.0 * 1024.0)
            except Exception:
                return None
            return None
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("MemTotal:"):
                        parts = line.split()
                        return float(parts[1]) / 1024.0
        except OSError:
            return None
        return None


# =============================================================================
# BỘ LỌC KÝ TỰ RÁC, CHỐNG LẶP, TÁCH LUỒNG <think>
# =============================================================================

_EXOTIC_SCRIPT_PATTERN: re.Pattern[str] = re.compile(
    "["
    "\u4e00-\u9fff"  # CJK thống nhất
    "\u3400-\u4dbf"  # CJK mở rộng A
    "\u3000-\u303f"  # Dấu câu CJK
    "\u3040-\u30ff"  # Hiragana, Katakana
    "\uac00-\ud7af"  # Hangul
    "\uff00-\uffef"  # Ký tự toàn chiều rộng
    "\u0600-\u06ff"  # Chữ Ả Rập
    "\u0750-\u077f"  # Ả Rập bổ sung
    "\u0400-\u04ff"  # Kirin
    "\u0500-\u052f"  # Kirin bổ sung
    "]"
)


def _filter_exotic_scripts(text: str) -> str:
    """Loại bỏ 100% chữ Hán (CJK), chữ Ả Rập và chữ Kirin khỏi văn bản."""
    return _EXOTIC_SCRIPT_PATTERN.sub("", text)


class RepetitionBreaker:
    """Phát hiện mô hình bị lặp vô tận (lặp ký tự, lặp cụm ngắn, lặp câu, lặp dòng)."""

    def __init__(
        self,
        window: int = 1000,
        char_run: int = 40,
        unit_repeats: int = 8,
        phrase_repeats: int = 3,
        line_repeats: int = 4,
    ) -> None:
        self.window: int = window
        self.char_run: int = char_run
        self.unit_repeats: int = unit_repeats
        self.phrase_repeats: int = phrase_repeats
        self.line_repeats: int = line_repeats
        self._tail: str = ""
        self.triggered: bool = False
        self._char_pattern = re.compile(r"([^\s=\-_*#.~])\1{" + str(char_run - 1) + r",}")
        self._unit_pattern = re.compile(r"(.{3,60}?)\1{" + str(unit_repeats - 1) + r",}", re.DOTALL)
        self._phrase_pattern = re.compile(r"(.{30,250}?)\1{" + str(phrase_repeats - 1) + r",}", re.DOTALL)

    def reset(self) -> None:
        """Đặt lại trạng thái."""
        self._tail = ""
        self.triggered = False

    def feed(self, chunk: str) -> bool:
        """Nạp thêm đoạn văn bản. Trả về True nếu phát hiện vòng lặp và cần ngắt."""
        if self.triggered:
            return True
        self._tail = (self._tail + chunk)[-self.window :]
        if self._detect(self._tail):
            self.triggered = True
        return self.triggered

    def _detect(self, tail: str) -> bool:
        if self._char_pattern.search(tail):
            return True
        if self._unit_pattern.search(tail):
            return True
        if self._phrase_pattern.search(tail):
            return True
        lines = [line.strip() for line in tail.split("\n") if line.strip()]
        if len(lines) >= self.line_repeats:
            last_lines = lines[-self.line_repeats :]
            if len(last_lines[0]) >= 10 and all(item == last_lines[0] for item in last_lines):
                return True
        return False


class ThinkParser:
    """Tách luồng <think>...</think> theo thời gian thực, an toàn khi thẻ bị cắt giữa các chunk."""

    OPEN_TAG: str = "<think>"
    CLOSE_TAG: str = "</think>"

    def __init__(self, start_in_think: bool = False) -> None:
        self._buffer: str = ""
        self._in_think: bool = start_in_think
        self.think_text: str = ""
        self.answer_text: str = ""

    @property
    def in_think(self) -> bool:
        """True nếu đang ở bên trong khối suy nghĩ."""
        return self._in_think

    @staticmethod
    def _partial_suffix_length(buffer: str, tag: str) -> int:
        """Độ dài hậu tố dài nhất của buffer là tiền tố (chưa đầy đủ) của thẻ."""
        upper = min(len(tag) - 1, len(buffer))
        for size in range(upper, 0, -1):
            if buffer.endswith(tag[:size]):
                return size
        return 0

    def _emit(self, text: str) -> tuple[str, str]:
        if self._in_think:
            self.think_text += text
            return ("think", text)
        self.answer_text += text
        return ("answer", text)

    def feed(self, chunk: str) -> list[tuple[str, str]]:
        """Nạp một chunk, trả về danh sách sự kiện [('think'|'answer', văn bản), ...]."""
        self._buffer += chunk
        events: list[tuple[str, str]] = []
        while True:
            tag = self.CLOSE_TAG if self._in_think else self.OPEN_TAG
            index = self._buffer.find(tag)
            if index >= 0:
                before = self._buffer[:index]
                if before:
                    events.append(self._emit(before))
                self._buffer = self._buffer[index + len(tag) :]
                self._in_think = not self._in_think
                continue
            hold = self._partial_suffix_length(self._buffer, tag)
            safe_length = len(self._buffer) - hold
            if safe_length > 0:
                events.append(self._emit(self._buffer[:safe_length]))
                self._buffer = self._buffer[safe_length:]
            break
        return events

    def flush(self) -> list[tuple[str, str]]:
        """Đẩy nốt phần còn trong bộ đệm khi luồng kết thúc."""
        events: list[tuple[str, str]] = []
        if self._buffer:
            events.append(self._emit(self._buffer))
            self._buffer = ""
        return events


# =============================================================================
# CẤU TRÚC DỮ LIỆU BÀI TOÁN
# =============================================================================

@dataclass
class GeometryProblemContext:
    """Ngữ cảnh bài toán hình học đã được Python CAS tính toán (Ground Truth)."""

    problem_text: str
    ground_truth_points: list[tuple[str, float, float]] = field(default_factory=list)
    ground_truth_areas: list[tuple[str, float]] = field(default_factory=list)
    special_shapes: list[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    """Kết quả một lần sinh văn bản."""

    profile_id: int
    think_text: str = ""
    answer_text: str = ""
    stopped_by_repetition: bool = False
    elapsed_seconds: float = 0.0
    notices: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ModelProfile:
    """Mô tả một profile mô hình."""

    profile_id: int
    label: str
    backend: str  # "python" | "gemini" | "ollama" | "ollama_or_gguf"
    model_name: str
    approx_ram_mb: int
    gguf_size_hint: str = ""


PROFILES: dict[int, ModelProfile] = {
    0: ModelProfile(0, "⚡ Thuần Python (0.01s, 0 MB RAM, 100% Ground Truth)", "python", "python-cas", 0),
    1: ModelProfile(1, "☁️ Gemini Cloud (Gemini 2.0 Flash / 1.5 Flash, 0 MB RAM)", "gemini", "gemini-2.0-flash", 0),
    2: ModelProfile(2, "🖥️ Local AI DeepSeek-R1 7B (Ollama, suy luận chuyên sâu)", "ollama", "deepseek-r1:7b", 6500, "7b"),
    3: ModelProfile(3, "🖥️ Local AI DeepSeek-R1 1.5B (Ollama/GGUF, siêu nhẹ ~1.5 GB RAM)", "ollama_or_gguf", "deepseek-r1:1.5b", 1500, "1.5b"),
    4: ModelProfile(4, "🖥️ Local AI Qwen 2.5 Coder 7B (Ollama, tối ưu logic & code)", "ollama", "qwen2.5-coder:7b", 6500, "7b"),
}

GEMINI_FALLBACK_MODELS: list[str] = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
]


# =============================================================================
# KHÁCH HÀNG OLLAMA
# =============================================================================

class OllamaClient:
    """Giao tiếp HTTP với Ollama bằng urllib (không phụ thuộc thư viện ngoài)."""

    def __init__(self, host: str = DEFAULT_OLLAMA_HOST, timeout_s: float = 600.0) -> None:
        self.host: str = host.rstrip("/")
        self.timeout_s: float = timeout_s

    def _post_json(self, endpoint: str, payload: dict[str, Any], timeout_s: float | None = None) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.host + endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_s or self.timeout_s) as response:
                body = response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, OSError) as error:
            raise LocalAIError(f"Không kết nối được Ollama tại {self.host}: {error}") from error
        try:
            parsed = json.loads(body) if body.strip() else {}
        except json.JSONDecodeError:
            parsed = {}
        return parsed if isinstance(parsed, dict) else {}

    def _get_json(self, endpoint: str, timeout_s: float = 5.0) -> dict[str, Any]:
        request = urllib.request.Request(self.host + endpoint, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout_s) as response:
                body = response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, OSError) as error:
            raise LocalAIError(f"Không kết nối được Ollama tại {self.host}: {error}") from error
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def is_alive(self) -> bool:
        """Kiểm tra máy chủ Ollama có đang chạy không."""
        try:
            self._get_json("/api/tags", timeout_s=2.0)
        except LocalAIError:
            return False
        return True

    def list_installed_models(self) -> list[str]:
        """Liệt kê tên các mô hình đã cài."""
        data = self._get_json("/api/tags")
        names: list[str] = []
        for item in data.get("models", []):
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                names.append(item["name"])
        return names

    def list_running_models(self) -> list[str]:
        """Liệt kê tên các mô hình đang nằm trong RAM/VRAM."""
        data = self._get_json("/api/ps")
        names: list[str] = []
        for item in data.get("models", []):
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                names.append(item["name"])
        return names

    def build_unload_payload(self, model_name: str) -> dict[str, Any]:
        """Tạo payload thu hồi bộ nhớ ngay lập tức (keep_alive = 0)."""
        return {"model": model_name, "prompt": "", "stream": False, "keep_alive": 0}

    def unload_model(self, model_name: str) -> bool:
        """Gửi keep_alive = 0 tới /api/generate để giải phóng mô hình. Trả về True nếu thành công."""
        try:
            self._post_json("/api/generate", self.build_unload_payload(model_name), timeout_s=15.0)
        except LocalAIError:
            return False
        return True

    def stream_generate(
        self,
        model_name: str,
        prompt: str,
        keep_alive: str = "5m",
        temperature: float = 0.3,
        num_ctx: int = 4096,
        num_predict: int = 2048,
    ) -> Iterator[str]:
        """Sinh văn bản dạng luồng, trả về từng đoạn 'response'."""
        payload: dict[str, Any] = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "keep_alive": keep_alive,
            "options": {
                "temperature": temperature,
                "num_ctx": num_ctx,
                "num_predict": num_predict,
                "repeat_penalty": 1.2,
                "repeat_last_n": 64,
            },
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.host + "/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            response = urllib.request.urlopen(request, timeout=self.timeout_s)
        except (urllib.error.URLError, OSError) as error:
            raise LocalAIError(f"Không kết nối được Ollama tại {self.host}: {error}") from error
        try:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(item, dict):
                    continue
                if "error" in item:
                    raise LocalAIError(f"Ollama báo lỗi: {item['error']}")
                piece = item.get("response", "")
                if isinstance(piece, str) and piece:
                    yield piece
                if item.get("done"):
                    break
        finally:
            response.close()


# =============================================================================
# KHÁCH HÀNG GEMINI
# =============================================================================

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


class GeminiClient:
    """Giao tiếp REST với Gemini (SSE streaming) bằng urllib."""

    def __init__(self, api_key: str, timeout_s: float = 120.0) -> None:
        self.api_key: str = api_key
        self.timeout_s: float = timeout_s

    @staticmethod
    def extract_text(item: dict[str, Any]) -> str:
        """Rút văn bản từ một khối phản hồi Gemini."""
        pieces: list[str] = []
        for candidate in item.get("candidates", []):
            if not isinstance(candidate, dict):
                continue
            content = candidate.get("content", {})
            if not isinstance(content, dict):
                continue
            for part in content.get("parts", []):
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    pieces.append(part["text"])
        return "".join(pieces)

    def stream_generate(self, model_name: str, prompt: str, temperature: float = 0.3) -> Iterator[str]:
        """Sinh văn bản dạng luồng từ một mô hình Gemini."""
        url = f"{GEMINI_API_BASE}/{model_name}:streamGenerateContent?alt=sse&key={self.api_key}"
        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": 2048},
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": self.api_key},
            method="POST",
        )
        try:
            response = urllib.request.urlopen(request, timeout=self.timeout_s, context=_get_ssl_context())
        except urllib.error.HTTPError as error:
            raise LocalAIError(f"Gemini trả về lỗi HTTP {error.code} với mô hình {model_name}.") from error
        except (urllib.error.URLError, OSError) as error:
            raise LocalAIError(f"Không kết nối được Gemini: {error}") from error
        try:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                body = line[5:].strip()
                if not body:
                    continue
                try:
                    item = json.loads(body)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    text = self.extract_text(item)
                    if text:
                        yield text
        finally:
            response.close()


# =============================================================================
# TỰ ĐỘNG GIẢI PHÓNG KHI RẢNH RỖI
# =============================================================================

class IdleUnloader:
    """Đếm ngược thời gian rảnh, hết hạn thì gọi callback để giải phóng bộ nhớ."""

    def __init__(self, timeout_s: float, callback: Callable[[], None]) -> None:
        self.timeout_s: float = timeout_s
        self._callback: Callable[[], None] = callback
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def touch(self) -> None:
        """Đặt lại bộ đếm (gọi mỗi khi có hoạt động)."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self.timeout_s, self._fire)
            self._timer.daemon = True
            self._timer.start()

    def cancel(self) -> None:
        """Hủy bộ đếm."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

    def _fire(self) -> None:
        with self._lock:
            self._timer = None
        try:
            self._callback()
        except Exception:
            pass


# =============================================================================
# TRÌNH QUẢN LÝ CHÍNH
# =============================================================================

EventCallback = Callable[[str, str], None]


class AILocalManager:
    """Điều phối bốn profile mô hình, quản lý RAM và đường ống lọc luồng."""

    def __init__(
        self,
        paths: AIPaths | None = None,
        ollama_host: str = DEFAULT_OLLAMA_HOST,
        idle_timeout_s: float = 300.0,
        configure_env: bool = True,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.paths: AIPaths = paths if paths is not None else AIPaths()
        self.paths.ensure_directories()
        if configure_env:
            self.paths.configure_environment()
        self.key_store: GeminiKeyStore = GeminiKeyStore(self.paths.api_key_file)
        self.ollama: OllamaClient = ollama_client if ollama_client is not None else OllamaClient(ollama_host)
        self.memory: MemoryMonitor = MemoryMonitor()
        self.active_profile_id: int = 0
        self._loaded_ollama_models: set[str] = set()
        self._gguf_model: Any = None
        self._gguf_path: Path | None = None
        self._lock = threading.RLock()
        self.idle: IdleUnloader = IdleUnloader(idle_timeout_s, self.unload_all)

    # ------------------------------------------------------------------ RAM

    def check_ram_for_profile(self, profile_id: int) -> tuple[bool, str]:
        """Kiểm tra RAM khả dụng có đủ để nạp profile hay không."""
        profile = PROFILES[profile_id]
        if profile.approx_ram_mb <= 0:
            return True, "Profile không dùng RAM cục bộ."
        available = self.memory.available_ram_mb()
        if available is None:
            return True, "Không đo được RAM khả dụng, tiếp tục nạp mô hình."
        needed = float(profile.approx_ram_mb + RAM_SAFETY_MARGIN_MB)
        if available >= needed:
            return True, f"RAM khả dụng {available:.0f} MB, đủ cho {profile.model_name} (cần ~{needed:.0f} MB)."
        return False, f"RAM khả dụng {available:.0f} MB, không đủ cho {profile.model_name} (cần ~{needed:.0f} MB)."

    # ------------------------------------------------------- NẠP / GIẢI PHÓNG

    def unload_ollama_model(self, model_name: str) -> bool:
        """Thu hồi một mô hình Ollama bằng keep_alive = 0."""
        with self._lock:
            ok = self.ollama.unload_model(model_name)
            self._loaded_ollama_models.discard(model_name)
            return ok

    def unload_gguf(self) -> None:
        """Giải phóng mô hình GGUF đang giữ trong bộ nhớ."""
        with self._lock:
            self._gguf_model = None
            self._gguf_path = None
        gc.collect()

    def unload_all(self) -> None:
        """Giải phóng toàn bộ mô hình cục bộ (Ollama và GGUF)."""
        with self._lock:
            names = set(self._loaded_ollama_models)
            try:
                names.update(self.ollama.list_running_models())
            except LocalAIError:
                pass
            for name in names:
                self.unload_ollama_model(name)
            self.unload_gguf()

    def switch_profile(self, new_profile_id: int) -> list[str]:
        """Chuyển profile, tự thu hồi bộ nhớ của mô hình cũ nếu khác mô hình mới."""
        if new_profile_id not in PROFILES:
            raise ValueError(f"Profile không hợp lệ: {new_profile_id}")
        notices: list[str] = []
        with self._lock:
            new_profile = PROFILES[new_profile_id]
            for name in list(self._loaded_ollama_models):
                if name != new_profile.model_name:
                    if self.unload_ollama_model(name):
                        notices.append(f"Đã thu hồi bộ nhớ mô hình {name}.")
            if self._gguf_model is not None and new_profile.backend != "ollama_or_gguf":
                self.unload_gguf()
                notices.append("Đã giải phóng mô hình GGUF.")
            self.active_profile_id = new_profile_id
        return notices

    def shutdown(self) -> None:
        """Dừng bộ đếm rảnh rỗi và giải phóng toàn bộ mô hình."""
        self.idle.cancel()
        self.unload_all()

    # --------------------------------------------------------------- PROMPT

    @staticmethod
    def build_prompt(context: GeometryProblemContext) -> str:
        """Dựng prompt neuro-symbolic: LLM chỉ diễn giải, mọi số liệu lấy từ Ground Truth."""
        lines: list[str] = []
        lines.append("Bạn là chuyên gia tính toán hình học. Trình bày ngắn gọn, trực diện, logic theo chuẩn kỹ thuật.")
        lines.append("QUY TẮC: Chỉ trả lời bằng tiếng Việt. Tuyệt đối dùng đúng số liệu Ground Truth bên dưới, không tự bịa số.")
        lines.append("")
        lines.append("ĐỀ BÀI:")
        lines.append(context.problem_text.strip())
        lines.append("")
        lines.append("GROUND TRUTH (do Python CAS tính, đã kiểm chứng):")
        if context.ground_truth_points:
            lines.append("- Tọa độ các điểm:")
            for name, x_value, y_value in context.ground_truth_points:
                lines.append(f"  + {name}({x_value:.4f}; {y_value:.4f})")
        if context.ground_truth_areas:
            lines.append("- Diện tích:")
            for name, area in context.ground_truth_areas:
                lines.append(f"  + {name} = {area:.4f}")
        if context.special_shapes:
            lines.append("- Hình đặc biệt: " + ", ".join(context.special_shapes))
        lines.append("")
        lines.append("YÊU CẦU: Trình bày lời giải từng bước, ngắn gọn, nêu rõ cách dùng các kết quả Ground Truth ở trên.")
        return "\n".join(lines)

    @staticmethod
    def build_python_explanation(context: GeometryProblemContext) -> str:
        """Profile 0: diễn giải thuần Python từ Ground Truth, không dùng LLM."""
        lines: list[str] = ["Kết quả tính toán chính xác (Python CAS):"]
        if context.special_shapes:
            lines.append("Hình đặc biệt nhận diện được: " + ", ".join(context.special_shapes) + ".")
        if context.ground_truth_points:
            lines.append("Tọa độ các điểm:")
            for name, x_value, y_value in context.ground_truth_points:
                lines.append(f"- {name}({x_value:.4f}; {y_value:.4f})")
        if context.ground_truth_areas:
            lines.append("Diện tích:")
            for name, area in context.ground_truth_areas:
                lines.append(f"- {name} = {area:.4f}")
        if len(lines) == 1:
            lines.append("Không có dữ liệu Ground Truth cho đề bài này.")
        return "\n".join(lines)

    # ------------------------------------------------------ ĐƯỜNG ỐNG LỌC

    @staticmethod
    def process_stream(
        chunks: Iterable[str],
        parser: ThinkParser,
        breaker: RepetitionBreaker,
        on_event: EventCallback | None = None,
    ) -> bool:
        """Lọc ký tự rác, ngắt chuỗi lặp, tách <think>. Trả về True nếu bị ngắt do lặp."""
        stopped = False
        for raw_chunk in chunks:
            clean = _filter_exotic_scripts(raw_chunk)
            if not clean:
                continue
            if breaker.feed(clean):
                stopped = True
                break
            for kind, text in parser.feed(clean):
                if on_event is not None:
                    on_event(kind, text)
        for kind, text in parser.flush():
            if on_event is not None:
                on_event(kind, text)
        return stopped

    # ------------------------------------------------------------ NGUỒN LUỒNG

    def _stream_gguf(self, gguf_path: Path, prompt: str) -> Iterator[str]:
        try:
            from llama_cpp import Llama  # type: ignore[import-not-found]
        except Exception as error:
            raise LocalAIError("Chưa cài llama-cpp-python nên không chạy được GGUF.") from error
        with self._lock:
            if self._gguf_model is None or self._gguf_path != gguf_path:
                self._gguf_model = Llama(model_path=str(gguf_path), n_ctx=4096, verbose=False)
                self._gguf_path = gguf_path
            model = self._gguf_model
        for item in model.create_completion(prompt, max_tokens=2048, temperature=0.3, stream=True):
            try:
                piece = item["choices"][0]["text"]
            except (KeyError, IndexError, TypeError):
                continue
            if piece:
                yield piece

    def _stream_for_profile(self, profile: ModelProfile, prompt: str, notices: list[str]) -> Iterator[str]:
        if profile.backend == "gemini":
            api_key = self.key_store.read()
            if not api_key:
                raise LocalAIError(f"Chưa có khóa API Gemini. Hãy lưu vào {self.paths.api_key_file}.")
            client = GeminiClient(api_key)
            last_error: LocalAIError | None = None
            for model_name in GEMINI_FALLBACK_MODELS:
                try:
                    yield from client.stream_generate(model_name, prompt)
                    return
                except LocalAIError as error:
                    last_error = error
                    notices.append(f"Mô hình {model_name} lỗi, thử mô hình dự phòng.")
            raise last_error if last_error is not None else LocalAIError("Gemini không phản hồi.")
        if profile.backend == "ollama":
            with self._lock:
                self._loaded_ollama_models.add(profile.model_name)
            yield from self.ollama.stream_generate(profile.model_name, prompt)
            return
        if profile.backend == "ollama_or_gguf":
            use_ollama = False
            if self.ollama.is_alive():
                try:
                    installed = self.ollama.list_installed_models()
                except LocalAIError:
                    installed = []
                use_ollama = profile.model_name in installed
            if use_ollama:
                with self._lock:
                    self._loaded_ollama_models.add(profile.model_name)
                yield from self.ollama.stream_generate(profile.model_name, prompt)
                return
            gguf_path = self.paths.find_gguf(profile.gguf_size_hint)
            if gguf_path is None:
                raise LocalAIError(
                    f"Không tìm thấy mô hình {profile.model_name} trong Ollama và không có tệp GGUF "
                    f"{profile.gguf_size_hint} trong {self.paths.gguf_dir}."
                )
            notices.append(f"Dùng tệp GGUF: {gguf_path.name}")
            yield from self._stream_gguf(gguf_path, prompt)
            return
        raise LocalAIError(f"Backend không được hỗ trợ: {profile.backend}")

    # -------------------------------------------------------------- GIAO DIỆN

    def explain(
        self,
        context: GeometryProblemContext,
        profile_id: int | None = None,
        on_event: EventCallback | None = None,
    ) -> GenerationResult:
        """Sinh lời giải thích cho bài toán theo profile chọn (mặc định: profile đang hoạt động)."""
        chosen = self.active_profile_id if profile_id is None else profile_id
        if chosen not in PROFILES:
            raise ValueError(f"Profile không hợp lệ: {chosen}")
        started = time.monotonic()
        notices: list[str] = []

        if chosen in (2, 3):
            enough, message = self.check_ram_for_profile(chosen)
            notices.append(message)
            if not enough and chosen == 2:
                notices.append("Tự động hạ xuống Profile 3 (DeepSeek-R1 1.5B) để tránh tràn RAM.")
                chosen = 3
        notices.extend(self.switch_profile(chosen))
        profile = PROFILES[chosen]

        if profile.backend == "python":
            text = self.build_python_explanation(context)
            if on_event is not None:
                on_event("answer", text)
            return GenerationResult(
                profile_id=chosen,
                answer_text=text,
                elapsed_seconds=time.monotonic() - started,
                notices=notices,
            )

        self.idle.touch()
        parser = ThinkParser()
        breaker = RepetitionBreaker()
        prompt = self.build_prompt(context)
        stopped = self.process_stream(self._stream_for_profile(profile, prompt, notices), parser, breaker, on_event)
        self.idle.touch()
        if stopped:
            notices.append("Đã ngắt do mô hình lặp vô tận.")
        return GenerationResult(
            profile_id=chosen,
            think_text=parser.think_text,
            answer_text=parser.answer_text.strip(),
            stopped_by_repetition=stopped,
            elapsed_seconds=time.monotonic() - started,
            notices=notices,
        )


# =============================================================================
# BỘ KIỂM THỬ TÍCH HỢP (SELF-CONTAINED)
# =============================================================================

class _FakeOllamaClient(OllamaClient):
    """Ollama giả lập: ghi lại payload, không gọi mạng."""

    def __init__(self) -> None:
        super().__init__("http://127.0.0.1:1")
        self.posted: list[tuple[str, dict[str, Any]]] = []
        self.stream_pieces: list[str] = []

    def _post_json(self, endpoint: str, payload: dict[str, Any], timeout_s: float | None = None) -> dict[str, Any]:
        self.posted.append((endpoint, payload))
        return {}

    def _get_json(self, endpoint: str, timeout_s: float = 5.0) -> dict[str, Any]:
        raise LocalAIError("Ollama giả lập không chạy.")

    def stream_generate(self, model_name: str, prompt: str, **kwargs: Any) -> Iterator[str]:
        yield from self.stream_pieces


class TestPathsOnDrive(unittest.TestCase):
    """Kiểm tra việc tạo và phát hiện đường dẫn."""

    def test_default_constants_point_to_drive_d(self) -> None:
        self.assertEqual(DEFAULT_MODELS_ROOT, r"D:\AI DATA\STEM_APP\models")
        default_paths = AIPaths()
        self.assertTrue(str(default_paths.ollama_dir).endswith("ollama"))
        self.assertTrue(str(default_paths.gguf_dir).endswith("gguf"))
        self.assertTrue(str(default_paths.api_key_file).endswith("gemini_api_key.txt"))

    def test_create_and_detect_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = AIPaths(Path(temp_dir) / "models")
            before = paths.detect_layout()
            self.assertFalse(before["ollama_dir"])
            self.assertTrue(paths.ensure_directories())
            after = paths.detect_layout()
            self.assertTrue(after["models_root"])
            self.assertTrue(after["ollama_dir"])
            self.assertTrue(after["gguf_dir"])
            self.assertFalse(after["api_key_file"])

    def test_manager_sets_ollama_models_env(self) -> None:
        old_value = os.environ.get("OLLAMA_MODELS")
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                paths = AIPaths(Path(temp_dir) / "models")
                manager = AILocalManager(paths=paths, ollama_client=_FakeOllamaClient())
                self.assertEqual(os.environ["OLLAMA_MODELS"], str(paths.ollama_dir))
                manager.shutdown()
        finally:
            if old_value is None:
                os.environ.pop("OLLAMA_MODELS", None)
            else:
                os.environ["OLLAMA_MODELS"] = old_value

    def test_find_gguf_prefers_r1(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = AIPaths(Path(temp_dir) / "models")
            paths.ensure_directories()
            (paths.gguf_dir / "other-1.5b-q4.gguf").write_bytes(b"x")
            (paths.gguf_dir / "DeepSeek-R1-Distill-1.5B-Q4.gguf").write_bytes(b"x")
            found = paths.find_gguf("1.5b")
            self.assertIsNotNone(found)
            assert found is not None
            self.assertIn("R1", found.name)
            self.assertIsNone(paths.find_gguf("7b"))


class TestExoticFilter(unittest.TestCase):
    """Kiểm tra bộ lọc chữ Hán, Ả Rập, Kirin."""

    def test_filter_removes_cjk_arabic_cyrillic(self) -> None:
        dirty = "Tam giác 三角形 đều مرحبا có cạnh Привет bằng 5."
        clean = _filter_exotic_scripts(dirty)
        self.assertNotRegex(clean, r"[\u4e00-\u9fff]")
        self.assertNotRegex(clean, r"[\u0600-\u06ff]")
        self.assertNotRegex(clean, r"[\u0400-\u04ff]")
        self.assertIn("Tam giác", clean)
        self.assertIn("đều", clean)
        self.assertIn("cạnh", clean)

    def test_filter_keeps_vietnamese(self) -> None:
        text = "Diện tích hình thang cân: S = (a + b) × h / 2 ≈ 12,5 cm²"
        self.assertEqual(_filter_exotic_scripts(text), text)


class TestRepetitionBreaker(unittest.TestCase):
    """Kiểm tra bộ ngắt chuỗi lặp."""

    def test_detects_zero_loop(self) -> None:
        breaker = RepetitionBreaker()
        triggered = False
        for _ in range(40):
            if breaker.feed(",000"):
                triggered = True
                break
        self.assertTrue(triggered)

    def test_detects_long_zero_run(self) -> None:
        breaker = RepetitionBreaker()
        self.assertTrue(breaker.feed("Kết quả là 1" + "0" * 60))

    def test_detects_repeated_sentence(self) -> None:
        breaker = RepetitionBreaker()
        sentence = "Vậy diện tích tam giác ABC bằng một nửa tích đáy và chiều cao. "
        triggered = False
        for _ in range(6):
            if breaker.feed(sentence):
                triggered = True
                break
        self.assertTrue(triggered)

    def test_detects_repeated_lines(self) -> None:
        breaker = RepetitionBreaker()
        triggered = False
        for _ in range(6):
            if breaker.feed("Bước tiếp theo là tính\n"):
                triggered = True
                break
        self.assertTrue(triggered)

    def test_normal_text_not_triggered(self) -> None:
        breaker = RepetitionBreaker()
        text = (
            "Cho tam giác ABC đều cạnh 6. Gọi H là chân đường cao hạ từ A xuống BC. "
            "Khi đó AH = 3√3 và diện tích tam giác bằng 9√3. "
            "Tiếp theo, ta xét hình thang cân ABCD với hai đáy AB = 4 và CD = 10."
        )
        self.assertFalse(breaker.feed(text))
        self.assertFalse(breaker.triggered)

    def test_reset(self) -> None:
        breaker = RepetitionBreaker()
        breaker.feed("0" * 80)
        self.assertTrue(breaker.triggered)
        breaker.reset()
        self.assertFalse(breaker.triggered)
        self.assertFalse(breaker.feed("Xin chào"))


class TestThinkParser(unittest.TestCase):
    """Kiểm tra tách luồng <think>, kể cả khi thẻ bị cắt giữa các chunk."""

    def test_split_tags_across_chunks(self) -> None:
        parser = ThinkParser()
        chunks = ["<thi", "nk>suy ngh", "ĩ</th", "ink>Đáp ", "án"]
        events: list[tuple[str, str]] = []
        for chunk in chunks:
            events.extend(parser.feed(chunk))
        events.extend(parser.flush())
        self.assertEqual(parser.think_text, "suy nghĩ")
        self.assertEqual(parser.answer_text, "Đáp án")
        for kind, text in events:
            self.assertNotIn("<", text)
            self.assertIn(kind, ("think", "answer"))

    def test_tag_in_single_chunk(self) -> None:
        parser = ThinkParser()
        parser.feed("<think>a</think>b")
        parser.flush()
        self.assertEqual(parser.think_text, "a")
        self.assertEqual(parser.answer_text, "b")

    def test_char_by_char(self) -> None:
        parser = ThinkParser()
        for character in "<think>x</think>y":
            parser.feed(character)
        parser.flush()
        self.assertEqual(parser.think_text, "x")
        self.assertEqual(parser.answer_text, "y")

    def test_lone_angle_bracket_is_preserved(self) -> None:
        parser = ThinkParser()
        parser.feed("a < b")
        parser.flush()
        self.assertEqual(parser.answer_text, "a < b")

    def test_start_in_think(self) -> None:
        parser = ThinkParser(start_in_think=True)
        parser.feed("nghĩ</think>nói")
        parser.flush()
        self.assertEqual(parser.think_text, "nghĩ")
        self.assertEqual(parser.answer_text, "nói")


class TestGeminiKeyStore(unittest.TestCase):
    """Kiểm tra đọc/lưu gemini_api_key.txt."""

    def test_save_and_read(self) -> None:
        old_env = os.environ.pop("GEMINI_API_KEY", None)
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                paths = AIPaths(Path(temp_dir) / "models")
                store = GeminiKeyStore(paths.api_key_file)
                self.assertIsNone(store.read())
                store.save("  KHOA-API-THU-NGHIEM  \n")
                self.assertTrue(paths.api_key_file.is_file())
                self.assertEqual(store.read(), "KHOA-API-THU-NGHIEM")
        finally:
            if old_env is not None:
                os.environ["GEMINI_API_KEY"] = old_env

    def test_empty_key_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = GeminiKeyStore(Path(temp_dir) / "key.txt")
            with self.assertRaises(ValueError):
                store.save("   ")


class TestManagerBehaviour(unittest.TestCase):
    """Kiểm tra hành vi tổng thể của trình quản lý."""

    def _make_manager(self, temp_dir: str) -> tuple[AILocalManager, _FakeOllamaClient]:
        fake = _FakeOllamaClient()
        manager = AILocalManager(
            paths=AIPaths(Path(temp_dir) / "models"),
            configure_env=False,
            ollama_client=fake,
            idle_timeout_s=3600.0,
        )
        return manager, fake

    def test_unload_payload_uses_keep_alive_zero(self) -> None:
        fake = _FakeOllamaClient()
        payload = fake.build_unload_payload("deepseek-r1:7b")
        self.assertEqual(payload["keep_alive"], 0)
        self.assertEqual(payload["model"], "deepseek-r1:7b")
        self.assertTrue(fake.unload_model("deepseek-r1:7b"))
        self.assertEqual(fake.posted[0][0], "/api/generate")
        self.assertEqual(fake.posted[0][1]["keep_alive"], 0)

    def test_profile_zero_is_pure_python(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manager, _ = self._make_manager(temp_dir)
            context = GeometryProblemContext(
                problem_text="Cho tam giác đều ABC cạnh 2.",
                ground_truth_points=[("A", 0.0, 0.0), ("B", 2.0, 0.0), ("C", 1.0, 1.7320508)],
                ground_truth_areas=[("S_ABC", 1.7320508)],
                special_shapes=["Tam giác đều"],
            )
            result = manager.explain(context, profile_id=0)
            self.assertEqual(result.profile_id, 0)
            self.assertIn("Tam giác đều", result.answer_text)
            self.assertIn("1.7321", result.answer_text)
            manager.shutdown()

    def test_switch_profile_unloads_previous_model(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manager, fake = self._make_manager(temp_dir)
            manager._loaded_ollama_models.add("deepseek-r1:7b")
            notices = manager.switch_profile(3)
            self.assertTrue(any("deepseek-r1:7b" in item for item in notices))
            self.assertEqual(fake.posted[0][1]["keep_alive"], 0)
            self.assertNotIn("deepseek-r1:7b", manager._loaded_ollama_models)
            manager.shutdown()

    def test_pipeline_filters_and_parses(self) -> None:
        parser = ThinkParser()
        breaker = RepetitionBreaker()
        events: list[tuple[str, str]] = []
        stopped = AILocalManager.process_stream(
            ["<think>Xét 三角形 ", "ABC</think>Kết quả: ", "diện tích 9 Привет"],
            parser,
            breaker,
            lambda kind, text: events.append((kind, text)),
        )
        self.assertFalse(stopped)
        self.assertEqual(parser.think_text, "Xét  ABC")
        self.assertEqual(parser.answer_text, "Kết quả: diện tích 9 ")

    def test_pipeline_stops_on_repetition(self) -> None:
        parser = ThinkParser()
        breaker = RepetitionBreaker()
        stopped = AILocalManager.process_stream(
            ["Kết quả là 1"] + [",000"] * 50,
            parser,
            breaker,
            None,
        )
        self.assertTrue(stopped)

    def test_prompt_contains_ground_truth(self) -> None:
        context = GeometryProblemContext(
            problem_text="Tính diện tích.",
            ground_truth_points=[("A", 1.0, 2.0)],
            ground_truth_areas=[("S", 3.5)],
            special_shapes=["Tam giác vuông"],
        )
        prompt = AILocalManager.build_prompt(context)
        self.assertIn("A(1.0000; 2.0000)", prompt)
        self.assertIn("S = 3.5000", prompt)
        self.assertIn("Tam giác vuông", prompt)

    def test_explain_via_fake_ollama_profile_three(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manager, fake = self._make_manager(temp_dir)
            fake.stream_pieces = ["<think>nghĩ</think>", "Đáp án 42"]
            manager.paths.ensure_directories()
            (manager.paths.gguf_dir / "x-r1-1.5b.gguf").write_bytes(b"x")
            # Ollama giả lập báo không chạy => đi nhánh GGUF => cần llama_cpp; kiểm tra lỗi rõ ràng.
            context = GeometryProblemContext(problem_text="Test")
            if "llama_cpp" in sys.modules:
                self.skipTest("llama_cpp có sẵn, bỏ qua kiểm thử nhánh lỗi.")
            try:
                manager.explain(context, profile_id=3)
            except LocalAIError as error:
                self.assertIn("llama", str(error).lower())
            manager.shutdown()


if __name__ == "__main__":
    unittest.main(verbosity=2)
