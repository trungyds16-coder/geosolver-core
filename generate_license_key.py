# -*- coding: utf-8 -*-
"""
TLabtool - Bộ Sinh Mã Bản Quyền STEM CAD Pro (License Key Generator)
Dành cho Nhà phát triển TLabtool: Sinh mã bản quyền GeoSolver 2D & 3D Pro tặng trường học / giáo viên khóa theo 1 máy tính.
"""

import sys
import hashlib
import platform

SALT_2D = "GEOSOLVER_2D_CAD_PRO_SECRET_SALT_2026"
SALT_3D = "GEOSOLVER_3D_CAD_PRO_SECRET_SALT_2026"


def generate_key_for_hwid(hwid: str, label: str = "EDU", product: str = "2D") -> str:
    """
    Sinh mã kích hoạt Pro khóa chặt duy nhất theo Hardware ID (Mã máy) của máy tính.
    product: "2D" hoặc "3D"
    """
    clean_hw = hwid.strip().upper().replace("-", "").replace(" ", "")
    clean_lbl = (label.strip().upper()[:4] if label.strip() else "VIP").ljust(4, "X")[:4]
    salt = SALT_2D if product == "2D" else SALT_3D
    prefix = "PRO2D" if product == "2D" else "PRO3D"
    raw = f"{clean_hw}|{clean_lbl}|{salt}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()
    return f"{prefix}-{clean_lbl}-{h[:4]}-{h[4:8]}"


def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("TLabtool - Trình Tạo Mã Bản Quyền GeoSolver CAD Pro")
    root.geometry("540x470")
    root.resizable(False, False)
    root.configure(bg="#ECE9D8")

    font_ui = ("Tahoma", 9)
    font_bold = ("Tahoma", 9, "bold")

    # Header
    hdr = tk.Frame(root, bg="#002D62", pady=10, padx=14)
    hdr.pack(fill=tk.X)
    tk.Label(hdr, text="🔑 TRÌNH TẠO KEY BẢN QUYỀN GEOSOLVER CAD PRO", font=("Tahoma", 11, "bold"), bg="#002D62", fg="#FFD700").pack(anchor="w")
    tk.Label(hdr, text="Sinh mã kích hoạt miễn phí tặng trường học — Khóa bản quyền 1 máy", font=("Tahoma", 8), bg="#002D62", fg="#FFFFFF").pack(anchor="w")

    body = tk.Frame(root, bg="#ECE9D8", padx=16, pady=12)
    body.pack(fill=tk.BOTH, expand=True)

    # 0. Chọn sản phẩm
    tk.Label(body, text="0. Chọn Sản phẩm:", font=font_bold, bg="#ECE9D8").pack(anchor="w", pady=(0, 2))
    var_product = tk.StringVar(value="2D")
    f_prod = tk.Frame(body, bg="#ECE9D8")
    f_prod.pack(fill=tk.X, pady=(0, 8))
    tk.Radiobutton(f_prod, text="📐 GeoSolver 2D CAD Pro (Mặt phẳng Oxy)", variable=var_product, value="2D", bg="#ECE9D8", font=font_ui).pack(side=tk.LEFT, padx=(0, 14))
    tk.Radiobutton(f_prod, text="📦 GeoSolver 3D CAD Pro (Hình không gian)", variable=var_product, value="3D", bg="#ECE9D8", font=font_ui).pack(side=tk.LEFT)

    # 1. Hardware ID
    tk.Label(body, text="1. Nhập Mã máy của người nhận (Hardware ID do người dùng gửi):", font=font_bold, bg="#ECE9D8").pack(anchor="w", pady=(0, 2))
    entry_hwid = tk.Entry(body, font=("Consolas", 11, "bold"), width=35)
    entry_hwid.pack(fill=tk.X, pady=(0, 8))
    entry_hwid.insert(0, "Ví dụ: 6DE9-1469-D7AB")

    # 2. Label / Trường học
    tk.Label(body, text="2. Tên Trường học / Giáo viên nhận key (Không dấu, viết liền):", font=font_bold, bg="#ECE9D8").pack(anchor="w", pady=(0, 2))
    entry_label = tk.Entry(body, font=font_ui, width=35)
    entry_label.pack(fill=tk.X, pady=(0, 12))
    entry_label.insert(0, "THPT-CHUYEN")

    # Result Box
    res_frame = tk.LabelFrame(body, text="MÃ KÍCH HOẠT ĐÃ TẠO (Gửi mã này cho trường)", font=font_bold, bg="#ECE9D8", padx=10, pady=8)
    res_frame.pack(fill=tk.X, pady=(0, 10))

    entry_key = tk.Entry(res_frame, font=("Consolas", 13, "bold"), fg="#000080", bg="#FFFFFF", justify="center")
    entry_key.pack(fill=tk.X, pady=4)

    def on_generate():
        hw = entry_hwid.get().strip()
        lbl = entry_label.get().strip()
        prod = var_product.get()
        if not hw or "Ví dụ" in hw:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã máy tính (Hardware ID) của người nhận!")
            return
        key = generate_key_for_hwid(hw, lbl, prod)
        entry_key.delete(0, tk.END)
        entry_key.insert(0, key)
        root.clipboard_clear()
        root.clipboard_append(key)
        messagebox.showinfo("Đã tạo mã", f"Đã tạo mã thành công cho GeoSolver {prod} Pro và sao chép vào bộ nhớ đệm:\n\n{key}\n\n(Mã này chỉ kích hoạt được trên đúng máy có Hardware ID {hw})")

    def on_copy():
        k = entry_key.get().strip()
        if k:
            root.clipboard_clear()
            root.clipboard_append(k)
            messagebox.showinfo("Đã sao chép", "Đã sao chép mã vào bộ nhớ đệm (Clipboard)!")

    btn_row = tk.Frame(body, bg="#ECE9D8")
    btn_row.pack(fill=tk.X, pady=4)

    tk.Button(btn_row, text="[ ⚡ Tạo Mã Kích Hoạt (Tự Động Copy) ]", font=font_bold, bg="#2E7D32", fg="#FFFFFF", padx=10, pady=5, command=on_generate).pack(side=tk.LEFT)
    tk.Button(btn_row, text="[ Sao chép lại ]", font=font_ui, bg="#ECE9D8", padx=8, pady=5, command=on_copy).pack(side=tk.LEFT, padx=6)

    tk.Label(
        body,
        text="* Lưu ý: Mã này tính toán theo thuật toán băm mật mã học (SHA-256).\nNgười nhận không thể chia sẻ mã cho máy khác vì khác Hardware ID sẽ bị từ chối.",
        font=("Tahoma", 8, "italic"),
        fg="#555555",
        bg="#ECE9D8",
        justify="left"
    ).pack(anchor="w", pady=(8, 0))

    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "":
        hwid_arg = sys.argv[1]
        lbl_arg = sys.argv[2] if len(sys.argv) > 2 else "VIP"
        prod_arg = sys.argv[3] if len(sys.argv) > 3 else "2D"
        k = generate_key_for_hwid(hwid_arg, lbl_arg, prod_arg)
        print(f"Product: GeoSolver {prod_arg} Pro")
        print(f"HWID:    {hwid_arg}")
        print(f"Key:     {k}")
    else:
        run_gui()
