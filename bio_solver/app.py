# -*- coding: utf-8 -*-
"""
Module: app.py
Đường dẫn: D:\\AI DATA\\STEM_APP\\bio_solver\\app.py
Mô tả: Giao diện Desktop Tkinter cho phần mềm giáo dục Sinh học (Biology Solver).
Phong cách: MS Office 2003 / Sư phạm kỹ thuật (Nền xám #F0F0F0, phông Tahoma/Segoe UI).
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox
import itertools
from collections import defaultdict

# ==============================================================================
# IMPORT HOẶC GIẢ LẬP STEM_SHARED_CORE (Để chạy độc lập không lỗi)
# ==============================================================================
try:
    from stem_shared_core.biology import solve_mendelian_cross, analyze_hardy_weinberg
    from stem_shared_core.i18n import t, set_language
    from stem_shared_core.hf_downloader import ask_download_model
except ImportError:
    # --- MOCK LÕI DỰ PHÒNG NẾU CHƯA CÓ MODULE ---
    CURRENT_LANG = "vi"
    TRANSLATIONS = {
        "vi": {
            "app_title": "STEM Biology Solver - Educational Edition",
            "btn_mendel": "🧬\nMen-đen",
            "btn_hw": "📊\nHacđi-Vanbec",
            "btn_lang": "🌐\nNgôn ngữ",
            "btn_ai": "🤖\nTải AI",
            "tab_mendel_title": "MÔ PHỎNG PHÉP LAI DI TRUYỀN MEN-ĐEN",
            "tab_hw_title": "CÂN BẰNG DI TRUYỀN QUẦN THỂ HACĐI - VANBEC",
            "input_p": "Nhập kiểu gen P",
            "father": "Bố (Parent 1):",
            "mother": "Mẹ (Parent 2):",
            "btn_analyze": "Phân tích phép lai",
            "res_ratios": "Tỷ lệ kiểu gen & kiểu hình F1",
            "geno_ratio": "Tỷ lệ kiểu gen:",
            "pheno_ratio": "Tỷ lệ kiểu hình:",
            "punnett": "Bàn cờ Punnett (Punnett Square)",
            "hw_input": "Thông số Quần thể",
            "q2_input": "Tần số kiểu hình lặn q² (aa):",
            "btn_hw_calc": "Tính trạng thái cân bằng",
            "hw_results": "Phân tích Cấu trúc Di truyền",
            "freq_p": "Tần số alen trội p(A):",
            "freq_q": "Tần số alen lặn q(a):",
            "freq_AA": "Tỷ lệ kiểu gen AA:",
            "freq_Aa": "Tỷ lệ kiểu gen Aa:",
            "freq_aa": "Tỷ lệ kiểu gen aa:",
            "eq_str": "Phương trình cân bằng:",
            "err_title": "Lỗi",
            "err_msg": "Dữ liệu nhập không hợp lệ."
        },
        "en": {
            "app_title": "STEM Biology Solver - Educational Edition",
            "btn_mendel": "🧬\nMendelian",
            "btn_hw": "📊\nHardy-Weinb",
            "btn_lang": "🌐\nLanguage",
            "btn_ai": "🤖\nLoad AI",
            "tab_mendel_title": "MENDELIAN GENETICS SIMULATION",
            "tab_hw_title": "HARDY-WEINBERG POPULATION EQUILIBRIUM",
            "input_p": "Parental Genotypes (P)",
            "father": "Parent 1:",
            "mother": "Parent 2:",
            "btn_analyze": "Analyze Cross",
            "res_ratios": "F1 Genotype & Phenotype Ratios",
            "geno_ratio": "Genotype Ratio:",
            "pheno_ratio": "Phenotype Ratio:",
            "punnett": "Punnett Square",
            "hw_input": "Population Parameters",
            "q2_input": "Recessive Phenotype Freq q² (aa):",
            "btn_hw_calc": "Calculate Equilibrium",
            "hw_results": "Genetic Structure Analysis",
            "freq_p": "Dominant allele freq p(A):",
            "freq_q": "Recessive allele freq q(a):",
            "freq_AA": "Genotype AA ratio:",
            "freq_Aa": "Genotype Aa ratio:",
            "freq_aa": "Genotype aa ratio:",
            "eq_str": "Equilibrium equation:",
            "err_title": "Error",
            "err_msg": "Invalid input data."
        }
    }

    def set_language(lang):
        global CURRENT_LANG
        CURRENT_LANG = lang

    def t(key):
        return TRANSLATIONS[CURRENT_LANG].get(key, key)

    def _get_gametes(geno):
        if len(geno) == 2:
            return list(set(geno))
        elif len(geno) == 4:
            g = [geno[0:2], geno[2:4]]
            return list(set([a+b for a, b in itertools.product(g[0], g[1])]))
        return []

    def _combine(g1, g2):
        if len(g1) == 1:
            return "".join(sorted([g1, g2], key=lambda x: (0 if x.isupper() else 1)))
        else:
            p1 = "".join(sorted([g1[0], g2[0]], key=lambda x: (0 if x.isupper() else 1)))
            p2 = "".join(sorted([g1[1], g2[1]], key=lambda x: (0 if x.isupper() else 1)))
            return p1 + p2

    def solve_mendelian_cross(p1, p2):
        g1 = _get_gametes(p1)
        g2 = _get_gametes(p2)
        if not g1 or not g2 or len(p1) != len(p2):
            raise ValueError("Invalid genotypes")
        
        # Hardcode ratio strings for common crosses to simplify the mock
        if p1 == "Aa" and p2 == "Aa":
            g_ratio = "1 AA : 2 Aa : 1 aa"
            p_ratio = "3 A- : 1 aa"
        elif p1 == "AaBb" and p2 == "AaBb":
            g_ratio = "1 AABB : 2 AABb : ... : 1 aabb"
            p_ratio = "9 A-B- : 3 A-bb : 3 aaB- : 1 aabb"
        else:
            g_ratio = "Calculated Genotypes"
            p_ratio = "Calculated Phenotypes"
            
        return {
            "gametes_1": sorted(g1),
            "gametes_2": sorted(g2),
            "genotype_ratio_str": g_ratio,
            "phenotype_ratio_str": p_ratio,
            "matrix": [g1, g2] # Custom for GUI drawing
        }

    def analyze_hardy_weinberg(recessive_phenotype_freq):
        if not (0 <= recessive_phenotype_freq <= 1):
            raise ValueError
        q = math.sqrt(recessive_phenotype_freq)
        p = 1.0 - q
        return {
            "allele_frequencies": {"p_A": p, "q_a": q},
            "equilibrium_genotype_frequencies": {"AA": p**2, "Aa": 2*p*q, "aa": q**2},
            "equation_str": f"{p**2:.4f}AA + {2*p*q:.4f}Aa + {q**2:.4f}aa = 1"
        }

    def ask_download_model(parent):
        messagebox.showinfo("Tải AI", "Hệ thống giả lập: Đang tải mô hình HuggingFace AI...", parent=parent)


# ==============================================================================
# CẤU HÌNH GIAO DIỆN (UI CONFIG)
# ==============================================================================
BG_COLOR = "#F0F0F0"
CANVAS_BG = "#FAFAFA"
FONT_NORMAL = ("Tahoma", 9)
FONT_BOLD = ("Tahoma", 9, "bold")
FONT_TITLE = ("Tahoma", 10, "bold")
FONT_ICON = ("Segoe UI", 8)


class BioSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(t("app_title"))
        self.geometry("900x650")
        self.configure(bg=BG_COLOR)
        
        # Áp dụng theme cổ điển (Office 2003)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure(".", background=BG_COLOR, font=FONT_NORMAL)
        self.style.configure("TLabelframe", background=BG_COLOR, borderwidth=2, relief=tk.GROOVE)
        self.style.configure("TLabelframe.Label", font=FONT_BOLD, background=BG_COLOR, foreground="#333333")
        self.style.configure("TButton", font=FONT_NORMAL)
        
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

        self.btn_mendel = tk.Button(self.toolbar, command=lambda: self.notebook.select(0), **btn_opts)
        self.btn_mendel.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_hw = tk.Button(self.toolbar, command=lambda: self.notebook.select(1), **btn_opts)
        self.btn_hw.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        self.btn_lang = tk.Button(self.toolbar, command=self.toggle_language, **btn_opts)
        self.btn_lang.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_ai = tk.Button(self.toolbar, command=lambda: ask_download_model(self), **btn_opts)
        self.btn_ai.pack(side=tk.LEFT, padx=2, pady=2)
        
        for btn in (self.btn_mendel, self.btn_hw, self.btn_lang, self.btn_ai):
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

    def _build_main_area(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # TAB 1: MEN-ĐEN
        self.tab_mendel = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_mendel, text="Tab1")
        self._build_mendel_tab()

        # TAB 2: HARDY-WEINBERG
        self.tab_hw = tk.Frame(self.notebook, bg=BG_COLOR)
        self.notebook.add(self.tab_hw, text="Tab2")
        self._build_hw_tab()

    # ==========================================================================
    # GIAO DIỆN TAB 1: MEN-ĐEN & BÀN CỜ PUNNETT
    # ==========================================================================
    def _build_mendel_tab(self):
        self.lbl_title_mendel = tk.Label(self.tab_mendel, font=FONT_TITLE, bg=BG_COLOR, fg="#003366")
        self.lbl_title_mendel.pack(anchor=tk.W, pady=(0, 5))

        # --- Khu vực trên: Nhập liệu và Tỷ lệ ---
        top_frame = tk.Frame(self.tab_mendel, bg=BG_COLOR)
        top_frame.pack(fill=tk.X, pady=5)

        # Trái: Nhập liệu
        self.lf_mendel_in = ttk.LabelFrame(top_frame)
        self.lf_mendel_in.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        self.lbl_p1 = tk.Label(self.lf_mendel_in, bg=BG_COLOR)
        self.lbl_p1.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_p1 = tk.Entry(self.lf_mendel_in, width=10, font=FONT_BOLD, relief=tk.SUNKEN, bd=2)
        self.ent_p1.insert(0, "AaBb")
        self.ent_p1.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_p2 = tk.Label(self.lf_mendel_in, bg=BG_COLOR)
        self.lbl_p2.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_p2 = tk.Entry(self.lf_mendel_in, width=10, font=FONT_BOLD, relief=tk.SUNKEN, bd=2)
        self.ent_p2.insert(0, "AaBb")
        self.ent_p2.grid(row=1, column=1, padx=5, pady=5)

        self.btn_analyze = tk.Button(self.lf_mendel_in, command=self.process_mendel,
                                     bg="#D4D0C8", relief=tk.RAISED, bd=2)
        self.btn_analyze.grid(row=2, column=0, columnspan=2, pady=10, ipadx=10)

        # Phải: Hiển thị Tỷ lệ
        self.lf_mendel_res = ttk.LabelFrame(top_frame)
        self.lf_mendel_res.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.var_g_ratio = tk.StringVar(value="-")
        self.var_p_ratio = tk.StringVar(value="-")

        self.lbl_gr = tk.Label(self.lf_mendel_res, bg=BG_COLOR, font=FONT_BOLD)
        self.lbl_gr.grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
        tk.Label(self.lf_mendel_res, textvariable=self.var_g_ratio, bg=BG_COLOR, fg="#800000",
                 font=("Consolas", 10, "bold")).grid(row=0, column=1, sticky=tk.W, padx=5)

        self.lbl_pr = tk.Label(self.lf_mendel_res, bg=BG_COLOR, font=FONT_BOLD)
        self.lbl_pr.grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        tk.Label(self.lf_mendel_res, textvariable=self.var_p_ratio, bg=BG_COLOR, fg="#006600",
                 font=("Consolas", 10, "bold")).grid(row=1, column=1, sticky=tk.W, padx=5)

        # --- Khu vực dưới: Bàn cờ Punnett ---
        self.lf_punnett = ttk.LabelFrame(self.tab_mendel)
        self.lf_punnett.pack(fill=tk.BOTH, expand=True, pady=10)

        self.canvas = tk.Canvas(self.lf_punnett, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # ==========================================================================
    # GIAO DIỆN TAB 2: HARDY-WEINBERG
    # ==========================================================================
    def _build_hw_tab(self):
        self.lbl_title_hw = tk.Label(self.tab_hw, font=FONT_TITLE, bg=BG_COLOR, fg="#003366")
        self.lbl_title_hw.pack(anchor=tk.W, pady=(0, 10))

        main_frame = tk.Frame(self.tab_hw, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Trái: Nhập liệu
        self.lf_hw_in = ttk.LabelFrame(main_frame)
        self.lf_hw_in.grid(row=0, column=0, sticky=tk.N, padx=(0, 10))

        self.lbl_q2 = tk.Label(self.lf_hw_in, bg=BG_COLOR)
        self.lbl_q2.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.ent_q2 = tk.Entry(self.lf_hw_in, width=15, relief=tk.SUNKEN, bd=2)
        self.ent_q2.insert(0, "0.16")
        self.ent_q2.grid(row=0, column=1, padx=10, pady=10)

        self.btn_hw_calc = tk.Button(self.lf_hw_in, command=self.process_hw,
                                     bg="#D4D0C8", relief=tk.RAISED, bd=2)
        self.btn_hw_calc.grid(row=1, column=0, columnspan=2, pady=15, ipadx=10)

        # Phải: Kết quả
        self.lf_hw_res = ttk.LabelFrame(main_frame)
        self.lf_hw_res.grid(row=0, column=1, sticky=tk.N)

        self.hw_vars = {
            "p": tk.StringVar(), "q": tk.StringVar(),
            "AA": tk.StringVar(), "Aa": tk.StringVar(), "aa": tk.StringVar(),
            "eq": tk.StringVar()
        }
        self.hw_labels = {}

        keys_ui = ["freq_p", "freq_q", "freq_AA", "freq_Aa", "freq_aa", "eq_str"]
        keys_var = ["p", "q", "AA", "Aa", "aa", "eq"]

        for idx, (k_ui, k_var) in enumerate(zip(keys_ui, keys_var)):
            lbl = tk.Label(self.lf_hw_res, bg=BG_COLOR, font=FONT_BOLD)
            lbl.grid(row=idx, column=0, sticky=tk.W, padx=10, pady=8)
            self.hw_labels[k_ui] = lbl
            
            fg_color = "#800000" if k_var == "eq" else "#000080"
            font_st = FONT_BOLD if k_var == "eq" else FONT_NORMAL
            
            tk.Label(self.lf_hw_res, textvariable=self.hw_vars[k_var], bg=BG_COLOR, 
                     fg=fg_color, font=font_st, relief=tk.GROOVE, bd=2, width=30, anchor=tk.E).grid(row=idx, column=1, padx=10, pady=8)

    # ==========================================================================
    # LOGIC NGÔN NGỮ (I18N)
    # ==========================================================================
    def toggle_language(self):
        self.lang_mode = "en" if self.lang_mode == "vi" else "vi"
        set_language(self.lang_mode)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.title(t("app_title"))
        self.btn_mendel.config(text=t("btn_mendel"))
        self.btn_hw.config(text=t("btn_hw"))
        self.btn_lang.config(text=t("btn_lang"))
        self.btn_ai.config(text=t("btn_ai"))
        
        # Tab Mendel
        self.lbl_title_mendel.config(text=t("tab_mendel_title"))
        self.lf_mendel_in.config(text=t("input_p"))
        self.lbl_p1.config(text=t("father"))
        self.lbl_p2.config(text=t("mother"))
        self.btn_analyze.config(text=t("btn_analyze"))
        self.lf_mendel_res.config(text=t("res_ratios"))
        self.lbl_gr.config(text=t("geno_ratio"))
        self.lbl_pr.config(text=t("pheno_ratio"))
        self.lf_punnett.config(text=t("punnett"))

        # Tab HW
        self.lbl_title_hw.config(text=t("tab_hw_title"))
        self.lf_hw_in.config(text=t("hw_input"))
        self.lbl_q2.config(text=t("q2_input"))
        self.btn_hw_calc.config(text=t("btn_hw_calc"))
        self.lf_hw_res.config(text=t("hw_results"))
        
        for k_ui, lbl in self.hw_labels.items():
            lbl.config(text=t(k_ui))

    # ==========================================================================
    # LOGIC SỰ KIỆN: MEN-ĐEN & PUNNETT SQUARE
    # ==========================================================================
    def process_mendel(self):
        p1 = self.ent_p1.get().strip()
        p2 = self.ent_p2.get().strip()
        try:
            res = solve_mendelian_cross(p1, p2)
            self.var_g_ratio.set(res.get("genotype_ratio_str", ""))
            self.var_p_ratio.set(res.get("phenotype_ratio_str", ""))
            
            # Gọi hàm vẽ lưới
            self.update_idletasks() # Đảm bảo canvas đã resize trước khi vẽ
            self.draw_punnett_square(res.get("gametes_1", []), res.get("gametes_2", []))
            
        except ValueError:
            messagebox.showerror(t("err_title"), t("err_msg"), parent=self)

    def draw_punnett_square(self, g1_list, g2_list):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if not g1_list or not g2_list or w < 50 or h < 50:
            return

        cols = len(g1_list) + 1
        rows = len(g2_list) + 1
        
        # Để margin nhỏ
        margin = 10
        cell_w = (w - 2*margin) / cols
        cell_h = (h - 2*margin) / rows

        # Vẽ tiêu đề giao tử (Màu nền nhạt #E8E8E8)
        for c, gamete in enumerate(g1_list):
            x1 = margin + (c + 1) * cell_w
            y1 = margin
            self.canvas.create_rectangle(x1, y1, x1+cell_w, y1+cell_h, fill="#E8E8E8", outline="#A0A0A0")
            self.canvas.create_text(x1 + cell_w/2, y1 + cell_h/2, text=f"♂ {gamete}", font=FONT_BOLD)

        for r, gamete in enumerate(g2_list):
            x1 = margin
            y1 = margin + (r + 1) * cell_h
            self.canvas.create_rectangle(x1, y1, x1+cell_w, y1+cell_h, fill="#E8E8E8", outline="#A0A0A0")
            self.canvas.create_text(x1 + cell_w/2, y1 + cell_h/2, text=f"♀ {gamete}", font=FONT_BOLD)

        # Ô gốc cùng bên trái trên
        self.canvas.create_rectangle(margin, margin, margin+cell_w, margin+cell_h, fill="#D0D0D0", outline="#A0A0A0")
        self.canvas.create_line(margin, margin, margin+cell_w, margin+cell_h, fill="#A0A0A0")

        # Vẽ tổ hợp hợp tử F1
        for r, g2 in enumerate(g2_list):
            for c, g1 in enumerate(g1_list):
                x1 = margin + (c + 1) * cell_w
                y1 = margin + (r + 1) * cell_h
                
                # Hàm mock nội bộ _combine nếu chạy giả lập, hoặc tự tính
                try:
                    zygote = _combine(g1, g2)
                except NameError:
                    zygote = g1 + g2 # Fallback an toàn

                self.canvas.create_rectangle(x1, y1, x1+cell_w, y1+cell_h, fill=CANVAS_BG, outline="#C0C0C0")
                self.canvas.create_text(x1 + cell_w/2, y1 + cell_h/2, text=zygote, font=("Consolas", 11, "bold"), fill="#000080")

    # ==========================================================================
    # LOGIC SỰ KIỆN: HARDY-WEINBERG
    # ==========================================================================
    def process_hw(self):
        try:
            q2 = float(self.ent_q2.get())
            res = analyze_hardy_weinberg(recessive_phenotype_freq=q2)
            
            p = res["allele_frequencies"]["p_A"]
            q = res["allele_frequencies"]["q_a"]
            AA = res["equilibrium_genotype_frequencies"]["AA"]
            Aa = res["equilibrium_genotype_frequencies"]["Aa"]
            aa = res["equilibrium_genotype_frequencies"]["aa"]
            
            self.hw_vars["p"].set(f"{p:.4f}")
            self.hw_vars["q"].set(f"{q:.4f}")
            self.hw_vars["AA"].set(f"{AA:.4f}  ({AA*100:.2f}%)")
            self.hw_vars["Aa"].set(f"{Aa:.4f}  ({Aa*100:.2f}%)")
            self.hw_vars["aa"].set(f"{aa:.4f}  ({aa*100:.2f}%)")
            self.hw_vars["eq"].set(res["equation_str"])
            
        except ValueError:
            messagebox.showerror(t("err_title"), t("err_msg"), parent=self)


if __name__ == "__main__":
    app = BioSolverApp()
    app.mainloop()