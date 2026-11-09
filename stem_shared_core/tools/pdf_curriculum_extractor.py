# -*- coding: utf-8 -*-
"""
pdf_curriculum_extractor.py
===========================
Công cụ tự động trích xuất các bài toán Đại số, Hệ phương trình, Phương trình vô tỉ,
và Bất đẳng thức từ tài liệu PDF trong thư mục D:\\AI DATA\\đại số.
Tự động đóng gói thành file Markdown / JSON chuẩn để nạp trực tiếp lên Gemini (Google AI Studio).
"""

from __future__ import annotations
import sys
import re
from pathlib import Path
import fitz  # PyMuPDF

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SOURCE_DIR = Path(r"D:\AI DATA\đại số")
OUTPUT_MD = Path(r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\TAP_DE_DAI_SO_VN_OLYMPIC_GEMINI.md")

def clean_text(text: str) -> str:
    """Làm sạch văn bản sau khi trích xuất từ PDF."""
    # Xóa các dòng trống lặp lại
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Xóa các header/footer dạng số trang đơn lẻ
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    return text.strip()

def extract_key_problems_from_pdfs():
    print(f"📂 Đang quét các tài liệu PDF trong: {SOURCE_DIR}")
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    print(f"🔎 Tìm thấy {len(pdf_files)} tài liệu chuyên khảo & đề thi:\n")

    md_lines = [
        "# BỘ ĐỀ TOÁN ĐẠI SỐ CHUYÊN SÂU & OLYMPIC VIỆT NAM (VMO / HSG TỈNH / VẬN DỤNG CAO)",
        "Tài liệu được trích xuất tự động từ nguồn tài liệu gốc tại `D:\\AI DATA\\đại số`.",
        "Dành cho: Chuyên gia Khảo thí & Thẩm định Sư phạm Gemini (Google AI Studio).",
        "\n" + "=" * 70 + "\n"
    ]

    total_extracted_pages = 0

    for pdf_path in pdf_files:
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            print(f"📄 Đang xử lý: {pdf_path.name} ({total_pages} trang)...")

            md_lines.append(f"## NGUỒN TÀI LIỆU: {pdf_path.stem.upper()}")
            md_lines.append(f"- **Tên file:** `{pdf_path.name}`")
            md_lines.append(f"- **Tổng số trang:** {total_pages}\n")

            # Để tối ưu ngữ cảnh, ta trích xuất các trang tiêu biểu chứa đề bài / bài tập
            # Với đề thi (ít trang): lấy toàn bộ
            # Với sách/chuyên đề dày (> 50 trang): lấy 15 trang đầu và các trang bài tập trọng tâm
            max_pages_to_extract = min(15, total_pages) if total_pages > 30 else total_pages

            extracted_text = []
            for page_idx in range(max_pages_to_extract):
                page_text = doc[page_idx].get_text()
                if page_text.strip():
                    extracted_text.append(f"### [Trang {page_idx + 1}]\n{clean_text(page_text)}\n")

            total_extracted_pages += len(extracted_text)
            md_lines.extend(extracted_text)
            md_lines.append("\n" + "-" * 50 + "\n")
            doc.close()
            print(f"   -> Đã trích xuất {len(extracted_text)} trang nội dung toán học.")

        except Exception as e:
            print(f"   ⚠️ Lỗi khi đọc {pdf_path.name}: {e}")

    # Ghi ra file Markdown
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("\n" + "=" * 70)
    print(f"🎉 HOÀN TẤT TRÍCH XUẤT! Đã đóng gói {total_extracted_pages} trang toán học.")
    print(f"💾 File Markdown đã sẵn sàng để tải lên Gemini tại:\n   👉 {OUTPUT_MD}")
    print("=" * 70)

if __name__ == "__main__":
    extract_key_problems_from_pdfs()
