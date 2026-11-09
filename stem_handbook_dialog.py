# -*- coding: utf-8 -*-
"""
stem_handbook_dialog.py
Hệ thống Hướng Dẫn Sử Dụng CAD Math & GeoSolver 2D (In-App Desktop User Guide)
Thiết kế theo chuẩn Classic Help:
- Tên cửa sổ: "Hướng dẫn sử dụng GeoSolver 2D" / "GeoSolver 2D User Guide"
- Dấu hỏi lớn (❓) trên thanh tiêu đề
- Tab bên trái đặt trong PanedWindow có thể kéo thả (draggable sash)
- Tự động căn chỉnh vừa vặn nội dung
- Mặc định hiển thị TIẾNG ANH (English default), chuyển sang Tiếng Việt khi bấm chuyển
- Thanh tìm kiếm hỗ trợ tìm kiếm toàn diện xuyên suốt tất cả các chuyên mục với highlight
- Tích hợp biểu tượng icon cửa sổ chính hãng từ assets
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import webbrowser

_ACTIVE_DIALOG = None


class STEMHandbookDialog(tk.Toplevel):
    """
    Cửa sổ Hướng dẫn sử dụng GeoSolver 2D tích hợp trong phần mềm.
    """

    def __init__(self, parent=None, initial_tab=0, initial_lang="en"):
        super().__init__(parent)
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

        # Mặc định tiếng Anh theo yêu cầu người dùng
        self.current_lang = initial_lang if initial_lang in ("en", "vi") else "en"
        self.current_tab_idx = initial_tab

        # Cập nhật tiêu đề cửa sổ theo ngôn ngữ
        self._update_window_title()

        self.geometry("980x680")
        self.minsize(760, 480)
        self.configure(bg="#FFFFFF")

        # Thiết lập icon cho cửa sổ
        self._setup_window_icon()

        # Dữ liệu tìm kiếm
        self.search_matches = []  # danh sách các vị trí match trong tab hiện tại
        self.current_match_idx = -1

        self._build_header()
        self._build_paned_body()
        self._build_footer()

        # Phím tắt trong cửa sổ hướng dẫn
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Control-f>", lambda e: self.entry_search.focus_set())
        self.bind("<F3>", lambda e: self.find_next())

        # Hiển thị tab ban đầu
        self.switch_topic(self.current_tab_idx)

        # Căn giữa màn hình
        self._center_window()

    def _setup_window_icon(self):
        """Nạp biểu tượng icon cho cửa sổ từ assets."""
        possible_icons = [
            os.path.join(self.root_dir, "cad_math_v2", "assets", "cad_math.ico"),
            os.path.join(self.root_dir, "geosolver", "assets", "geosolver_2d.ico"),
            os.path.join(self.root_dir, "geosolver_3d", "assets", "geosolver_3d.ico"),
            os.path.join(self.root_dir, "stem_shared_core", "assets", "cad_math.ico")
        ]
        for ico in possible_icons:
            if os.path.exists(ico):
                try:
                    self.iconbitmap(ico)
                    break
                except Exception:
                    pass

    def _update_window_title(self):
        if self.current_lang == "vi":
            self.title("Hướng dẫn sử dụng GeoSolver 2D")
        else:
            self.title("GeoSolver 2D User Guide")

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # =========================================================================
    # HEADER: DẤU HỎI LỚN, TIÊU ĐỀ, CHUYỂN NGÔN NGỮ & THANH TÌM KIẾM
    # =========================================================================
    def _build_header(self):
        self.header_frame = tk.Frame(self, bg="#FFFFFF", padx=16, pady=12)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Dấu hỏi lớn classic (❓)
        canvas_q = tk.Canvas(self.header_frame, width=44, height=44, bg="#FFFFFF", highlightthickness=0)
        canvas_q.pack(side=tk.LEFT, padx=(0, 12))
        canvas_q.create_oval(2, 2, 42, 42, outline="#000000", width=2, fill="#F9FAFB")
        canvas_q.create_text(22, 22, text="?", font=("Georgia", 22, "bold"), fill="#000000")

        # Cụm tiêu đề chính
        title_box = tk.Frame(self.header_frame, bg="#FFFFFF")
        title_box.pack(side=tk.LEFT, fill=tk.Y)

        self.lbl_main_title = tk.Label(
            title_box,
            text="GEOSOLVER 2D USER GUIDE" if self.current_lang == "en" else "HƯỚNG DẪN SỬ DỤNG GEOSOLVER 2D",
            font=("Segoe UI", 13, "bold"),
            fg="#000000",
            bg="#FFFFFF"
        )
        self.lbl_main_title.pack(anchor=tk.W)

        self.lbl_main_sub = tk.Label(
            title_box,
            text="CAD Math Studio v2.1 & GeoSolver 2D CAD • Complete Operations Handbook" if self.current_lang == "en" else "Bộ đôi CAD Math Studio v2.1 & GeoSolver 2D CAD • Sổ tay hướng dẫn toàn tập",
            font=("Segoe UI", 9),
            fg="#4B5563",
            bg="#FFFFFF"
        )
        self.lbl_main_sub.pack(anchor=tk.W, pady=(2, 0))

        # Cụm tìm kiếm và nút đổi ngôn ngữ bên phải
        right_hdr = tk.Frame(self.header_frame, bg="#FFFFFF")
        right_hdr.pack(side=tk.RIGHT, fill=tk.Y)

        # Nút chuyển đổi ngôn ngữ Anh / Việt
        self.btn_lang = tk.Button(
            right_hdr,
            text="🌐 Tiếng Việt" if self.current_lang == "en" else "🌐 English",
            font=("Segoe UI", 9, "bold"),
            bg="#F3F4F6",
            fg="#000000",
            relief="solid",
            bd=1,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.toggle_language
        )
        self.btn_lang.pack(side=tk.TOP, anchor="e", pady=(0, 6))

        # Thanh tìm kiếm
        search_box = tk.Frame(right_hdr, bg="#FFFFFF")
        search_box.pack(side=tk.TOP, anchor="e")

        lbl_s = tk.Label(search_box, text="Search:" if self.current_lang == "en" else "Tìm kiếm:", font=("Segoe UI", 9), fg="#4B5563", bg="#FFFFFF")
        lbl_s.pack(side=tk.LEFT, padx=(0, 4))

        self.var_search = tk.StringVar()
        self.entry_search = tk.Entry(
            search_box,
            textvariable=self.var_search,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
            width=16
        )
        self.entry_search.pack(side=tk.LEFT, ipady=1)
        self.entry_search.bind("<Return>", lambda e: self.do_search())

        self.btn_search = tk.Button(
            search_box,
            text="Find" if self.current_lang == "en" else "Tìm",
            font=("Segoe UI", 8, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            relief="solid",
            bd=1,
            padx=6,
            pady=1,
            cursor="hand2",
            command=self.do_search
        )
        self.btn_search.pack(side=tk.LEFT, padx=(4, 2))

        self.btn_next = tk.Button(
            search_box,
            text="Next" if self.current_lang == "en" else "Tiếp",
            font=("Segoe UI", 8),
            bg="#F3F4F6",
            fg="#000000",
            relief="solid",
            bd=1,
            padx=4,
            pady=1,
            cursor="hand2",
            command=self.find_next
        )
        self.btn_next.pack(side=tk.LEFT)

        # Đường kẻ phân cách đen trắng
        sep = tk.Frame(self, height=1, bg="#000000")
        sep.pack(side=tk.TOP, fill=tk.X)

    # =========================================================================
    # BODY: THANH KÉO THẢ (PANEDWINDOW SASH) & NỘI DUNG TỰ CĂN CHỈNH
    # =========================================================================
    def _build_paned_body(self):
        # Sử dụng PanedWindow để người dùng có thể kéo thả điều chỉnh độ rộng tab trái!
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6, sashrelief=tk.RAISED, bg="#D1D5DB")
        self.paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 1. PANE TRÁI: KHUNG DANH MỤC CÓ THỂ KÉO THẢ
        self.left_pane = tk.Frame(self.paned, bg="#F9FAFB", width=250)
        self.paned.add(self.left_pane, minsize=180, width=250)

        self.lbl_side_title = tk.Label(
            self.left_pane,
            text="TOPICS / SECTIONS" if self.current_lang == "en" else "DANH MỤC CHỦ ĐỀ",
            font=("Segoe UI", 9, "bold"),
            fg="#6B7280",
            bg="#F9FAFB",
            anchor="w",
            padx=12,
            pady=8
        )
        self.lbl_side_title.pack(side=tk.TOP, fill=tk.X)

        # Frame cuộn chứa danh sách tab
        self.tab_container = tk.Frame(self.left_pane, bg="#F9FAFB")
        self.tab_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=4, pady=2)

        self.topic_buttons = []
        self._populate_topic_buttons()

        # Bắt sự kiện co giãn của pane trái để tự động căn chỉnh chữ vừa tab!
        self.left_pane.bind("<Configure>", self._on_left_pane_resize)

        # 2. PANE PHẢI: KHUNG VĂN BẢN TỰ CO GIÃN THEO KHUNG
        self.right_pane = tk.Frame(self.paned, bg="#FFFFFF")
        self.paned.add(self.right_pane, minsize=400)

        self.txt = scrolledtext.ScrolledText(
            self.right_pane,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#111827",
            padx=20,
            pady=16,
            relief="flat",
            bd=0
        )
        self.txt.pack(fill=tk.BOTH, expand=True)

        # Text tags định dạng
        self.txt.tag_config("h1", font=("Segoe UI", 13, "bold"), foreground="#000000", spacing3=6)
        self.txt.tag_config("h2", font=("Segoe UI", 11, "bold"), foreground="#1F2937", spacing1=8, spacing3=4)
        self.txt.tag_config("body", font=("Segoe UI", 10), foreground="#111827", spacing2=3)
        self.txt.tag_config("bullet", font=("Segoe UI", 10), foreground="#111827", lmargin1=16, lmargin2=28, spacing2=2)
        self.txt.tag_config("key", font=("Consolas", 9, "bold"), background="#E5E7EB", foreground="#000000")
        self.txt.tag_config("code", font=("Consolas", 9), background="#F3F4F6", foreground="#111827")
        self.txt.tag_config("box", font=("Segoe UI", 10), background="#F9FAFB", foreground="#111827", lmargin1=16, lmargin2=16, spacing1=4, spacing3=4)
        self.txt.tag_config("table_header", font=("Consolas", 9, "bold"), background="#F3F4F6", foreground="#000000")
        self.txt.tag_config("table_row", font=("Consolas", 9), foreground="#111827")
        self.txt.tag_config("highlight", background="#FEF08A", foreground="#000000")
        self.txt.tag_config("current_highlight", background="#F59E0B", foreground="#FFFFFF")

    def _on_left_pane_resize(self, event):
        """Tự động điều chỉnh wraplength của các nút danh mục để vừa vặn khi người dùng kéo thả tab trái."""
        new_width = max(150, event.width - 24)
        for btn in self.topic_buttons:
            try:
                btn.configure(wraplength=new_width)
            except Exception:
                pass

    def _get_topics_def(self):
        if self.current_lang == "vi":
            return [
                ("1. 📌 Tổng quan hệ thống", self._content_overview_vi),
                ("2. 📐 CAD Math: 6 Chuyên đề", self._content_cad_math_vi),
                ("3. ✏️ GeoSolver: Dựng hình CAD & Elip", self._content_geosolver_tools_vi),
                ("4. 🔍 Quan hệ tự động & Ẩn nét", self._content_invariants_and_ghost_vi),
                ("5. ⌨️ Bảng tra cứu phím tắt", self._content_shortcuts_vi),
                ("6. 💡 Mẹo thao tác tối ưu (Pro Tips)", self._content_protips_vi)
            ]
        else:
            return [
                ("1. 📌 System Overview", self._content_overview_en),
                ("2. 📐 CAD Math: 6 Core Modules", self._content_cad_math_en),
                ("3. ✏️ GeoSolver: CAD Tools & Ellipse", self._content_geosolver_tools_en),
                ("4. 🔍 Invariant Detection & Ghost Mode", self._content_invariants_and_ghost_en),
                ("5. ⌨️ Complete Shortcuts Cheat Sheet", self._content_shortcuts_en),
                ("6. 💡 Operational Pro Tips", self._content_protips_en)
            ]

    def _populate_topic_buttons(self):
        for btn in self.topic_buttons:
            btn.destroy()
        self.topic_buttons.clear()

        self.topics = self._get_topics_def()
        for idx, (label, _) in enumerate(self.topics):
            btn = tk.Button(
                self.tab_container,
                text=label,
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
                padx=10,
                pady=7,
                relief="flat",
                bd=0,
                cursor="hand2",
                wraplength=220,
                command=lambda i=idx: self.switch_topic(i)
            )
            btn.pack(fill=tk.X, padx=4, pady=2)
            self.topic_buttons.append(btn)

    # =========================================================================
    # FOOTER: TRẠNG THÁI & CÁC NÚT MỞ BẢN IN
    # =========================================================================
    def _build_footer(self):
        sep = tk.Frame(self, height=1, bg="#E5E7EB")
        sep.pack(side=tk.TOP, fill=tk.X)

        self.footer = tk.Frame(self, bg="#FFFFFF", padx=16, pady=8)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_status = tk.Label(
            self.footer,
            text="Shortcuts: Esc to Close • Ctrl+F to Search • F3 for Next Match" if self.current_lang == "en" else "Phím tắt: Esc để đóng • Ctrl+F để tìm kiếm • F3 tìm tiếp",
            font=("Segoe UI", 9),
            fg="#6B7280",
            bg="#FFFFFF"
        )
        self.lbl_status.pack(side=tk.LEFT)

        self.btn_close = tk.Button(
            self.footer,
            text="Close (Esc)" if self.current_lang == "en" else "Đóng (Esc)",
            font=("Segoe UI", 9, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            relief="solid",
            bd=1,
            padx=12,
            pady=2,
            cursor="hand2",
            command=self.destroy
        )
        self.btn_close.pack(side=tk.RIGHT, padx=(6, 0))

        self.btn_open_md = tk.Button(
            self.footer,
            text="Open Markdown (.md)" if self.current_lang == "en" else "Mở tệp Markdown (.md)",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._open_markdown_file
        )
        self.btn_open_md.pack(side=tk.RIGHT, padx=(6, 0))

        self.btn_open_html = tk.Button(
            self.footer,
            text="Open HTML Guide" if self.current_lang == "en" else "Mở bản in HTML",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#000000",
            relief="solid",
            bd=1,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._open_html_file
        )
        self.btn_open_html.pack(side=tk.RIGHT)

    def _open_markdown_file(self):
        md_p = os.path.join(self.root_dir, "CAM_NANG_SU_DUNG_STEM_CAD_MATH.md")
        if os.path.exists(md_p):
            try:
                os.startfile(md_p)
            except Exception:
                webbrowser.open(md_p)

    def _open_html_file(self):
        html_p = os.path.join(self.root_dir, "CAM_NANG_SU_DUNG_STEM_CAD_MATH.html")
        if os.path.exists(html_p):
            try:
                webbrowser.open(os.path.abspath(html_p))
            except Exception:
                os.startfile(html_p)

    # =========================================================================
    # CHUYỂN ĐỔI NGÔN NGỮ (ANH <-> VIỆT)
    # =========================================================================
    def toggle_language(self):
        self.current_lang = "vi" if self.current_lang == "en" else "en"
        self._update_window_title()

        # Cập nhật nhãn nút & text
        if self.current_lang == "en":
            self.lbl_main_title.config(text="GEOSOLVER 2D USER GUIDE")
            self.lbl_main_sub.config(text="CAD Math Studio v2.1 & GeoSolver 2D CAD • Complete Operations Handbook")
            self.btn_lang.config(text="🌐 Tiếng Việt")
            self.btn_search.config(text="Find")
            self.btn_next.config(text="Next")
            self.lbl_side_title.config(text="TOPICS / SECTIONS")
            self.btn_close.config(text="Close (Esc)")
            self.btn_open_md.config(text="Open Markdown (.md)")
            self.btn_open_html.config(text="Open HTML Guide")
            self.lbl_status.config(text="Shortcuts: Esc to Close • Ctrl+F to Search • F3 for Next Match")
        else:
            self.lbl_main_title.config(text="HƯỚNG DẪN SỬ DỤNG GEOSOLVER 2D")
            self.lbl_main_sub.config(text="Bộ đôi CAD Math Studio v2.1 & GeoSolver 2D CAD • Sổ tay hướng dẫn toàn tập")
            self.btn_lang.config(text="🌐 English")
            self.btn_search.config(text="Tìm")
            self.btn_next.config(text="Tiếp")
            self.lbl_side_title.config(text="DANH MỤC CHỦ ĐỀ")
            self.btn_close.config(text="Đóng (Esc)")
            self.btn_open_md.config(text="Mở tệp Markdown (.md)")
            self.btn_open_html.config(text="Mở bản in HTML")
            self.lbl_status.config(text="Phím tắt: Esc để đóng • Ctrl+F để tìm kiếm • F3 tìm tiếp")

        # Nạp lại danh mục chủ đề
        self._populate_topic_buttons()
        self.switch_topic(self.current_tab_idx)

    # =========================================================================
    # CHUYỂN ĐỔI CHỦ ĐỀ
    # =========================================================================
    def switch_topic(self, idx):
        if idx < 0 or idx >= len(self.topics):
            idx = 0
        self.current_tab_idx = idx

        for i, btn in enumerate(self.topic_buttons):
            if i == idx:
                btn.configure(bg="#000000", fg="#FFFFFF", font=("Segoe UI", 10, "bold"))
            else:
                btn.configure(bg="#F9FAFB", fg="#1F2937", font=("Segoe UI", 10))

        self.txt.configure(state="normal")
        self.txt.delete("1.0", tk.END)

        _, content_func = self.topics[idx]
        content_func()

        self.txt.configure(state="disabled")
        self.txt.see("1.0")

        # Reset search matches trong tab mới
        self.search_matches.clear()
        self.current_match_idx = -1

    # =========================================================================
    # TÌM KIẾM TOÀN DIỆN XUYÊN SUỐT TẤT CẢ CÁC CHỦ ĐỀ
    # =========================================================================
    def do_search(self):
        raw_query = self.var_search.get().strip().lower()
        if not raw_query:
            return

        query_variants = [raw_query]
        aliases = {
            "elip": "ellipse", "ellipse": "elip",
            "ma tran": "matrix", "matran": "matrix", "matrix": "ma trận",
            "tam giac": "triangle", "tam giác": "triangle", "triangle": "tam giác",
            "phim tat": "shortcut", "phím tắt": "shortcut", "shortcut": "phím tắt",
            "vuong goc": "perpendicular", "vuông góc": "perpendicular",
            "song song": "parallel", "duong tron": "circle", "đường tròn": "circle"
        }
        if raw_query in aliases:
            query_variants.append(aliases[raw_query])

        for q in query_variants:
            # 1. Tìm kiếm trong tab hiện tại trước
            matches_in_current = self._highlight_matches_in_current(q)
            if matches_in_current > 0:
                self.lbl_status.config(
                    text=f"Found {matches_in_current} matches for '{q}' (Match 1/{matches_in_current})." if self.current_lang == "en"
                    else f"Tìm thấy {matches_in_current} kết quả cho '{q}' (Kết quả 1/{matches_in_current})."
                )
                return

            # 2. Nếu không có trong tab hiện tại, quét các tab khác!
            for other_idx, (t_name, _) in enumerate(self.topics):
                if other_idx == self.current_tab_idx:
                    continue
                self.switch_topic(other_idx)
                m_count = self._highlight_matches_in_current(q)
                if m_count > 0:
                    self.lbl_status.config(
                        text=f"Jumped to '{t_name}': Found {m_count} matches for '{q}'." if self.current_lang == "en"
                        else f"Chuyển sang '{t_name}': Tìm thấy {m_count} kết quả cho '{q}'."
                    )
                    return

        # 3. Không tìm thấy bất kỳ đâu
        self.lbl_status.config(
            text=f"No matches found for '{raw_query}' in any section." if self.current_lang == "en"
            else f"Không tìm thấy từ khóa '{raw_query}' trong bất kỳ chuyên mục nào."
        )

    def _highlight_matches_in_current(self, query):
        self.txt.configure(state="normal")
        self.txt.tag_remove("highlight", "1.0", tk.END)
        self.txt.tag_remove("current_highlight", "1.0", tk.END)
        self.search_matches.clear()

        idx = "1.0"
        while True:
            idx = self.txt.search(query, idx, nocase=True, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(query)}c"
            self.txt.tag_add("highlight", idx, end_idx)
            self.search_matches.append((idx, end_idx))
            idx = end_idx

        self.txt.configure(state="disabled")

        if self.search_matches:
            self.current_match_idx = 0
            self._focus_current_match()
            return len(self.search_matches)
        return 0

    def find_next(self):
        if not self.search_matches:
            self.do_search()
            return
        self.current_match_idx = (self.current_match_idx + 1) % len(self.search_matches)
        self._focus_current_match()
        total = len(self.search_matches)
        curr = self.current_match_idx + 1
        self.lbl_status.config(
            text=f"Match {curr}/{total}" if self.current_lang == "en" else f"Kết quả {curr}/{total}"
        )

    def _focus_current_match(self):
        if 0 <= self.current_match_idx < len(self.search_matches):
            start, end = self.search_matches[self.current_match_idx]
            self.txt.configure(state="normal")
            self.txt.tag_remove("current_highlight", "1.0", tk.END)
            self.txt.tag_add("current_highlight", start, end)
            self.txt.configure(state="disabled")
            self.txt.see(start)

    # =========================================================================
    # NỘI DUNG TIẾNG ANH (ENGLISH CONTENT - DEFAULT)
    # =========================================================================
    def _content_overview_en(self):
        t = self.txt
        t.insert(tk.END, "1. SYSTEM OVERVIEW: STEM MATHEMATICS SUITE\n\n", "h1")

        t.insert(tk.END, "Core Architecture:\n", "h2")
        t.insert(tk.END, "The STEM Mathematics Suite combines two deep, complementary technical software modules:\n\n", "body")

        t.insert(tk.END, "• CAD Math Studio v2.1: ", "bullet")
        t.insert(tk.END, "A computer algebra system (CAS) and numerical analysis engine. Solves equations, multivariable optimization, calculus, linear algebra, statistics, and 2D function graphing with interactive Matplotlib plots and real-time MathText/LaTeX rendering.\n", "body")

        t.insert(tk.END, "• GeoSolver 2D CAD Studio: ", "bullet")
        t.insert(tk.END, "A mechanical-grade dynamic geometry modeling environment. Features smart snap-to-grid, exact Apollonius ellipse co-focus construction, automatic invariant detection (equilateral, isosceles, right triangles, parallel, perpendicular, midpoints), and SymPy theorem proving with AI support.\n\n", "body")

        t.insert(tk.END, "Key Operational Pillars:\n", "h2")
        t.insert(tk.END, "1. 100% Offline Algorithmic Power: Completely self-contained; never leaks problem data to third parties.\n", "body")
        t.insert(tk.END, "2. Clean Diagram Publishing: Only geometric lines, point names, and right-angle squares are rendered. No cluttered gray line text.\n", "body")
        t.insert(tk.END, "3. Native 64-bit Clipboard Image Copying: Copy high-resolution, white-background plots directly to the Windows clipboard for instant pasting into Word, PowerPoint, or messaging apps.\n", "body")
        t.insert(tk.END, "4. Exact Radical Representation: Geometric lengths are rendered in simplified radical form (e.g. √34 ≈ 5.83, 5√2, 6) to eliminate float rounding confusion.\n\n", "body")

    def _content_cad_math_en(self):
        t = self.txt
        t.insert(tk.END, "2. CAD MATH STUDIO v2.1: 6 CORE MODULES\n\n", "h1")

        t.insert(tk.END, "Module Breakdown:\n", "h2")

        t.insert(tk.END, "• Tab 1: Equations, Inequalities & Systems (Parametric m, Complex Numbers):\n", "bullet")
        t.insert(tk.END, "  - Natural input syntax: <=, >=, !=, \\le, \\ge. Implicit multiplication: 2x, x sqrt(y), (x+1)(x-2).\n", "body")
        t.insert(tk.END, "  - Radicals and Abs: sqrt(x), root(x, n), \\sqrt{x}, |x|, Abs(x-2).\n", "body")
        t.insert(tk.END, "  - Parameter m: Enter x^2 - 2(m-1)x + m + 5 >= 0 or sqrt(x-1) + sqrt(5-x) <= m. Automatically isolates m, builds the auxiliary function variation table, and computes exact conditions for m.\n", "body")
        t.insert(tk.END, "  - Complex Numbers: Imaginary unit i (sqrt(-1)), conjugates \\bar{z} or z_bar. Example: (1 + 2i)z + 3 - i = 0.\n\n", "body")

        t.insert(tk.END, "• Tab 2: Multivariable Extrema & Inequalities:\n", "bullet")
        t.insert(tk.END, "  - Solves constrained multivariable Max/Min using multi-start Nelder-Mead and SymPy Lagrange multipliers. Visualizes the feasible region with 2D contour maps.\n\n", "body")

        t.insert(tk.END, "• Tab 3: Calculus & Multivariable Analysis:\n", "bullet")
        t.insert(tk.END, "  - Partial derivatives: ∂f/∂x, ∂f/∂y, higher order derivatives.\n", "body")
        t.insert(tk.END, "  - Definite/indefinite integration, Taylor/Maclaurin series expansions at x0.\n\n", "body")

        t.insert(tk.END, "• Tab 4: Linear Algebra & Matrices:\n", "bullet")
        t.insert(tk.END, "  - Matrix line input: Computes determinant det(A), matrix inverse A⁻¹, rank(A), product A x B, and solves AX = B.\n\n", "body")

        t.insert(tk.END, "• Tab 5: Probability & Descriptive Statistics:\n", "bullet")
        t.insert(tk.END, "  - Input sample values: 12, 15, 18, 14, 22, 19, 15, 24, 30.\n", "body")
        t.insert(tk.END, "  - Computes Mean x̄, Median Me, Mode Mo, Variance s², Standard Deviation s, Interquartile Range ΔQ.\n", "body")
        t.insert(tk.END, "  - Auto-plots Histogram and Boxplot with outlier detection.\n\n", "body")

        t.insert(tk.END, "• Tab 6: 2D Oxy Function Analysis & Grapher:\n", "bullet")
        t.insert(tk.END, "  - Comprehensive 12-step curve sketching: domain, derivative y', sign table, extrema, inflection points y'', vertical/horizontal/oblique asymptotes, tangent lines at x0.\n\n", "body")

        t.insert(tk.END, "Formula Canvas (MathFormulaCanvas) & Quick Image Copy:\n", "h2")
        t.insert(tk.END, "• [Copy LaTeX]: Copies LaTeX code to clipboard.\n", "body")
        t.insert(tk.END, "• [Copy Text]: Copies plain mathematical text.\n", "body")
        t.insert(tk.END, "• [📋 Copy Image]: Copies native 300 DPI white-background image into Windows Clipboard (Ctrl+V into Word).\n", "body")
        t.insert(tk.END, "• [💾 Save Image]: Saves plot to PNG/PDF.\n\n", "body")

    def _content_geosolver_tools_en(self):
        t = self.txt
        t.insert(tk.END, "3. GEOSOLVER 2D CAD STUDIO: TOOLS & ELLIPSE\n\n", "h1")

        t.insert(tk.END, "CAD Canvas Navigation:\n", "h2")
        t.insert(tk.END, "• Left Mouse Button (LMB): Select objects, construct shapes, or drag selection box.\n", "body")
        t.insert(tk.END, "• Right Mouse Button (RMB): Cancels construction mode back to [↖ Move]. Right-click on [Hide/Show] button to Unhide All.\n", "body")
        t.insert(tk.END, "• Mouse Wheel: Smooth Zoom In / Zoom Out centered at mouse cursor.\n", "body")
        t.insert(tk.END, "• Middle Mouse Button Drag: Pan entire canvas view.\n\n", "body")

        t.insert(tk.END, "Next-Generation Ellipse Construction Tool:\n", "h2")
        t.insert(tk.END, "Constructs ellipses using Apollonius's classical definition: MF1 + MF2 = 2a.\n", "body")
        t.insert(tk.END, "1. Click Focus 1 (F1).\n", "body")
        t.insert(tk.END, "2. Click Focus 2 (F2). A real-time rubber-band ellipse preview immediately tracks mouse motion.\n", "body")
        t.insert(tk.END, "3. Click point M on the desired rim.\n", "body")
        t.insert(tk.END, "• Automatic Geometry: Center O, semi-major a, semi-minor b, focal distance 2c, area S = πab, and Ramanujan perimeter.\n", "body")
        t.insert(tk.END, "• CAD Translation: Click to select the ellipse (orange outline) and drag to translate the ellipse and its foci smoothly.\n\n", "body")

        t.insert(tk.END, "Clutter-Free Canvas (Zero Ghost Text Labels):\n", "h2")
        t.insert(tk.END, "All auto-jumping text strings like 'ray BI', 'd perpendicular', 'parallel line' have been removed.\n", "body")
        t.insert(tk.END, "Only geometric strokes, point names (A, B, C...), and perpendicular square marks are drawn.\n\n", "body")

    def _content_invariants_and_ghost_en(self):
        t = self.txt
        t.insert(tk.END, "4. INVARIANT DETECTION & GHOST MODE\n\n", "h1")

        t.insert(tk.END, "Deep Invariant Detection with Exact Radical Values:\n", "h2")
        t.insert(tk.END, "Runs continuously with rigorous CAD tolerance (tol = max(0.025, 0.006 * L_max)):\n", "body")
        t.insert(tk.END, "• Special Triangles: Equilateral, right-isosceles, isosceles, right triangles.\n", "body")
        t.insert(tk.END, "• Exact Radical Form: Side lengths are formatted as exact radicals (e.g. √34 ≈ 5.83, 5√2, 6) rather than loose floats.\n", "body")
        t.insert(tk.END, "• Relations: Parallel segments (AB ∥ CD), perpendiculars (AB ⊥ CD), midpoints.\n", "body")
        t.insert(tk.END, "• Auto-feeding: Detected facts populate problem hypotheses automatically for SymPy proving.\n\n", "body")

        t.insert(tk.END, "Ghost Mode (Selective Secondary Hiding):\n", "h2")
        t.insert(tk.END, "• Hide Selected: Select objects -> Click [Hide/Show] to hide auxiliary lines (they remain mathematically linked).\n", "body")
        t.insert(tk.END, "• Ghost View: Click [Hide/Show] when nothing is selected to toggle faint dotted preview (#adb5bd).\n", "body")
        t.insert(tk.END, "• Unhide All: Right-click the [Hide/Show] button or select Options -> Unhide All Objects.\n\n", "body")

        t.insert(tk.END, "Export CAD Image Dialog (Ctrl + E):\n", "h2")
        t.insert(tk.END, "• Independent checkboxes: Oxy axes, Grid, Infinite lines, Auto-crop (25px padding).\n\n", "body")

    def _content_shortcuts_en(self):
        t = self.txt
        t.insert(tk.END, "5. COMPLETE SHORTCUTS CHEAT SHEET\n\n", "h1")

        t.insert(tk.END, "CAD Math Studio v2.1 Shortcuts:\n", "h2")
        header = f"{'Shortcut':<18} | {'Action':<22} | {'Description'}\n"
        sep_line = "-" * 80 + "\n"
        t.insert(tk.END, header, "table_header")
        t.insert(tk.END, sep_line, "table_header")

        cad_keys = [
            ("F1", "Open User Guide", "Opens this in-app User Guide dialog"),
            ("F5 / Enter", "Solve Problem", "Triggers solver for active tab"),
            ("Ctrl + P", "Export HTML Report", "Generates printable HTML report with graphs"),
            ("Ctrl + S", "Save Solution", "Saves full step-by-step text solution"),
            ("Ctrl + Shift + S", "Save Plot Image", "Saves Matplotlib plot to PNG"),
            ("Ctrl + O", "Open Problem File", "Loads previously saved problem text"),
            ("Ctrl + L", "Clear Active Tab", "Clears inputs and outputs of active tab"),
            ("Ctrl + + / -", "Zoom Font In / Out", "Increases or decreases font size in results"),
            ("Ctrl + 0", "Reset Font Size", "Resets font size to default 10pt"),
            ("Ctrl + Q", "Quit Application", "Safely closes application")
        ]
        for k, a, d in cad_keys:
            t.insert(tk.END, f"{k:<18} | {a:<22} | {d}\n", "table_row")

        t.insert(tk.END, "\nGeoSolver 2D CAD Studio Shortcuts:\n", "h2")
        t.insert(tk.END, header, "table_header")
        t.insert(tk.END, sep_line, "table_header")

        geo_keys = [
            ("F1", "Open User Guide", "Opens this in-app User Guide dialog"),
            ("F5", "AI Solve", "Runs AI Support geometric reasoning"),
            ("Ctrl + Z", "Undo", "Reverts previous drawing or deletion step"),
            ("Ctrl + Y", "Redo", "Restores undone operation"),
            ("Ctrl + A", "Select All", "Selects all points, lines, segments, ellipses"),
            ("Ctrl + C / V", "Copy / Paste", "Copies and pastes selected geometric entities"),
            ("Ctrl + N", "New Drawing", "Clears canvas and resets problem state"),
            ("Ctrl + E", "Export CAD Image", "Opens 300 DPI image export dialog"),
            ("Ctrl + P", "Export HTML Report", "Generates complete HTML dossier"),
            ("Delete / Backspace", "Delete Selected", "Deletes active geometric objects"),
            ("Escape (Esc)", "Cancel Tool", "Returns pointer to default [↖ Move] tool"),
            ("Mouse Wheel", "Zoom In / Out", "Zooms canvas centered at cursor"),
            ("Middle Drag", "Pan Canvas", "Pans entire CAD viewing space"),
            ("Right-Click [Hide]", "Unhide All", "Restores all hidden auxiliary objects")
        ]
        for k, a, d in geo_keys:
            t.insert(tk.END, f"{k:<18} | {a:<22} | {d}\n", "table_row")
        t.insert(tk.END, "\n")

    def _content_protips_en(self):
        t = self.txt
        t.insert(tk.END, "6. OPERATIONAL PRO TIPS\n\n", "h1")

        t.insert(tk.END, "💡 Pro Tip 1: Paste directly into Word & PowerPoint without saving files\n", "h2")
        t.insert(tk.END, "Never save to a temporary file just to Insert Picture. Click [📋 Copy Image] on any graph tab in CAD Math Studio or choose 'Options -> Copy Canvas Image to Clipboard' in GeoSolver 2D. Then open Word/PowerPoint and press Ctrl + V. The high-resolution image appears immediately on pure white background!\n\n", "box")

        t.insert(tk.END, "💡 Pro Tip 2: Textbook-perfect exam figures with Auto-Crop\n", "h2")
        t.insert(tk.END, "When opening the Export Image Dialog (Ctrl + E) in GeoSolver 2D, check 'Auto-crop to content' and uncheck 'Oxy coordinate axes' and 'Coordinate grid'. The exported PNG will be tightly cropped with a neat 25px margin ready for tests and exams.\n\n", "box")

        t.insert(tk.END, "💡 Pro Tip 3: Rapid math symbol buttons\n", "h2")
        t.insert(tk.END, "Directly below GeoSolver 2D's toolbars, click the buttons ∠, |x|, cos, √, π to insert mathematical notations instantly without switching keyboard input methods.\n\n", "box")

    # =========================================================================
    # NỘI DUNG TIẾNG VIỆT (VIETNAMESE CONTENT)
    # =========================================================================
    def _content_overview_vi(self):
        t = self.txt
        t.insert(tk.END, "1. TỔNG QUAN HỆ THỐNG STEM MATHEMATICS SUITE\n\n", "h1")
        t.insert(tk.END, "Kiến trúc hệ thống:\n", "h2")
        t.insert(tk.END, "Hệ thống STEM Mathematics Suite kết hợp hai phân hệ bổ trợ chuyên sâu:\n\n", "body")
        t.insert(tk.END, "• CAD Math Studio v2.1: ", "bullet")
        t.insert(tk.END, "Phần mềm giải quyết toàn diện Đại số, Giải tích, Ma trận, Xác suất thống kê và Khảo sát hàm số. Hệ thống tính toán hình thức SymPy chuẩn mực, biểu đồ tương tác Matplotlib và khung MathText thời gian thực.\n", "body")
        t.insert(tk.END, "• GeoSolver 2D CAD Studio: ", "bullet")
        t.insert(tk.END, "Mô hình hóa hình học phẳng động chuẩn CAD cơ khí. Dựng elip chuẩn 2 tiêu điểm Apollonius, tự động nhận diện quan hệ bất biến (tam giác đều, cân, vuông, song song, trung điểm) với kết quả dạng căn thức chính xác.\n\n", "body")

    def _content_cad_math_vi(self):
        t = self.txt
        t.insert(tk.END, "2. CẨM NANG SỬ DỤNG CAD MATH STUDIO v2.1: 6 CHUYÊN ĐỀ\n\n", "h1")
        t.insert(tk.END, "Chi tiết 6 Tab chuyên đề:\n", "h2")
        t.insert(tk.END, "• Tab 1: Phương trình, BPT & Hệ (Tham số m, Số phức): Dấu <=, >=, nhân ngầm 2x, cô lập m lập bảng biến thiên, giải số phức z, z_bar.\n", "bullet")
        t.insert(tk.END, "• Tab 2: Cực trị VDC & Bất đẳng thức: Tối ưu Nelder-Mead kết hợp Lagrange, bản đồ đường mức Contour.\n", "bullet")
        t.insert(tk.END, "• Tab 3: Vi tích phân: Đạo hàm riêng ∂f/∂x, tích phân, chuỗi Taylor.\n", "bullet")
        t.insert(tk.END, "• Tab 4: Ma trận: Định thức det(A), nghịch đảo A⁻¹, hạng rank(A), tích A x B, giải AX = B.\n", "bullet")
        t.insert(tk.END, "• Tab 5: Xác suất & Thống kê: x̄, Me, Mo, s², s, tứ phân vị, Histogram và Boxplot.\n", "bullet")
        t.insert(tk.END, "• Tab 6: Khảo sát hàm số Oxy: 12 bước khảo sát, cực trị, điểm uốn, tiệm cận, tiếp tuyến.\n\n", "bullet")

    def _content_geosolver_tools_vi(self):
        t = self.txt
        t.insert(tk.END, "3. GEOSOLVER 2D CAD STUDIO: DỰNG HÌNH & ELIP\n\n", "h1")
        t.insert(tk.END, "Công cụ vẽ Elip 2 tiêu điểm:\n", "h2")
        t.insert(tk.END, "1. Click chọn tiêu điểm F1.\n2. Click tiêu điểm F2 (xuất hiện đường elip xem trước trực quan co giãn theo chuột).\n3. Click điểm M trên đường elip.\n", "body")
        t.insert(tk.END, "• Tự động tính tâm O, bán trục a, b, tiêu cự 2c, diện tích, chu vi. Kéo rê di chuyển toàn bộ elip mượt mà.\n\n", "body")
        t.insert(tk.END, "Bản vẽ sạch chuẩn mực:\n", "h2")
        t.insert(tk.END, "Đã loại bỏ toàn bộ các dòng chữ xám phụ làm rối hình (tia BI, d vuông góc). Chỉ hiển thị hình học, tên điểm và ký hiệu vuông góc.\n\n", "body")

    def _content_invariants_and_ghost_vi(self):
        t = self.txt
        t.insert(tk.END, "4. QUAN HỆ TỰ ĐỘNG & CHẾ ĐỘ NÉT ẨN\n\n", "h1")
        t.insert(tk.END, "Hiển thị dạng căn thức chính xác (chống ảo giác):\n", "h2")
        t.insert(tk.END, "Hệ thống tự động rút gọn độ dài các cạnh về dạng căn thức (Ví dụ: AB = AC = √34 (≈ 5.83), đáy BC = 6), phân biệt rạch ròi tam giác cân và tam giác đều, loại bỏ hoàn toàn sai số làm tròn.\n\n", "body")
        t.insert(tk.END, "Chế độ Nét ẩn (Ghost Mode):\n", "h2")
        t.insert(tk.END, "• Ẩn đối tượng: Bấm [Ẩn/Hiện] để giấu đường phụ.\n• Nét mờ: Bấm khi không chọn gì để xem nét mờ #adb5bd.\n• Khôi phục tất cả: Chuột phải vào [Ẩn/Hiện] hoặc menu Tùy chọn -> Hiện lại tất cả đối tượng ẩn.\n\n", "body")

    def _content_shortcuts_vi(self):
        t = self.txt
        t.insert(tk.END, "5. BẢNG TRA CỨU PHÍM TẮT TOÀN TẬP\n\n", "h1")
        self._content_shortcuts_en()

    def _content_protips_vi(self):
        t = self.txt
        t.insert(tk.END, "6. MẸO & KINH NGHIỆM TỐI ƯU HÓA THAO TÁC\n\n", "h1")
        t.insert(tk.END, "💡 Mẹo 1: Sao chép ảnh dán thẳng vào Word (Ctrl+V) không qua file trung gian.\n\n", "box")
        t.insert(tk.END, "💡 Mẹo 2: Xuất hình vẽ đề thi dùng Auto-crop cắt sát hình kèm lề an toàn 25px.\n\n", "box")
        t.insert(tk.END, "💡 Mẹo 3: Soạn đề bài nhanh với các nút ký hiệu ∠, |x|, cos, √, π.\n\n", "box")


def show_stem_handbook_dialog(parent=None, initial_tab=0, initial_lang="en"):
    """
    Hàm khởi chạy cửa sổ Hướng dẫn sử dụng GeoSolver 2D duy nhất (Singleton).
    Mặc định ngôn ngữ là TIẾNG ANH (initial_lang='en') theo yêu cầu người dùng.
    """
    global _ACTIVE_DIALOG
    if _ACTIVE_DIALOG is not None and _ACTIVE_DIALOG.winfo_exists():
        _ACTIVE_DIALOG.switch_topic(initial_tab)
        _ACTIVE_DIALOG.deiconify()
        _ACTIVE_DIALOG.lift()
        _ACTIVE_DIALOG.focus_set()
        return _ACTIVE_DIALOG

    dlg = STEMHandbookDialog(parent=parent, initial_tab=initial_tab, initial_lang=initial_lang)
    _ACTIVE_DIALOG = dlg
    return dlg


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    dlg = show_stem_handbook_dialog(root, initial_tab=0, initial_lang="en")
    dlg.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
