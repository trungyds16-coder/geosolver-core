# -*- coding: utf-8 -*-
"""
Module: app.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\chem_solver\\app.py
Mô tả: Giao diện Desktop Tkinter cho phần mềm giáo dục Hóa học (Chemistry Solver).
Phong cách: MS Office 2003 / Kỹ thuật (Nền xám #F0F0F0, phông Tahoma/Segoe UI, viền Groove).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re

# ==============================================================================
# IMPORT HOẶC GIẢ LẬP STEM_SHARED_CORE (Để chạy độc lập không lỗi)
# ==============================================================================
try:
    from stem_shared_core.chemistry import balance_chemical_equation, calculate_solution_concentrations
    from stem_shared_core.i18n import t, set_language
    from stem_shared_core.hf_downloader import ask_download_model
except ImportError:
    # --- MOCK LÕI DỰ PHÒNG (Fallback) NẾU CHƯA CÓ MODULE ---
    CURRENT_LANG = "vi"
    TRANSLATIONS = {
        "vi": {
            "app_title": "STEM Chemistry Solver - Technical Edition",
            "btn_bal": "⚗️\nCân bằng",
            "btn_conc": "🧪\nNồng độ",
            "btn_lang": "🌐\nNgôn ngữ",
            "btn_ai": "🤖\nTải AI",
            "tab_bal_title": "CÂN BẰNG PHƯƠNG TRÌNH HÓA HỌC (MATRIX NULLSPACE)",
            "tab_conc_title": "TÍNH TOÁN & PHA CHẾ DUNG DỊCH",
            "input_eq": "Nhập phương trình phản ứng (dùng '->' hoặc '='):",
            "btn_balance": "Cân bằng ngay",
            "res_eq": "Phương trình cân bằng:",
            "res_check": "Bảng kiểm tra bảo toàn nguyên tố:",
            "col_elem": "Nguyên tố",
            "col_lhs": "Vế trái (Tham gia)",
            "col_rhs": "Vế phải (Sản phẩm)",
            "input_params": "Thông số Pha chế",
            "mass": "Khối lượng chất tan m (g):",
            "molar_mass": "Khối lượng mol M (g/mol):",
            "volume": "Thể tích dung dịch V (L):",
            "btn_calc": "Tính Nồng độ",
            "results": "Bảng Kết quả",
            "moles": "Số mol chất tan n (mol):",
            "molarity": "Nồng độ mol CM (mol/L):",
            "formula": "Công thức liên hệ:",
            "err_title": "Lỗi",
            "err_msg": "Vui lòng kiểm tra lại dữ liệu nhập vào."
        },
        "en": {
            "app_title": "STEM Chemistry Solver - Technical Edition",
            "btn_bal": "⚗️\nBalance",
            "btn_conc": "🧪\nConcentrate",
            "btn_lang": "🌐\nLanguage",
            "btn_ai": "🤖\nLoad AI",
            "tab_bal_title": "CHEMICAL EQUATION BALANCER (MATRIX NULLSPACE)",
            "tab_conc_title": "SOLUTION CONCENTRATION CALCULATION",
            "input_eq": "Enter chemical equation (use '->' or '='):",
            "btn_balance": "Balance Now",
            "res_eq": "Balanced Equation:",
            "res_check": "Element Conservation Check:",
            "col_elem": "Element",
            "col_lhs": "Left Hand Side (LHS)",
            "col_rhs": "Right Hand Side (RHS)",
            "input_params": "Preparation Parameters",
            "mass": "Solute mass m (g):",
            "molar_mass": "Molar mass M (g/mol):",
            "volume": "Solution volume V (L):",
            "btn_calc": "Calculate Concentration",
            "results": "Results Table",
            "moles": "Solute moles n (mol):",
            "molarity": "Molarity CM (mol/L):",
            "formula": "Related Formula:",
            "err_title": "Error",
            "err_msg": "Please verify your input data."
        }
    }

    def set_language(lang):
        global CURRENT_LANG
        CURRENT_LANG = lang

    def t(key):
        return TRANSLATIONS[CURRENT_LANG].get(key, key)

    def balance_chemical_equation(eq_str):
        """Mock function để minh họa bảng nguyên tố trên giao diện"""
        if "Fe + O2" in eq_str.replace(" ", ""):
            return {
                "balanced_equation": "4Fe + 3O2 -> 2Fe2O3",
                "elements": ["Fe", "O"],
                "check_data": {"Fe": (4, 4), "O": (6, 6)}
            }
        elif "Fe2(SO4)3+NaOH" in eq_str.replace(" ", ""):
            return {
                "balanced_equation": "Fe2(SO4)3 + 6NaOH -> 2Fe(OH)3 + 3Na2SO4",
                "elements": ["Fe", "S", "O", "Na", "H"],
                "check_data": {"Fe": (2, 2), "S": (3, 3), "O": (18, 18), "Na": (6, 6), "H": (6, 6)}
            }
        else:
            # Fake logic for other inputs
            return {
                "balanced_equation": eq_str.replace("=", "->").upper() + " (Mocked)",
                "elements": ["X"],
                "check_data": {"X": (1, 1)}
            }

    def calculate_solution_concentrations(m_solute_gram, molar_mass, v_solution_liter):
        if molar_mass <= 0 or v_solution_liter <= 0:
            raise ValueError("M and V must be > 0")
        n = m_solute_gram / molar_mass
        c_m = n / v_solution_liter
        return {"n_solute_mol": n, "C_M": c_m}

    def ask_download_model(parent):
        messagebox.showinfo("Tải AI", "Hệ thống giả lập: Đang tải mô hình HuggingFace AI...", parent=parent)


# ==============================================================================
# CẤU HÌNH GIAO DIỆN (UI CONFIG)
# ==============================================================================
BG_COLOR = "#F0F0F0"
WHITE_BG = "#FFFFFF"
FONT_NORMAL = ("Tahoma", 9)
FONT_BOLD = ("Tahoma", 10, "bold")
FONT_ICON = ("Segoe UI", 8)
FONT_CODE = ("Consolas", 14, "bold")


class ChemSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(t("app_title"))
        self.geometry("850x650")
        self.configure(bg=BG_COLOR)
        
        # Áp dụng theme cổ điển (Office 2003 / CAD style)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure(".", background=BG_COLOR, font=FONT_NORMAL)
        self.style.configure("TLabelframe", background=BG_COLOR, borderwidth=2, relief=tk.GROOVE)
        self.style.configure("TLabelframe.Label", font=FONT_BOLD, background=BG_COLOR, foreground="#333333")
        self.style.configure("TButton", font=FONT_NORMAL)
        self.style.configure("Treeview", font=FONT_NORMAL, rowheight=25)
        self.style.configure("Treeview.Heading", font=FONT_BOLD, background="#E8E8E8")
        
        # Ẩn tiêu đề Tab của Notebook
        self.style.layout("TNotebook.Tab", []) 

        self._build_toolbar()
        self._build_main_area()
        
        self.lang_mode = "vi"
        self.update_ui_texts()

    def _build_toolbar(self):
        """Thanh công cụ Toolbar trên cùng"""
        self.toolbar = tk.Frame(self, bg=BG_COLOR, bd=2, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_opts = {
            "font": FONT_ICON, "bg": BG_COLOR, "relief": tk.FLAT, 
            "bd": 1, "justify": tk.CENTER, "width": 10
        }

        self.btn_bal = tk.Button(self.toolbar, command=lambda: self.notebook.select(0), **btn_opts)
        self.btn_bal.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_conc = tk.Button(self.toolbar, command=lambda: self.notebook.select(1), **btn_opts)
        self.btn_conc.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        self.btn_lang = tk.Button(self.toolbar, command=self.toggle_language, **btn_opts)
        self.btn_lang.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_ai = tk.Button(self.toolbar, command=lambda: ask_download_model(self), **btn_opts)
        self.btn_ai.pack(side=tk.LEFT, padx=2, pady=2)
        
        for btn in (self.btn_bal, self.btn_conc, self.btn_lang, self.btn_ai):
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

    def _build_main_area(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # TAB 1: CÂN BẰNG PHƯƠNG TRÌNH
        self.tab_bal = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_bal, text="Tab1")
        self._build_balancing_tab()

        # TAB 2: NỒNG ĐỘ DUNG DỊCH
        self.tab_conc = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_conc, text="Tab2")
        self._build_concentration_tab()

    # ==========================================================================
    # GIAO DIỆN TAB 1: CÂN BẰNG PTHH
    # ==========================================================================
    def _build_balancing_tab(self):
        self.lbl_title_bal = tk.Label(self.tab_bal, font=FONT_BOLD, bg=BG_COLOR, fg="#003366")
        self.lbl_title_bal.pack(anchor=tk.W, pady=(0, 10))

        # --- Khu vực nhập liệu ---
        frame_input = tk.Frame(self.tab_bal, bg=BG_COLOR)
        frame_input.pack(fill=tk.X, pady=5)
        
        self.lbl_input_eq = tk.Label(frame_input, bg=BG_COLOR)
        self.lbl_input_eq.pack(anchor=tk.W)
        
        self.ent_eq = tk.Entry(frame_input, font=("Consolas", 12), relief=tk.SUNKEN, bd=2)
        self.ent_eq.insert(0, "Fe2(SO4)3 + NaOH -> Fe(OH)3 + Na2SO4")
        self.ent_eq.pack(fill=tk.X, pady=(5, 10), ipady=4)
        
        self.btn_balance_exec = tk.Button(frame_input, command=self.process_balancing,
                                          bg="#D4D0C8", relief=tk.RAISED, bd=2, font=FONT_BOLD)
        self.btn_balance_exec.pack(anchor=tk.W, ipadx=15, ipady=2)

        # --- Khu vực kết quả Kỹ thuật ---
        self.lf_res_bal = ttk.LabelFrame(self.tab_bal)
        self.lf_res_bal.pack(fill=tk.BOTH, expand=True, pady=15)

        self.lbl_res_eq = tk.Label(self.lf_res_bal, font=FONT_CODE, bg=WHITE_BG, fg="#800000", 
                                   relief=tk.SUNKEN, bd=2, anchor=tk.W, padx=10, pady=10)
        self.lbl_res_eq.pack(fill=tk.X, padx=10, pady=10)

        self.lbl_res_check = tk.Label(self.lf_res_bal, bg=BG_COLOR, font=FONT_BOLD)
        self.lbl_res_check.pack(anchor=tk.W, padx=10, pady=(5, 0))

        # Bảng Treeview kiểm tra nguyên tố
        cols = ("elem", "lhs", "rhs")
        self.tree_check = ttk.Treeview(self.lf_res_bal, columns=cols, show="headings", height=8)
        self.tree_check.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ==========================================================================
    # GIAO DIỆN TAB 2: NỒNG ĐỘ DUNG DỊCH
    # ==========================================================================
    def _build_concentration_tab(self):
        self.lbl_title_conc = tk.Label(self.tab_conc, font=FONT_BOLD, bg=BG_COLOR, fg="#003366")
        self.lbl_title_conc.pack(anchor=tk.W, pady=(0, 10))

        main_frame = tk.Frame(self.tab_conc, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Cột trái: Nhập thông số ---
        self.lf_conc_input = ttk.LabelFrame(main_frame)
        self.lf_conc_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.lbl_mass = tk.Label(self.lf_conc_input, bg=BG_COLOR)
        self.lbl_mass.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.ent_mass = tk.Entry(self.lf_conc_input, width=15, relief=tk.SUNKEN, bd=2)
        self.ent_mass.insert(0, "5.85")
        self.ent_mass.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_molar = tk.Label(self.lf_conc_input, bg=BG_COLOR)
        self.lbl_molar.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.ent_molar = tk.Entry(self.lf_conc_input, width=15, relief=tk.SUNKEN, bd=2)
        self.ent_molar.insert(0, "58.5")
        self.ent_molar.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_vol = tk.Label(self.lf_conc_input, bg=BG_COLOR)
        self.lbl_vol.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.ent_vol = tk.Entry(self.lf_conc_input, width=15, relief=tk.SUNKEN, bd=2)
        self.ent_vol.insert(0, "0.5")
        self.ent_vol.grid(row=2, column=1, padx=10, pady=10)

        self.btn_calc_conc = tk.Button(self.lf_conc_input, command=self.process_concentration,
                                       bg="#D4D0C8", relief=tk.RAISED, bd=2, font=FONT_BOLD)
        self.btn_calc_conc.grid(row=3, column=0, columnspan=2, pady=20, ipadx=10, ipady=2)

        # --- Cột phải: Kết quả ---
        self.lf_conc_res = ttk.LabelFrame(main_frame)
        self.lf_conc_res.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.var_moles = tk.StringVar()
        self.var_molarity = tk.StringVar()

        self.lbl_moles = tk.Label(self.lf_conc_res, bg=BG_COLOR, font=FONT_BOLD)
        self.lbl_moles.grid(row=0, column=0, sticky=tk.W, padx=10, pady=15)
        tk.Label(self.lf_conc_res, textvariable=self.var_moles, bg=BG_COLOR, fg="#000080", 
                 font=("Consolas", 11, "bold"), relief=tk.GROOVE, bd=2, width=15, anchor=tk.E).grid(row=0, column=1, padx=10, pady=15)

        self.lbl_molarity = tk.Label(self.lf_conc_res, bg=BG_COLOR, font=FONT_BOLD)
        self.lbl_molarity.grid(row=1, column=0, sticky=tk.W, padx=10, pady=15)
        tk.Label(self.lf_conc_res, textvariable=self.var_molarity, bg=BG_COLOR, fg="#006600", 
                 font=("Consolas", 11, "bold"), relief=tk.GROOVE, bd=2, width=15, anchor=tk.E).grid(row=1, column=1, padx=10, pady=15)

        self.lbl_formula = tk.Label(self.lf_conc_res, bg=BG_COLOR, font=FONT_NORMAL, fg="#555555")
        self.lbl_formula.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=20)


    # ==========================================================================
    # LOGIC NGÔN NGỮ (I18N)
    # ==========================================================================
    def toggle_language(self):
        self.lang_mode = "en" if self.lang_mode == "vi" else "vi"
        set_language(self.lang_mode)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.title(t("app_title"))
        self.btn_bal.config(text=t("btn_bal"))
        self.btn_conc.config(text=t("btn_conc"))
        self.btn_lang.config(text=t("btn_lang"))
        self.btn_ai.config(text=t("btn_ai"))
        
        # Tab 1 texts
        self.lbl_title_bal.config(text=t("tab_bal_title"))
        self.lbl_input_eq.config(text=t("input_eq"))
        self.btn_balance_exec.config(text=t("btn_balance"))
        self.lf_res_bal.config(text=t("results"))
        self.lbl_res_check.config(text=t("res_check"))
        
        self.tree_check.heading("elem", text=t("col_elem"))
        self.tree_check.heading("lhs", text=t("col_lhs"))
        self.tree_check.heading("rhs", text=t("col_rhs"))

        # Tab 2 texts
        self.lbl_title_conc.config(text=t("tab_conc_title"))
        self.lf_conc_input.config(text=t("input_params"))
        self.lf_conc_res.config(text=t("results"))
        self.lbl_mass.config(text=t("mass"))
        self.lbl_molar.config(text=t("molar_mass"))
        self.lbl_vol.config(text=t("volume"))
        self.btn_calc_conc.config(text=t("btn_calc"))
        
        self.lbl_moles.config(text=t("moles"))
        self.lbl_molarity.config(text=t("molarity"))
        self.lbl_formula.config(text=f"{t('formula')} CM = n / V  ;  n = m / M")

    # ==========================================================================
    # LOGIC XỬ LÝ SỰ KIỆN (EVENTS)
    # ==========================================================================
    def process_balancing(self):
        eq_input = self.ent_eq.get().strip()
        if not eq_input:
            return
            
        try:
            res = balance_chemical_equation(eq_input)
            
            # Hiển thị phương trình
            self.lbl_res_eq.config(text=res.get("balanced_equation", ""))
            
            # Cập nhật Treeview kiểm tra nguyên tố
            for row in self.tree_check.get_children():
                self.tree_check.delete(row)
                
            check_data = res.get("check_data", {})
            for elem in res.get("elements", []):
                counts = check_data.get(elem, (0, 0))
                # So sánh màu sắc, nếu lệch (lỗi bảo toàn) thì tô đỏ (dành cho hàm thực tế)
                self.tree_check.insert("", tk.END, values=(elem, counts[0], counts[1]))
                
        except Exception as e:
            messagebox.showerror(t("err_title"), f"{t('err_msg')}\nChi tiết: {str(e)}", parent=self)

    def process_concentration(self):
        try:
            m = float(self.ent_mass.get())
            M = float(self.ent_molar.get())
            V = float(self.ent_vol.get())
            
            res = calculate_solution_concentrations(m_solute_gram=m, molar_mass=M, v_solution_liter=V)
            
            self.var_moles.set(f"{res['n_solute_mol']:.4f}")
            self.var_molarity.set(f"{res['C_M']:.4f}")
            
        except ValueError:
            messagebox.showerror(t("err_title"), t("err_msg"), parent=self)


if __name__ == "__main__":
    app = ChemSolverApp()
    app.mainloop()