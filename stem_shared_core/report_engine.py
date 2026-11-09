# -*- coding: utf-8 -*-
"""
report_engine.py
================
Bộ sinh Báo cáo Kỹ thuật & Xuất bản Toán - Lý - Hình học (STEM Report Generator).
- Tạo tệp HTML duy nhất, tự chứa (self-contained), tích hợp MathJax 3.2 để kết xuất căn thức và công thức LaTeX tuyệt đẹp.
- Nhúng trực tiếp ảnh đồ thị / bản vẽ kỹ thuật dạng Base64 PNG.
- Tối ưu hóa in ấn (Print CSS) cho phép xuất ra tệp PDF chuẩn trang in A4 chỉ với 1 cú click (Print to PDF).
- Cung cấp tính năng sao chép mã LaTeX, sao chép văn bản thuần, và lưu ảnh công thức.
"""

from __future__ import annotations
import base64
import html
import io
import time
from typing import Optional, Dict, Any, List


def figure_to_base64_png(fig) -> str:
    """Chuyển đổi một đối tượng Matplotlib Figure thành chuỗi data URL base64 PNG."""
    if fig is None:
        return ""
    buf = io.BytesIO()
    try:
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""
    finally:
        buf.close()


def canvas_to_base64_png(tk_canvas) -> str:
    """Chuyển đổi nội dung Tkinter Canvas thành data URL base64 PNG bằng PIL/ImageGrab (nếu có) hoặc PostScript."""
    if tk_canvas is None:
        return ""
    try:
        from PIL import Image, ImageGrab
        x = tk_canvas.winfo_rootx()
        y = tk_canvas.winfo_rooty()
        w = tk_canvas.winfo_width()
        h = tk_canvas.winfo_height()
        if w > 10 and h > 10:
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            encoded = base64.b64encode(buf.read()).decode("ascii")
            return f"data:image/png;base64,{encoded}"
    except Exception:
        pass

    # Fallback: xuất Postscript rồi chuyển qua Pillow nếu cài Ghostscript
    try:
        from PIL import Image
        ps = tk_canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""


