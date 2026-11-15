import os

with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_old = """    def save_plot_dialog(self, fig=None):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to save!" if is_en else "Tab hiện tại không có đồ thị để lưu!")
            return

        path = filedialog.asksaveasfilename(
            title="Save Plot Image" if is_en else "Lưu hình ảnh đồ thị",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("PDF Document", "*.pdf"), ("SVG Vector Image", "*.svg")]
        )
        if path:
            try:
                target_fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='#ffffff', edgecolor='none')
                messagebox.showinfo("Success" if is_en else "Thành công", f"Exported high-res plot image (300 DPI):\\n{path}" if is_en else f"Đã xuất ảnh đồ thị chất lượng cao (300 DPI):\\n{path}")
                self.status_lbl.config(text=f"Saved plot image: {os.path.basename(path)}" if is_en else f"Đã lưu ảnh đồ thị: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi lưu ảnh", f"Cannot save plot image: {e}" if is_en else f"Không thể lưu ảnh đồ thị: {e}")"""

replacement_new = """    def print_plot_action(self, fig=None):
        \"\"\"In ấn đồ thị trực tiếp qua hộp thoại Windows Print chuẩn A4 / Máy in.\"\"\"
        import tempfile
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to print!" if is_en else "Tab hiện tại không có đồ thị để in!")
            return

        try:
            temp_path = os.path.join(tempfile.gettempdir(), "cad_math_print_plot.png")
            wm = target_fig.text(
                0.98, 0.02,
                "CAD Math Studio Pro",
                fontsize=8,
                color="#64748b",
                alpha=0.18,
                ha="right",
                va="bottom",
                fontstyle="italic"
            )
            target_fig.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
            try:
                wm.remove()
                target_fig.canvas.draw_idle()
            except Exception:
                pass

            os.startfile(temp_path, "print")
            self.status_lbl.config(text="Sending plot to Windows Print dialog..." if is_en else "Đang mở hộp thoại In ấn Windows...")
        except Exception as e:
            try:
                os.startfile(temp_path)
            except Exception:
                messagebox.showerror("Print Error" if is_en else "Lỗi in ấn", str(e))

    def save_plot_dialog(self, fig=None):
        is_en = (getattr(self, "current_lang", "vi") == "en")
        target_fig = fig
        if not target_fig:
            current_tab_idx = self.notebook.index(self.notebook.select())
            if current_tab_idx == 0: target_fig = getattr(self, 'eq_fig', None)
            elif current_tab_idx == 1: target_fig = getattr(self, 'ext_fig', None)
            elif current_tab_idx == 2: target_fig = getattr(self, 'calc_fig', None)
            elif current_tab_idx == 4: target_fig = getattr(self, 'stat_fig', None)
            elif current_tab_idx == 5: target_fig = getattr(self, 'plot_fig', None)

        if not target_fig:
            messagebox.showwarning("Warning" if is_en else "Cảnh báo", "Current tab does not have a plot to save!" if is_en else "Tab hiện tại không có đồ thị để lưu!")
            return

        path = filedialog.asksaveasfilename(
            title="Save Plot Image (with Subtle Trademark)" if is_en else "Lưu hình ảnh đồ thị (kèm Trademark mờ)",
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image / In ấn thông thường (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("PDF Document (*.pdf)", "*.pdf"),
                ("SVG Vector Image (*.svg)", "*.svg")
            ]
        )
        if path:
            try:
                ext = os.path.splitext(path)[1].lower()
                wm_artist = target_fig.text(
                    0.98, 0.02,
                    "CAD Math Studio Pro",
                    fontsize=8,
                    color="#64748b",
                    alpha=0.18,
                    ha="right",
                    va="bottom",
                    fontstyle="italic",
                    fontfamily="sans-serif"
                )

                if ext in [".jpg", ".jpeg"]:
                    import io
                    from PIL import Image
                    buf = io.BytesIO()
                    target_fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
                    buf.seek(0)
                    im = Image.open(buf).convert('RGB')
                    im.save(path, 'JPEG', quality=95, dpi=(300, 300))
                    buf.close()
                else:
                    target_fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='#ffffff', edgecolor='none')

                try:
                    wm_artist.remove()
                    target_fig.canvas.draw_idle()
                except Exception:
                    pass

                msg_success = f"Exported high-res image (300 DPI):\\n{path}" if is_en else f"Đã xuất ảnh chất lượng cao (300 DPI, trademark mờ phục vụ in ấn):\\n{path}"
                messagebox.showinfo("Success" if is_en else "Thành công", msg_success)
                self.status_lbl.config(text=f"Saved plot image: {os.path.basename(path)}" if is_en else f"Đã lưu ảnh đồ thị: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error" if is_en else "Lỗi lưu ảnh", f"Cannot save plot image: {e}" if is_en else f"Không thể lưu ảnh đồ thị: {e}")"""

if target_old in content:
    content = content.replace(target_old, replacement_new)
    print("Replaced save_plot_dialog successfully!")
else:
    print("Target not found directly, checking normalized...")

# Add print button to create_plot_toolbar
old_btn_save = """        btn_save = tk.Button(
            tb_frame,
            text="💾 " + ("Save Plot" if is_en else "Lưu Ảnh"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#0969da",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_save
        )
        btn_save.pack(side=tk.LEFT, padx=3, pady=2)"""

new_btn_save = """        btn_save = tk.Button(
            tb_frame,
            text="💾 " + ("Save Plot" if is_en else "Lưu Ảnh"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#0969da",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_save
        )
        btn_save.pack(side=tk.LEFT, padx=3, pady=2)

        def _do_print():
            fig = fig_getter()
            if auto_solve_func:
                if not fig or not fig.axes or not any(ax.lines or ax.collections or ax.patches for ax in fig.axes):
                    auto_solve_func()
                    fig = fig_getter()
            self.print_plot_action(fig)

        btn_print = tk.Button(
            tb_frame,
            text="🖨️ " + ("Print" if is_en else "In Ấn"),
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#10b981",
            relief="solid", bd=1, padx=6, pady=1,
            cursor="hand2",
            command=_do_print
        )
        btn_print.pack(side=tk.LEFT, padx=3, pady=2)"""

if old_btn_save in content:
    content = content.replace(old_btn_save, new_btn_save)
    print("Added Print button to toolbar successfully!")

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.write(content)
