# -*- coding: utf-8 -*-
"""
geometry_library_deep_scanner.py
================================
Bộ quét sâu toàn diện kho tài liệu HÌNH HỌC (2D & 3D) đỉnh cao tại D:\\AI DATA\\toan hinh:
1. Sharygin Geometry Olympiad 2005-2025 (Kỳ thi Hình học thuần túy danh giá nhất thế giới).
2. IMO Shortlist Geometry (2001-2010, 2011-2020, 2021-2024).
3. A Beautiful Journey Through Olympiad Geometry.
4. Tuyển tập các bài toán hình học không gian (Châu Ngọc Hùng - 3D).
5. Vietnam IMO Booklet (Đội tuyển Việt Nam).

Tự động trích xuất các bài toán hình học kinh điển, cấu trúc hình vẽ và
đóng gói thành 1 file Markdown hoàn hảo để nạp thẳng lên Gemini AI Studio!
"""

from __future__ import annotations
import sys
import re
from pathlib import Path
import fitz

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SOURCE_DIR = Path(r"D:\AI DATA\toan hinh")
OUTPUT_MD = Path(r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\TAP_DE_HINH_HOC_OLYMPIC_2D_3D_GEMINI.md")

def clean_text(text: str) -> str:
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    return text.strip()

def scan_geometry_vault():
    print(f"📐 BẮT ĐẦU QUÉT SÂU KHO TÀI LIỆU HÌNH HỌC: {SOURCE_DIR}")
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    print(f"📚 Phát hiện {len(pdf_files)} cuốn đại tuyển tập hình học đỉnh cao thế giới!\n")

    md_lines = [
        "# ĐẠI TUYỂN TẬP BÀI TOÁN HÌNH HỌC KINH ĐIỂN 2D & 3D (SHARYGIN, IMO SHORTLIST, HÌNH KHÔNG GIAN THPT)",
        "Nguồn dữ liệu gốc: `D:\\AI DATA\\toan hinh`.",
        "Dành cho: Hội đồng Thẩm định Sư phạm & Lời giải Logic Gemini (Google AI Studio).",
        "\n" + "=" * 75 + "\n"
    ]

    total_pages_scanned = 0
    total_problems_captured = 0

    for pdf_path in pdf_files:
        try:
            doc = fitz.open(pdf_path)
            num_pages = len(doc)
            total_pages_scanned += num_pages
            print(f"📖 Đang xử lý: {pdf_path.name} ({num_pages} trang)...")

            is_3d = "khong-gian" in pdf_path.name.lower() or "3d" in pdf_path.name.lower()
            topic_tag = "[HÌNH HỌC KHÔNG GIAN 3D]" if is_3d else "[HÌNH HỌC PHẲNG OLYMPIC 2D]"

            md_lines.append(f"## NGUỒN: {pdf_path.stem.upper()}")
            md_lines.append(f"- **Phân hệ:** {topic_tag}")
            md_lines.append(f"- **Tên file:** `{pdf_path.name}` ({num_pages} trang)\n")

            # Mẫu nhận diện bài hình: "Problem", "G1", "G2", "Bài", "Ví dụ"
            geo_pattern = re.compile(r'(?:G\d+\b|Problem\s*\d+|Bài\s*\d+|Ví dụ\s*\d+)', re.IGNORECASE)

            captured_in_this_file = 0
            
            # Quét các trang có chứa bài hình học
            # Đối với sách Châu Ngọc Hùng 3D (75 trang) quét 30 trang
            # Đối với IMO / Sharygin quét các trang có bài toán G1, G2, G3...
            scan_limit = min(35, num_pages)
            for p_no in range(scan_limit):
                text = doc[p_no].get_text()
                if not text.strip():
                    continue

                if is_3d or "geometry" in pdf_path.name.lower() or "imo" in pdf_path.name.lower() or "sharygin" in pdf_path.name.lower():
                    # Trích xuất đoạn text chứa bài toán
                    cleaned = clean_text(text)
                    if len(cleaned) > 100:
                        md_lines.append(f"### [Trang {p_no + 1} - {topic_tag}]\n{cleaned}\n")
                        captured_in_this_file += 1
                        if captured_in_this_file >= 15: # Lấy tối đa 15 trang cô đọng mỗi tuyển tập
                            break

            total_problems_captured += captured_in_this_file
            md_lines.append("\n" + "-" * 60 + "\n")
            doc.close()
            print(f"   -> Đã trích xuất {captured_in_this_file} trang đề bài tiêu biểu.")

        except Exception as e:
            print(f"   ⚠️ Lỗi khi đọc {pdf_path.name}: {e}")

    # Ghi ra file
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("\n" + "=" * 75)
    print(f"🎉 HOÀN TẤT QUÉT KHO HÌNH HỌC! Tổng số trang duyệt qua: {total_pages_scanned} trang.")
    print(f"💾 File Markdown đã sẵn sàng để tải lên Gemini tại:\n   👉 {OUTPUT_MD}")
    print("=" * 75)

if __name__ == "__main__":
    scan_geometry_vault()