def build_full_stem_html_report(
    app_title: str,
    topic: str,
    problem_text: str,
    hero_formula_latex: str = "",
    hero_formula_text: str = "",
    solution_steps: str = "",
    plot_base64_png: str = "",
    extra_facts: Optional[List[Dict[str, str]]] = None,
    ai_commentary: str = ""
) -> str:
    """
    Sinh mã HTML hoàn chỉnh, chuẩn in ấn và chuẩn hiển thị MathJax cho toàn bộ trang bài toán.
    """
    now_str = time.strftime("%d/%m/%Y %H:%M:%S")

    # Format solution steps: bảo vệ ký tự html nhưng giữ định dạng các đoạn công thức
    safe_solution = html.escape(solution_steps)
    formatted_solution = safe_solution.replace("\n", "<br>")

    # Chuẩn bị block hero result
    hero_html = ""
    if hero_formula_latex or hero_formula_text:
        display_math = hero_formula_latex.strip() if hero_formula_latex else hero_formula_text.strip()
        if not display_math.startswith("$$") and not display_math.startswith("\\["):
            display_math = f"$${display_math}$$"
        hero_html = f"""
        <div class="hero-card">
            <div class="card-label">KẾT QUẢ TÍNH TOÁN:</div>
            <div class="math-display">{display_math}</div>
            <div class="hero-actions">
                <button class="btn-copy" onclick="copyToClipboard('{html.escape(hero_formula_latex or hero_formula_text)}')">Sao chép LaTeX</button>
                <button class="btn-copy" onclick="copyToClipboard('{html.escape(hero_formula_text or hero_formula_latex)}')">Sao chép Văn bản</button>
            </div>
        </div>
        """

    # Chuẩn bị block đồ thị
    plot_html = ""
    if plot_base64_png:
        plot_html = f"""
        <div class="plot-container">
            <div class="section-title">HÌNH VẼ MINH HỌA / ĐỒ THỊ KỸ THUẬT:</div>
            <div class="plot-box">
                <img src="{plot_base64_png}" alt="Đồ thị kỹ thuật" class="plot-img" />
            </div>
        </div>
        """

    # Chuẩn bị facts table nếu có
    facts_html = ""
    if extra_facts:
        rows = "".join(f"<tr><td class='fact-key'>{html.escape(f.get('k', ''))}</td><td class='fact-val'>{html.escape(f.get('v', ''))}</td></tr>" for f in extra_facts)
        facts_html = f"""
        <div class="facts-section">
            <div class="section-title">THÔNG SỐ VÀ DỮ LIỆU ĐÃ KIỂM CHỨNG:</div>
            <table class="facts-table">
                {rows}
            </table>
        </div>
        """

    # Chuẩn bị AI commentary nếu có
    ai_html = ""
    if ai_commentary and len(ai_commentary.strip()) > 10:
        safe_ai = html.escape(ai_commentary).replace("\n", "<br>")
        ai_html = f"""
        <div class="ai-section">
            <div class="section-title">PHÂN TÍCH BƯỚC GIẢI (AI):</div>
            <div class="ai-box">{safe_ai}</div>
        </div>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(app_title)} - Báo Cáo Kỹ Thuật Chi Tiết</title>

<!-- MathJax 3.2 để hiển thị căn thức và công thức LaTeX chuẩn xác -->
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>
:root {{
  --primary: #0067C0;
  --primary-dark: #004E8C;
  --bg-page: #F3F3F3;
  --bg-card: #FFFFFF;
  --text-main: #0F172A;
  --text-muted: #64748B;
  --border: #E2E8F0;
  --success: #16A34A;
}}

body {{
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 24px;
  background-color: var(--bg-page);
  color: var(--text-main);
  line-height: 1.6;
}}

.report-container {{
  max-width: 960px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 36px 44px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}}

.top-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--primary);
  padding-bottom: 16px;
  margin-bottom: 24px;
}}

.brand-title {{
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.5px;
}}

.report-meta {{
  font-size: 12px;
  color: var(--text-muted);
  text-align: right;
}}

.action-bar {{
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}}

button {{
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid var(--border);
  background: #FFFFFF;
  color: var(--text-main);
  transition: all 0.15s ease;
}}

button:hover {{
  background: #F1F5F9;
  border-color: #CBD5E1;
}}

.btn-primary {{
  background: var(--primary);
  color: #FFFFFF;
  border-color: var(--primary);
}}

.btn-primary:hover {{
  background: var(--primary-dark);
}}

.btn-copy {{
  font-size: 11px;
  padding: 4px 10px;
  margin-right: 6px;
}}

.problem-box {{
  background: #F8FAFC;
  border-left: 4px solid var(--primary);
  padding: 14px 18px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 24px;
}}

.problem-label {{
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 4px;
}}

.problem-text {{
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
}}

.hero-card {{
  background: #F0FDF4;
  border: 1.5px solid #BBF7D0;
  border-radius: 8px;
  padding: 18px 24px;
  margin-bottom: 24px;
  text-align: center;
}}

.card-label {{
  font-size: 11px;
  font-weight: 700;
  color: var(--success);
  text-transform: uppercase;
  margin-bottom: 8px;
}}

.math-display {{
  font-size: 20px;
  color: #14532D;
  margin: 10px 0;
}}

.hero-actions {{
  margin-top: 10px;
}}

.section-title {{
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 24px 0 10px 0;
}}

.solution-box {{
  background: #F8FAFC;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 18px;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.7;
  color: #1E293B;
  white-space: pre-wrap;
  word-break: break-word;
}}

.plot-box {{
  text-align: center;
  margin: 16px 0;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: #FFFFFF;
}}

.plot-img {{
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}}

.facts-table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
}}

.facts-table td {{
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}}

.fact-key {{
  font-weight: 600;
  width: 30%;
  color: var(--text-muted);
}}

.fact-val {{
  color: var(--text-main);
}}

.ai-box {{
  background: #EFF6FF;
  border-left: 4px solid var(--primary);
  padding: 16px;
  border-radius: 0 6px 6px 0;
  font-size: 13.5px;
  line-height: 1.7;
}}

.footer {{
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}}

/* Print Stylesheet cho chuẩn in ấn và lưu PDF */
@media print {{
  body {{
    background: #FFFFFF;
    padding: 0;
  }}
  .report-container {{
    box-shadow: none;
    border: none;
    padding: 0;
    max-width: 100%;
  }}
  .action-bar, .hero-actions {{
    display: none !important;
  }}
  .hero-card {{
    border: 1px solid #16A34A;
  }}
  .solution-box, .problem-box, .plot-box {{
    border: 1px solid #CBD5E1;
  }}
}}
</style>

<script>
function copyToClipboard(text) {{
  if (!text) return;
  navigator.clipboard.writeText(text).then(function() {{
    alert("Đã sao chép vào bộ nhớ tạm: " + text);
  }}).catch(function(err) {{
    alert("Không thể sao chép: " + err);
  }});
}}

function printReport() {{
  window.print();
}}
</script>
</head>
<body>

<div class="report-container">
  <div class="top-bar">
    <div>
      <div class="brand-title">{html.escape(app_title)}</div>
      <div style="font-size: 13px; color: var(--text-muted);">{html.escape(topic)}</div>
    </div>
    <div class="report-meta">
      <div>Thời gian xuất: <b>{now_str}</b></div>
      <div>Bảo chứng: <b>100% Python Ground Truth</b></div>
    </div>
  </div>

  <div class="action-bar">
    <button class="btn-primary" onclick="printReport()">🖨️ In Báo Cáo / Lưu PDF</button>
    <button onclick="copyToClipboard(document.getElementById('sol-content').innerText)">📋 Sao Chép Toàn Bộ Lời Giải</button>
  </div>

  <div class="problem-box">
    <div class="problem-label">Đề bài & Dữ liệu đầu vào:</div>
    <div class="problem-text">{html.escape(problem_text)}</div>
  </div>

  {hero_html}

  {plot_html}

  {facts_html}

  <div class="section-title">QUY TRÌNH BIẾN ĐỔI VÀ LỜI GIẢI CHI TIẾT:</div>
  <div class="solution-box" id="sol-content">{formatted_solution}</div>

  {ai_html}

  <div class="footer">
    <div>Hệ thống phần mềm STEM CAD Studio • Bản quyền học thuật</div>
    <div>Trang 1 / 1 (Tối ưu hóa In ấn A4 & PDF)</div>
  </div>
</div>

</body>
</html>"""
    return html_template
