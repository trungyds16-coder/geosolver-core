# -*- coding: utf-8 -*-
"""
GeoSolver 3D CAD - License & In-App Purchase (IAP) Manager
Quản lý trạng thái bản quyền Gói Pro, tích hợp luồng mua hàng Microsoft Store Add-on ($1.99)
và hỗ trợ kích hoạt bản quyền / mã khuyến mãi (Promo Code).
"""

import os
import sys
import json
import hashlib
import platform
import webbrowser
from typing import Tuple, Optional

# Mã Add-on ID mặc định trên Microsoft Partner Center
# Bạn có thể cập nhật ID này sau khi tạo Add-on trên Partner Center
DEFAULT_ADDON_STORE_ID = "9NXXXXXX"
PRODUCT_STORE_ID = "9NXXXXXX" 

_LICENSE_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "TLabtool",
    "GeoSolver3DCAD"
)
_LICENSE_FILE = os.path.join(_LICENSE_DIR, "pro_license.json")
_SALT = "GEOSOLVER_3D_CAD_PRO_SECRET_SALT_2026"


def _generate_signature(email_or_code: str, timestamp_str: str) -> str:
    raw = f"{email_or_code}|{timestamp_str}|{_SALT}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class LicenseManager:
    """Quản lý bản quyền gói Pro và tương tác với Microsoft Store IAP."""

    _is_pro_cached: Optional[bool] = None

    @classmethod
    def get_hardware_id(cls) -> str:
        """Lấy Hardware ID duy nhất của máy tính Windows này."""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            raw = f"{guid}|{platform.node()}"
        except Exception:
            import uuid
            raw = str(uuid.getnode())
        h = hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()
        return f"{h[:4]}-{h[4:8]}-{h[8:12]}"

    @classmethod
    def get_license_dir(cls) -> str:
        os.makedirs(_LICENSE_DIR, exist_ok=True)
        return _LICENSE_DIR

    @classmethod
    def is_pro_active(cls) -> bool:
        """Kiểm tra xem người dùng đã sở hữu gói Pro hay chưa."""
        if cls._is_pro_cached is not None:
            return cls._is_pro_cached

        # Kiểm tra tệp chứng nhận bản quyền nội bộ
        if os.path.exists(_LICENSE_FILE):
            try:
                with open(_LICENSE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                sig = data.get("signature")
                code = data.get("code", "")
                ts = data.get("timestamp", "")
                hw = data.get("hwid", "")
                # Nếu là mã khóa theo máy, kiểm tra lại HWID hiện tại
                if hw and hw != cls.get_hardware_id():
                    cls._is_pro_cached = False
                    return False
                if sig and sig == _generate_signature(code, ts):
                    cls._is_pro_cached = True
                    return True
            except Exception:
                pass

        cls._is_pro_cached = False
        return False

    @classmethod
    def activate_with_code(cls, code: str) -> Tuple[bool, str]:
        """
        Kích hoạt gói Pro bằng mã bản quyền hoặc mã khuyến mại (Promo Code).
        Hỗ trợ:
        1. Mã khóa chặt theo 1 máy tính (Hardware ID): PRO3D-XXXX-YYYY-ZZZZ
        2. Mã Master nội bộ cho nhà phát triển kiểm thử: PRO3D-2026-VIP
        """
        cleaned = code.strip().upper()
        if not cleaned:
            return False, "Vui lòng nhập mã kích hoạt."

        is_valid = False
        current_hw = cls.get_hardware_id()

        # 1. Kiểm tra mã khóa theo Hardware ID 1 máy: PRO3D-LBL4-HASH1-HASH2
        parts = cleaned.split("-")
        if len(parts) == 4 and parts[0] == "PRO3D":
            clean_hw = current_hw.replace("-", "").strip().upper()
            lbl = (parts[1].strip().upper()[:4]).ljust(4, "X")[:4]
            raw = f"{clean_hw}|{lbl}|{_SALT}"
            h = hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()
            if parts[2] == h[:4] and parts[3] == h[4:8]:
                is_valid = True

        # 2. Hỗ trợ mã Master nội bộ
        if cleaned in ["PRO3D-2026-VIP", "GEO3D-PRO-CAD", "TLAB-STEM-2026"]:
            is_valid = True

        if is_valid:
            import time
            ts = str(int(time.time()))
            sig = _generate_signature(cleaned, ts)
            cls.get_license_dir()
            payload = {
                "product": "GeoSolver 3D CAD Pro",
                "code": cleaned,
                "hwid": current_hw,
                "timestamp": ts,
                "signature": sig,
                "status": "activated"
            }
            try:
                with open(_LICENSE_FILE, "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2)
                cls._is_pro_cached = True
                return True, "Kích hoạt Gói Pro thành công! Bản quyền đã được khóa và xác thực trên máy tính này."
            except Exception as ex:
                return False, f"Lỗi lưu trữ tệp bản quyền: {ex}"

        return False, "Mã kích hoạt không hợp lệ hoặc không khớp với phần cứng máy tính này."

    @classmethod
    def open_store_purchase(cls, addon_id: str = "") -> None:
        """
        Kích hoạt giao thức Microsoft Store để mở trang mua Add-on $1.99.
        Sử dụng URI ms-windows-store://
        """
        target_id = addon_id or DEFAULT_ADDON_STORE_ID
        # Nếu đã có Add-on Product ID thực tế: ms-windows-store://purchase/?ProductId=...
        # Hoặc trang PDP (Product Detail Page): ms-windows-store://pdp/?productid=...
        if target_id and target_id != "9NXXXXXX":
            store_uri = f"ms-windows-store://pdp/?productid={target_id}"
        else:
            # Nếu chưa có ID Add-on cụ thể, mở trang tìm kiếm/sản phẩm chính
            store_uri = "ms-windows-store://search/?query=GeoSolver%203D%20CAD"

        try:
            webbrowser.open(store_uri)
        except Exception:
            # Fallback sang web browser
            webbrowser.open("https://apps.microsoft.com")

    @classmethod
    def revoke_license_for_testing(cls) -> None:
        """Thu hồi bản quyền cục bộ (dùng để kiểm thử trạng thái bản Free)."""
        cls._is_pro_cached = None
        if os.path.exists(_LICENSE_FILE):
            try:
                os.remove(_LICENSE_FILE)
            except Exception:
                pass
