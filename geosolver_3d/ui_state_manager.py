# -*- coding: utf-8 -*-
"""
ui_state_manager.py
===================
Bộ quản lý lưu trữ & phục hồi trạng thái giao diện (Window Geometry & Tab Memory Manager)
cho GeoSolver 3D và các ứng dụng STEM:
- Ghi nhớ kích thước cửa sổ (geometry: width x height + x + y) và vị trí kéo thả
- Ghi nhớ tab đang kích hoạt (active tab) cho các hộp thoại
- Tự động chống tràn màn hình (off-screen clamping)
- Tương thích chuẩn JSON, tự động lưu khi đóng cửa sổ hoặc chuyển tab.
"""

from __future__ import annotations
import json
import os
import re
import tkinter as tk
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class UIStateManager:
    """
    Quản lý lưu trữ và phục hồi trạng thái giao diện người dùng (Geometry & Tab Persistence).
    """

    _DEFAULT_CONFIG_FILENAME = "ui_preferences.json"
    _memory_cache: Dict[str, Dict[str, Any]] = {}
    _config_path: Optional[Path] = None

    @classmethod
    def set_config_path(cls, path: Path | str) -> None:
        """Thiết lập đường dẫn file cấu hình json tùy chỉnh."""
        cls._config_path = Path(path).resolve()
        cls._memory_cache.clear()

    @classmethod
    def get_config_path(cls) -> Path:
        """Lấy đường dẫn file cấu hình JSON hiện tại."""
        if cls._config_path is not None:
            return cls._config_path

        # Ưu tiên thư mục của app hiện tại
        app_dir = Path(__file__).resolve().parent
        cls._config_path = app_dir / cls._DEFAULT_CONFIG_FILENAME
        return cls._config_path

    @classmethod
    def _load_all(cls) -> Dict[str, Dict[str, Any]]:
        """Đọc toàn bộ cấu hình từ file JSON (có cache trong bộ nhớ)."""
        if cls._memory_cache:
            return cls._memory_cache

        cfg_file = cls.get_config_path()
        if cfg_file.is_file():
            try:
                with open(cfg_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        cls._memory_cache = data
                        return cls._memory_cache
            except Exception:
                pass
        cls._memory_cache = {}
        return cls._memory_cache

    @classmethod
    def _save_all(cls) -> None:
        """Ghi toàn bộ cấu hình từ bộ nhớ ra file JSON an toàn."""
        cfg_file = cls.get_config_path()
        try:
            cfg_file.parent.mkdir(parents=True, exist_ok=True)
            temp_file = cfg_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(cls._memory_cache, f, indent=2, ensure_ascii=False)
            if temp_file.is_file():
                temp_file.replace(cfg_file)
        except Exception:
            pass

    @classmethod
    def get_state(cls, window_key: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Lấy toàn bộ từ điển trạng thái của một cửa sổ."""
        all_data = cls._load_all()
        val = all_data.get(window_key)
        if isinstance(val, dict):
            return dict(val)
        return dict(default) if default else {}

    @classmethod
    def save_state(cls, window_key: str, **kwargs: Any) -> None:
        """Lưu các trường trạng thái cho một cửa sổ."""
        all_data = cls._load_all()
        if window_key not in all_data or not isinstance(all_data[window_key], dict):
            all_data[window_key] = {}
        all_data[window_key].update(kwargs)
        cls._memory_cache = all_data
        cls._save_all()

    @classmethod
    def get_window_geometry(cls, window_key: str, default: str = "") -> str:
        """Lấy chuỗi geometry đã lưu của một cửa sổ."""
        state = cls.get_state(window_key)
        return str(state.get("geometry", default))

    @classmethod
    def save_window_geometry(cls, window_key: str, geometry: str) -> None:
        """Lưu chuỗi geometry của một cửa sổ."""
        cls.save_state(window_key, geometry=geometry)

    @classmethod
    def get_active_tab(cls, window_key: str, default: Any = 1) -> Any:
        """Lấy tab đang kích hoạt của một cửa sổ."""
        state = cls.get_state(window_key)
        return state.get("active_tab", default)

    @classmethod
    def save_active_tab(cls, window_key: str, active_tab: Any) -> None:
        """Lưu tab đang kích hoạt của một cửa sổ."""
        cls.save_state(window_key, active_tab=active_tab)

    @staticmethod
    def parse_geometry(geom_str: str) -> Optional[Tuple[int, int, Optional[int], Optional[int]]]:
        """
        Phân tích chuỗi geometry dạng 'WIDTHxHEIGHT+X+Y' hoặc 'WIDTHxHEIGHT'.
        Trả về (width, height, x, y).
        """
        if not geom_str:
            return None
        match = re.match(r"^(\d+)x(\d+)(?:([+-]\d+)([+-]\d+))?$", geom_str.strip())
        if not match:
            return None
        w = int(match.group(1))
        h = int(match.group(2))
        x = int(match.group(3)) if match.group(3) is not None else None
        y = int(match.group(4)) if match.group(4) is not None else None
        return (w, h, x, y)

    @classmethod
    def restore_window(
        cls,
        window: tk.Toplevel | tk.Tk,
        window_key: str,
        default_geometry: str = "700x550",
        min_width: int = 400,
        min_height: int = 300,
    ) -> None:
        """
        Phục hồi kích thước và vị trí cửa sổ an toàn (tự động chống tràn màn hình).
        """
        saved_geom = cls.get_window_geometry(window_key, default_geometry)
        parsed = cls.parse_geometry(saved_geom) or cls.parse_geometry(default_geometry)
        if not parsed:
            window.geometry(default_geometry)
            return

        w, h, x, y = parsed
        w = max(w, min_width)
        h = max(h, min_height)

        try:
            screen_w = window.winfo_screenwidth()
            screen_h = window.winfo_screenheight()
        except Exception:
            screen_w, screen_h = 1920, 1080

        w = min(w, screen_w - 40)
        h = min(h, screen_h - 60)

        if x is not None and y is not None:
            x = max(0, min(x, screen_w - w - 20))
            y = max(0, min(y, screen_h - h - 40))
            final_geom = f"{w}x{h}+{x}+{y}"
        else:
            final_geom = f"{w}x{h}"

        try:
            window.geometry(final_geom)
        except Exception:
            window.geometry(default_geometry)

    @classmethod
    def attach_window_tracking(
        cls,
        window: tk.Toplevel | tk.Tk,
        window_key: str,
        get_extra_state_fn: Optional[Any] = None,
        on_close_callback: Optional[Any] = None,
    ) -> None:
        """
        Tự động theo dõi cửa sổ và lưu trạng thái khi đóng (WM_DELETE_WINDOW).
        """
        def _on_close() -> None:
            try:
                geom = window.geometry()
                extra = get_extra_state_fn() if callable(get_extra_state_fn) else {}
                if not isinstance(extra, dict):
                    extra = {}
                cls.save_state(window_key, geometry=geom, **extra)
            except Exception:
                pass
            if callable(on_close_callback):
                on_close_callback()
            else:
                window.destroy()

        try:
            window.protocol("WM_DELETE_WINDOW", _on_close)
        except Exception:
            pass
