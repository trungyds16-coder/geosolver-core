# -*- coding: utf-8 -*-
"""
ai_config_dialog.py
===================
Hộp thoại cấu hình mô hình AI ngoại tuyến tối giản, gọn nhẹ.
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from typing import Optional, Callable


def show_clean_ai_config_dialog(
    parent: tk.Widget,
    ai_hub=None,
    ai_manager=None,
    current_profile_idx: int = 0,
    on_profile_selected: Optional[Callable[[int, str], None]] = None
) -> None:
    """Hiển thị hộp thoại cấu hình tài nguyên AI ngoại tuyến tối giản."""
    top = tk.Toplevel(parent)
    top.title("Cấu hình mô hình AI")

    # Kế thừa biểu tượng ứng dụng từ cửa sổ cha
    try:
        p_top = parent.winfo_toplevel()
        if hasattr(p_top, "_app_icon_photo") and p_top._app_icon_photo:
            top.iconphoto(False, p_top._app_icon_photo)
        if hasattr(p_top, "ico_path") and p_top.ico_path:
            top.iconbitmap(p_top.ico_path)
    except Exception:
        pass
    top.geometry("580x440")
    top.minsize(540, 410)
    top.resizable(True, True)
    top.configure(bg="#F8FAFC")
    top.transient(parent.winfo_toplevel())
    top.grab_set()

    # Căn giữa màn hình
    try:
        p_top = parent.winfo_toplevel()
        x = p_top.winfo_rootx() + (p_top.winfo_width() - 540) // 2
        y = p_top.winfo_rooty() + (p_top.winfo_height() - 390) // 2
        top.geometry(f"+{max(10, x)}+{max(10, y)}")
    except Exception:
        pass

    # Header
    hdr = tk.Frame(top, bg="#0F172A", pady=10, padx=14)
    hdr.pack(fill=tk.X)
    tk.Label(
        hdr,
        text="CẤU HÌNH MÔ HÌNH AI NGOẠI TUYẾN",
        font=("Segoe UI", 10, "bold"),
        fg="#F8FAFC",
        bg="#0F172A",
    ).pack(anchor="w")
    tk.Label(
        hdr,
        text="Chạy trực tiếp trên máy tính • Không cần kết nối mạng",
        font=("Segoe UI", 8),
        fg="#94A3B8",
        bg="#0F172A",
    ).pack(anchor="w", pady=(2, 0))

    body = tk.Frame(top, bg="#F8FAFC", padx=14, pady=8)
    body.pack(fill=tk.BOTH, expand=True)

    # 1. Khung Chọn Mô Hình
    model_card = tk.LabelFrame(
        body,
        text=" Lựa chọn mô hình ",
        font=("Segoe UI", 8, "bold"),
        fg="#0F172A",
        bg="#FFFFFF",
        padx=10,
        pady=6,
    )
    model_card.pack(fill=tk.X, pady=(0, 8))

    selected_idx = tk.IntVar(value=current_profile_idx)

    profiles = [
        (
            0,
            "1. Thuần thuật toán Python",
            "Tốc độ tức thì, không tốn RAM, phù hợp mọi cấu hình máy."
        ),
        (
            1,
            "2. DeepSeek-R1 1.5B (Gợi ý cho máy nhẹ)",
            "Mô hình nhỏ gọn (~1.5 GB RAM), phản hồi nhanh, không gây nặng máy."
        ),
        (
            2,
            "3. Qwen 2.5 Coder 7B",
            "Mô hình chi tiết, khuyến nghị máy có RAM từ 16 GB trở lên."
        ),
        (
            3,
            "4. DeepSeek-R1 7B",
            "Mô hình suy luận nhiều bước, khuyến nghị máy có RAM từ 16 GB trở lên."
        ),
    ]

    for idx, title, desc in profiles:
        r_frame = tk.Frame(model_card, bg="#FFFFFF")
        r_frame.pack(fill=tk.X, pady=2)
        rb = tk.Radiobutton(
            r_frame,
            text=title,
            variable=selected_idx,
            value=idx,
            font=("Segoe UI", 8, "bold" if idx == 1 else "normal"),
            fg="#0067C0" if idx == 1 else "#0F172A",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
        )
        rb.pack(anchor="w")
        tk.Label(
            r_frame,
            text=f"    {desc}",
            font=("Segoe UI", 7),
            fg="#64748B",
            bg="#FFFFFF",
        ).pack(anchor="w")

    # 2. Khung Trạng Thái Runtime
    rt_card = tk.LabelFrame(
        body,
        text=" Trạng thái hệ thống ",
        font=("Segoe UI", 8, "bold"),
        fg="#0F172A",
        bg="#FFFFFF",
        padx=10,
        pady=6,
    )
    rt_card.pack(fill=tk.X, pady=(0, 6))

    lbl_status_rt = tk.Label(rt_card, text="Đang kiểm tra...", font=("Segoe UI", 8), bg="#FFFFFF", fg="#475569")
    lbl_status_rt.pack(anchor="w")

    def update_runtime_info():
        try:
            if ai_hub:
                st = ai_hub.status()
                ollama_ok = st.get("ollama_ready", False)
                models = st.get("ollama_installed", [])
                gguf_ok = bool(st.get("gguf_file"))
                if ollama_ok:
                    m_list = ", ".join(models) if models else "deepseek-r1:1.5b"
                    msg = f"Ollama đang chạy | Mô hình sẵn sàng: {m_list}"
                    lbl_status_rt.config(text=msg, fg="#16A34A")
                elif gguf_ok:
                    msg = "Tệp mô hình GGUF đã có trong thư mục models"
                    lbl_status_rt.config(text=msg, fg="#16A34A")
                else:
                    msg = "Chưa phát hiện Ollama hoặc tệp mô hình trong máy"
                    lbl_status_rt.config(text=msg, fg="#D97706")
            else:
                lbl_status_rt.config(text="Chế độ thuật toán Python sẵn sàng", fg="#16A34A")
        except Exception as e:
            lbl_status_rt.config(text=f"Trạng thái: {e}", fg="#64748B")

    update_runtime_info()

    act_f = tk.Frame(rt_card, bg="#FFFFFF")
    act_f.pack(fill=tk.X, pady=(4, 0))

    def on_download_click():
        try:
            from stem_shared_core.hf_downloader import ask_download_model
            ask_download_model(parent=top)
            update_runtime_info()
        except Exception as ex:
            messagebox.showerror("Tải Mô Hình", f"Không thể mở trình tải: {ex}", parent=top)

    def on_open_folder():
        target_dir = os.path.abspath(r"models\gguf")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        if hasattr(os, "startfile"):
            os.startfile(target_dir)
        else:
            webbrowser.open(target_dir)

    tk.Button(
        act_f,
        text="Kiểm tra lại",
        font=("Segoe UI", 8),
        bg="#F1F5F9",
        fg="#0F172A",
        relief="solid",
        bd=1,
        padx=6,
        command=update_runtime_info,
    ).pack(side=tk.LEFT, padx=(0, 4))

    tk.Button(
        act_f,
        text="Thư mục models",
        font=("Segoe UI", 8),
        bg="#F1F5F9",
        fg="#0F172A",
        relief="solid",
        bd=1,
        padx=6,
        command=on_open_folder,
    ).pack(side=tk.LEFT, padx=4)

    tk.Button(
        act_f,
        text="Tải mô hình 1.5B",
        font=("Segoe UI", 8),
        bg="#0067C0",
        fg="#FFFFFF",
        relief="flat",
        padx=8,
        command=on_download_click,
    ).pack(side=tk.RIGHT)

    # 3. Thanh nút bấm Lưu / Đóng
    bottom_f = tk.Frame(top, bg="#F8FAFC", padx=14, pady=6)
    bottom_f.pack(fill=tk.X, side=tk.BOTTOM)

    def on_save_apply():
        choice = selected_idx.get()
        if 0 <= choice < len(profiles):
            chosen_title = profiles[choice][1]
            if on_profile_selected:
                on_profile_selected(choice, chosen_title)
        top.destroy()

    tk.Button(
        bottom_f,
        text="Lưu và Áp dụng",
        font=("Segoe UI", 8, "bold"),
        bg="#10B981",
        fg="#FFFFFF",
        relief="flat",
        padx=12,
        pady=3,
        cursor="hand2",
        command=on_save_apply,
    ).pack(side=tk.RIGHT, padx=(4, 0))

    tk.Button(
        bottom_f,
        text="Đóng",
        font=("Segoe UI", 8),
        bg="#E2E8F0",
        fg="#0F172A",
        relief="solid",
        bd=1,
        padx=10,
        pady=3,
        cursor="hand2",
        command=top.destroy,
    ).pack(side=tk.RIGHT, padx=4)
