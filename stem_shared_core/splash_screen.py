# -*- coding: utf-8 -*-
"""
splash_screen.py
================
Màn hình chờ (Splash Screen) phong cách tối giản chuẩn Antigravity / TLabtool:
- Cửa sổ không viền (frameless), căn giữa màn hình.
- Nền tối tinh tế (#0F172A).
- Biểu tượng màu xám bạc đơn sắc (Monochrome Grayscale Logo) hiện ra nhẹ nhàng (Smooth Fade-in).
- Phía dưới là chữ nhỏ "TLabtool" nhận diện thương hiệu.
- Thanh tiến trình siêu mảnh tối giản.
- Kiểm soát thời gian hiển thị tối thiểu 2.0s - 2.5s. Nếu app khởi động lâu hơn sẽ giữ màn hình chờ,
  khi app sẵn sàng sẽ chuyển cảnh mượt mà (Smooth Fade-out) vào giao diện chính.
"""

from __future__ import annotations
import os
import sys
import time
import tkinter as tk
from typing import Optional, Callable
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageEnhance

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CORE_DIR, "assets")


class TLabtoolSplashScreen:
    """
    Quản lý màn hình khởi động mượt mà cho các ứng dụng hệ sinh thái STEM TLabtool.
    """
    def __init__(
        self,
        master: tk.Tk | tk.Toplevel,
        app_id: str,
        app_title: str = "TLabtool STEM Studio",
        min_duration: float = 2.2,
        custom_logo_path: Optional[str] = None,
        on_ready_callback: Optional[Callable[[], None]] = None
    ):
        self.master = master
        self.app_id = app_id
        self.app_title = app_title
        self.min_duration = min_duration
        self.on_ready_callback = on_ready_callback
        self.is_app_ready = False
        self.start_time = time.time()
        self._closing = False
        self._anim_timer = None
        self._check_timer = None
        self._fade_timer = None

        # Đặt biểu tượng .ico và iconphoto mặc định toàn diện cho master window và toàn bộ hộp thoại con (Toplevel)
        ico_path = os.path.join(ASSETS_DIR, f"{app_id}.ico")
        if not os.path.exists(ico_path):
            app_assets = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets")
            cand_ico = os.path.join(app_assets, f"{app_id}.ico")
            if os.path.exists(cand_ico):
                ico_path = cand_ico

        if os.path.exists(ico_path):
            try:
                self.master.iconbitmap(default=ico_path)
                self.master.iconbitmap(ico_path)
            except Exception:
                try:
                    self.master.iconbitmap(ico_path)
                except Exception:
                    pass
            self.master.ico_path = ico_path

        # Đặt iconphoto(True, ...) để mọi Toplevel/Dialog con kế thừa tự động logo của ứng dụng
        png_path = os.path.join(ASSETS_DIR, f"{app_id}_logo.png")
        if not os.path.exists(png_path):
            app_assets = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets")
            cand_png = os.path.join(app_assets, f"{app_id}_logo.png")
            if os.path.exists(cand_png):
                png_path = cand_png

        if os.path.exists(png_path):
            try:
                pil_ico = Image.open(png_path).convert("RGBA")
                pil_ico = pil_ico.resize((64, 64), Image.Resampling.LANCZOS)
                self.master._app_icon_photo = ImageTk.PhotoImage(pil_ico, master=self.master)
                self.master.iconphoto(True, self.master._app_icon_photo)
            except Exception:
                pass

        # Tạo cửa sổ splash dạng Toplevel không viền phong cách Cursor / Antigravity nền sáng
        self.splash = tk.Toplevel(self.master)
        self.splash.title(f"{app_title} - Loading")
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#F8FAFC")

        # Đặt kích thước 360 x 310 px
        self.width = 360
        self.height = 310
        sw = self.splash.winfo_screenwidth()
        sh = self.splash.winfo_screenheight()
        x = max(0, (sw - self.width) // 2)
        y = max(0, (sh - self.height) // 2)
        self.splash.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.splash.attributes("-topmost", True)

        # Hỗ trợ fade-in trên Windows
        self.alpha = 0.0
        try:
            self.splash.attributes("-alpha", self.alpha)
        except Exception:
            pass

        # Tìm logo grayscale phù hợp (ưu tiên các phiên bản sắc nét v2 mới nhất)
        if custom_logo_path and os.path.exists(custom_logo_path):
            self.logo_path = custom_logo_path
        else:
            app_dirs = [
                os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", app_id, "assets"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f"{app_id}_v2", "assets"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geosolver", "assets"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phys_solver", "assets"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geosolver_3d", "assets"),
                ASSETS_DIR,
            ]
            candidates = []
            for ad in app_dirs:
                if os.path.exists(ad):
                    candidates.extend([
                        os.path.join(ad, f"{app_id}_logo_gray_v2_150x150.png"),
                        os.path.join(ad, f"{app_id}_logo_gray_v2_300x300.png"),
                        os.path.join(ad, f"{app_id}_logo_gray.png"),
                        os.path.join(ad, f"{app_id}_logo.png"),
                        os.path.join(ad, "icon_256.png"),
                        os.path.join(ad, "Square150x150Logo.png"),
                    ])
            self.logo_path = next((c for c in candidates if os.path.exists(c)), None)

        self._build_ui()
        self._fade_in()

    def _build_ui(self):
        # Khung viền thanh lịch chuẩn Cursor / Antigravity
        container = tk.Frame(
            self.splash,
            bg="#FFFFFF",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        container.pack(fill=tk.BOTH, expand=True)

        # 1. Logo màu xám ở giữa nổi bật trên nền sáng
        self.logo_img = None
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                pil_img = Image.open(self.logo_path).convert("RGBA")
                pil_img = pil_img.resize((115, 115), Image.Resampling.LANCZOS)
                # Tinh chỉnh vi tương phản & độ sắc nét khi hiển thị trên giao diện Tkinter
                r, g, b, a = pil_img.split()
                rgb = Image.merge("RGB", (r, g, b)).filter(
                    ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=1)
                )
                pil_img = Image.merge("RGBA", (*rgb.split(), a))
                self.logo_img = ImageTk.PhotoImage(pil_img, master=self.splash)
                lbl_logo = tk.Label(container, image=self.logo_img, bg="#FFFFFF")
                lbl_logo.pack(pady=(45, 10))
            except Exception as ex:
                print(f"[SPLASH WARNING] Không thể nạp ảnh logo ({self.logo_path}): {ex}")

        if not self.logo_img:
            # Spacing nếu ảnh chưa sẵn sàng (tuyệt đối không hiển thị ký tự lạ hình thoi)
            spacer = tk.Frame(container, bg="#FFFFFF", height=115, width=115)
            spacer.pack(pady=(45, 10))
            spacer.pack_propagate(False)

        # 2. Tên nhận diện thương hiệu "TLabtool"
        lbl_brand = tk.Label(
            container,
            text="TLabtool",
            font=("Segoe UI", 10, "bold"),
            fg="#1E293B", # Đen Slate 800 thanh lịch
            bg="#FFFFFF"
        )
        lbl_brand.pack(pady=(0, 2))

        # 3. Tiêu đề ứng dụng tinh gọn
        lbl_sub = tk.Label(
            container,
            text=self.app_title.upper(),
            font=("Segoe UI", 8, "normal"),
            fg="#64748B", # Muted Slate 500
            bg="#FFFFFF"
        )
        lbl_sub.pack(pady=(0, 20))

        # 4. Thanh tiến trình mỏng 2px tối giản
        prog_bar_frame = tk.Frame(container, bg="#F1F5F9", height=2, width=150)
        prog_bar_frame.pack()
        prog_bar_frame.pack_propagate(False)

        self.indicator = tk.Frame(prog_bar_frame, bg="#0969DA", height=2, width=38)
        self.indicator.place(x=0, y=0)
        self._anim_pos = 0
        self._anim_dir = 3
        self._animate_indicator()

    def _animate_indicator(self):
        """Hoạt ảnh chuyển động nhẹ của thanh tiến trình."""
        if self._closing:
            return
        try:
            if not self.splash.winfo_exists():
                return
            self._anim_pos += self._anim_dir
            if self._anim_pos > 112:
                self._anim_dir = -3
            elif self._anim_pos < 0:
                self._anim_dir = 3
            self.indicator.place(x=self._anim_pos, y=0)
            self._anim_timer = self.splash.after(25, self._animate_indicator)
        except Exception:
            pass

    def _fade_in(self):
        """Hiệu ứng hiện ra nhẹ nhàng (Smooth Fade-in)."""
        if self._closing:
            return
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + 0.1)
            try:
                if not self.splash.winfo_exists():
                    return
                self.splash.attributes("-alpha", self.alpha)
                self.splash.update_idletasks()
                self._fade_timer = self.splash.after(16, self._fade_in)
            except Exception:
                pass
        else:
            self._check_transition()

    def _check_transition(self):
        """Kiểm tra điều kiện chuyển từ màn hình chờ vào ứng dụng chính."""
        if self._closing:
            return
        try:
            if not self.splash.winfo_exists():
                return
            elapsed = time.time() - self.start_time
            if self.is_app_ready and elapsed >= self.min_duration:
                self._fade_out()
            else:
                self._check_timer = self.splash.after(60, self._check_transition)
        except Exception:
            pass

    def set_app_ready(self):
        """Được ứng dụng chính gọi khi đã nạp xong toàn bộ dữ liệu và giao diện."""
        self.is_app_ready = True

    def _fade_out(self):
        """Hiệu ứng biến mất nhẹ nhàng (Smooth Fade-out)."""
        self._closing = True
        self._do_fade_out()

    def _do_fade_out(self):
        try:
            if not self.splash.winfo_exists():
                self._finish_close()
                return
            if self.alpha > 0.0:
                self.alpha = max(0.0, self.alpha - 0.15)
                self.splash.attributes("-alpha", self.alpha)
                self.splash.update_idletasks()
                self._fade_timer = self.splash.after(16, self._do_fade_out)
            else:
                self._finish_close()
        except Exception:
            self._finish_close()

    def _finish_close(self):
        self._closing = True
        for timer in (self._anim_timer, self._check_timer, self._fade_timer):
            if timer and self.splash:
                try:
                    self.splash.after_cancel(timer)
                except Exception:
                    pass
        try:
            if self.splash.winfo_exists():
                self.splash.destroy()
        except Exception:
            pass
        if self.on_ready_callback:
            try:
                self.on_ready_callback()
            except Exception as e:
                pass


def attach_splash_screen(
    master: tk.Tk | tk.Toplevel,
    app_id: str,
    app_title: str = "TLabtool STEM Studio",
    min_duration: float = 2.2,
    custom_logo_path: Optional[str] = None
) -> TLabtoolSplashScreen:
    """
    Gắn màn hình chờ TLabtool Grayscale vào một ứng dụng Tkinter:
    1. Ẩn master window (withdraw).
    2. Hiển thị màn hình chờ Splash không viền với logo xám bạc.
    3. Trả về đối tượng splash để gọi `splash.set_app_ready()` khi nạp xong.
    4. Tự động hiển thị (deiconify) master window khi hoàn tất.
    """
    master.withdraw()

    def on_ready():
        master.deiconify()
        master.lift()
        master.focus_force()

    splash = TLabtoolSplashScreen(
        master=master,
        app_id=app_id,
        app_title=app_title,
        min_duration=min_duration,
        custom_logo_path=custom_logo_path,
        on_ready_callback=on_ready
    )
    return splash
