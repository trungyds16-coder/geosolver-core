# -*- coding: utf-8 -*-
"""
stem_shared_core.i18n - Hệ thống đa ngôn ngữ tập trung cho các app STEM.

Dùng nhanh:
    from stem_shared_core.i18n import t, set_language, get_language
    set_language("en")
    t("cad.x_range", xmin=-5, xmax=5)      # "x range: [-5, 5]"
    t("geo.point", lang="vi")               # "Điểm"

Quy ước:
  * Key dạng phẳng "nhóm.khóa" (file JSON có thể lồng nhau, sẽ được làm phẳng).
  * Thiếu key ở ngôn ngữ hiện tại -> thử tiếng Anh -> trả về chính key.
  * Chỉ gọi str.format khi có kwargs; khi đó dùng {{ và }} cho dấu ngoặc nhọn thật.
  * Ngôn ngữ người dùng lưu ở %LOCALAPPDATA%\\AIMathHub\\config.json (khóa "language").
"""
from __future__ import annotations

import json
import logging
import os
import threading
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

__all__ = ["I18nManager", "get_i18n", "t", "set_language", "get_language"]

log = logging.getLogger("stem.i18n")

_LOCALES_DIR = Path(__file__).resolve().parent / "locales"
_TERMS_FILE = "math_terms.json"


def _default_config_path() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    root = Path(base) if base else Path.home() / ".local" / "share"
    return root / "AIMathHub" / "config.json"


def _flatten(data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in data.items():
        if k.startswith("_") and not prefix:  # bỏ "_meta"
            continue
        key = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        else:
            out[key] = v
    return out


def _fold(text: str) -> str:
    """Chuẩn hóa để tra cứu: bỏ dấu tiếng Việt, hạ chữ thường, gọn khoảng trắng."""
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.lower().split())


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


class I18nManager:
    DEFAULT_LANG = "vi"
    FALLBACK_LANG = "en"

    _instance: Optional["I18nManager"] = None
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls) -> "I18nManager":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __init__(
        self,
        locales_dir: Optional[os.PathLike] = None,
        config_path: Optional[os.PathLike] = None,
        default_lang: Optional[str] = None,
    ) -> None:
        self._lock = threading.RLock()
        self._save_lock = threading.Lock()  # tuần tự hóa việc ghi config
        self._locales_dir = Path(locales_dir) if locales_dir else _LOCALES_DIR
        self._config_path = Path(config_path) if config_path else _default_config_path()
        self._catalog: Dict[str, Dict[str, Any]] = {}
        self._terms: Optional[Tuple[List[dict], Dict[str, Dict[str, dict]]]] = None
        self._listeners: List[Callable[[str], None]] = []
        self._warned: set = set()
        self.reload()
        self._lang = (
            self._normalize(self._load_saved_language())
            or self._normalize(default_lang)
            or self._normalize(self.DEFAULT_LANG)
            or self.FALLBACK_LANG
        )

    # ------------------------------------------------------------------ load
    def reload(self) -> None:
        """Đọc lại toàn bộ file *.json trong thư mục locales (trừ math_terms.json)."""
        catalog: Dict[str, Dict[str, Any]] = {}
        if self._locales_dir.is_dir():
            for path in sorted(self._locales_dir.glob("*.json")):
                if path.name == _TERMS_FILE:
                    continue
                try:
                    with open(path, "r", encoding="utf-8") as fh:
                        catalog[path.stem.lower()] = _flatten(json.load(fh))
                except (OSError, ValueError) as exc:
                    log.error("Không đọc được locale %s: %s", path, exc)
        with self._lock:
            # giữ lại các bản dịch đăng ký thêm lúc chạy
            for lang, extra in getattr(self, "_runtime", {}).items():
                catalog.setdefault(lang, {}).update(extra)
            self._catalog = catalog
            self._terms = None
            self._warned.clear()

    def register_translations(self, lang: str, mapping: Dict[str, Any]) -> None:
        """Cho app con bổ sung/ghi đè key lúc chạy (không ghi ra file)."""
        flat = _flatten(mapping)
        with self._lock:
            self._runtime = getattr(self, "_runtime", {})
            self._runtime.setdefault(lang.lower(), {}).update(flat)
            self._catalog.setdefault(lang.lower(), {}).update(flat)

    # ---------------------------------------------------------------- config
    def _load_saved_language(self) -> Optional[str]:
        try:
            with open(self._config_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            value = data.get("language")
            return value if isinstance(value, str) else None
        except (OSError, ValueError, AttributeError):
            return None

    def _save_language(self, lang: str) -> None:
        with self._save_lock:
            try:
                self._config_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with open(self._config_path, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                    if not isinstance(data, dict):
                        data = {}
                except (OSError, ValueError):
                    data = {}
                data["language"] = lang
                tmp = self._config_path.with_name(
                    f"{self._config_path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
                with open(tmp, "w", encoding="utf-8") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
                os.replace(tmp, self._config_path)
            except OSError as exc:
                log.warning("Không lưu được cấu hình ngôn ngữ: %s", exc)

    # -------------------------------------------------------------- language
    def _normalize(self, code: Optional[str]) -> Optional[str]:
        if not code:
            return None
        short = code.strip().lower().replace("_", "-").split("-")[0]
        with self._lock:
            return short if short in self._catalog else None

    def supported_languages(self) -> List[str]:
        with self._lock:
            return sorted(self._catalog)

    def get_language(self) -> str:
        with self._lock:
            return self._lang

    def set_language(self, lang_code: str, persist: bool = True) -> bool:
        """Đổi ngôn ngữ. Trả về False nếu ngôn ngữ không được hỗ trợ."""
        lang = self._normalize(lang_code)
        if lang is None:
            log.warning("Ngôn ngữ không hỗ trợ: %r", lang_code)
            return False
        with self._lock:
            changed = lang != self._lang
            self._lang = lang
            listeners = list(self._listeners)
        if persist:
            self._save_language(lang)
        if changed:
            for cb in listeners:  # gọi ngoài lock để tránh deadlock
                try:
                    cb(lang)
                except Exception:  # noqa: BLE001
                    log.exception("Lỗi trong callback đổi ngôn ngữ")
        return True

    def on_language_changed(self, callback: Callable[[str], None]) -> None:
        """Đăng ký hàm được gọi khi ngôn ngữ đổi (để UI tự làm mới nhãn)."""
        with self._lock:
            if callback not in self._listeners:
                self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[str], None]) -> None:
        with self._lock:
            if callback in self._listeners:
                self._listeners.remove(callback)

    # ------------------------------------------------------------ translate
    def t(self, key: str, lang: Optional[str] = None, **kwargs: Any) -> Any:
        with self._lock:
            lang = (self._normalize(lang) if lang else None) or self._lang
            value = self._catalog.get(lang, {}).get(key)
            if value is None and lang != self.FALLBACK_LANG:
                value = self._catalog.get(self.FALLBACK_LANG, {}).get(key)
                if value is not None:
                    self._warn_once(("fallback", lang, key), "Thiếu key '%s' ở '%s', dùng tiếng Anh", key, lang)
            if value is None:
                self._warn_once(("missing", key), "Thiếu key '%s' ở mọi ngôn ngữ", key)
                value = key
        if kwargs and isinstance(value, str):
            try:
                return value.format_map(_SafeDict(kwargs))
            except (ValueError, IndexError, KeyError, AttributeError):
                return value
        return value

    def has_key(self, key: str, lang: Optional[str] = None) -> bool:
        with self._lock:
            return key in self._catalog.get(lang or self._lang, {})

    def _warn_once(self, token: tuple, msg: str, *args: Any) -> None:
        if token not in self._warned:
            self._warned.add(token)
            log.warning(msg, *args)

    # ------------------------------------------------------------ math terms
    def _load_terms(self) -> Tuple[List[dict], Dict[str, Dict[str, dict]]]:
        with self._lock:
            if self._terms is not None:
                return self._terms
            entries: List[dict] = []
            try:
                with open(self._locales_dir / _TERMS_FILE, "r", encoding="utf-8") as fh:
                    entries = list(json.load(fh).get("terms", []))
            except (OSError, ValueError) as exc:
                log.error("Không đọc được %s: %s", _TERMS_FILE, exc)
            index: Dict[str, Dict[str, dict]] = {"en": {}, "vi": {}}
            for entry in entries:
                for lg in ("en", "vi"):
                    text = entry.get(lg)
                    if text:
                        index[lg].setdefault(_fold(text), entry)
            self._terms = (entries, index)
            return self._terms

    def translate_term(self, text: str, to_lang: Optional[str] = None) -> Optional[str]:
        """Tra thuật ngữ. Tự nhận ra ngôn ngữ nguồn; trả None nếu không có."""
        _, index = self._load_terms()
        key = _fold(text)
        for src, dst in (("en", "vi"), ("vi", "en")):
            entry = index[src].get(key)
            if entry:
                return entry.get(to_lang or dst)
        return None

    def search_terms(self, query: str, limit: int = 10) -> List[dict]:
        """Tìm gần đúng (chứa chuỗi, không phân biệt dấu) theo cả Anh lẫn Việt."""
        entries, _ = self._load_terms()
        q = _fold(query)
        if not q:
            return []
        starts, contains = [], []
        for e in entries:
            hay = [_fold(e.get("en", "")), _fold(e.get("vi", ""))]
            if any(h.startswith(q) for h in hay):
                starts.append(e)
            elif any(q in h for h in hay):
                contains.append(e)
        return (starts + contains)[:limit]


# ----------------------------------------------------------- module helpers
def get_i18n() -> I18nManager:
    return I18nManager.instance()


def t(key: str, lang: Optional[str] = None, **kwargs: Any) -> Any:
    return get_i18n().t(key, lang, **kwargs)


def set_language(lang_code: str, persist: bool = True) -> bool:
    return get_i18n().set_language(lang_code, persist)


def get_language() -> str:
    return get_i18n().get_language()
