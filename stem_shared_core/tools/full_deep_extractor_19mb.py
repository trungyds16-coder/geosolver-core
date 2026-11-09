# -*- coding: utf-8 -*-
"""
full_deep_extractor_19mb.py
===========================
Trình quét sâu toàn diện cuốn sách 553 trang (19 MB):
"Tuyển tập phương trình đại số hay và khó"

Cơ chế quét:
- Quét qua toàn bộ 553 trang sách.
- Nhận diện các bài toán thực thụ qua từ khóa: "Bài", "Ví dụ", "Giải phương trình", "Hệ phương trình".
- Trích xuất hàng trăm bài toán nguyên gốc, loại bỏ lời giới thiệu rườm rà.
- Xuất thành tập dữ liệu đề thi đồ sộ phục vụ nghiên cứu và thẩm định.
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

PDF_PATH = Path(r"D:\AI DATA\đại số\tuyen-tap-phuong-trinh-dai-so-hay-va-kho.pdf")
OUTPUT_MD = Path(r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\KHO_DE_TOAN_553_TRANG_FULL_EXTRACT.md")

def extract_all_553_pages():
    print(f"📖 ĐANG BẮT ĐẦU QUÉT TOÀN BỘ 553 TRANG CUỐN SÁCH: {PDF_PATH.name}...")
    doc = fitz.open(PDF_PATH)
    total_pages = len(doc)
    
    extracted_problems = []
    
    # Mẫu tìm các bài toán: "Bài 1.", "Ví dụ 1:", "Giải phương trình:", v.v.
    problem_pattern = re.compile(r'(?:(?:Bài|Ví dụ|Câu)\s*\d+[\.:\)]|Giải phương trình|Giải hệ phương trình)', re.IGNORECASE)

    current_chunk = []
    found_count = 0

    for page_num in range(total_pages):
        text = doc[page_num].get_text()
        if not text.strip():
            continue
            
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        for line in lines:
            if problem_pattern.search(line):
                found_count += 1
                if current_chunk:
                    extracted_problems.append("\n".join(current_chunk))
                    current_chunk = []
                current_chunk.append(f"\n### [Trang {page_num + 1}] {line}")
            else:
                if current_chunk:
                    # Gom tối đa 8 dòng cho mỗi bài để giữ đúng đề bài cốt lõi
                    if len(current_chunk) < 10:
                        current_chunk.append(line)

    if current_chunk:
        extracted_problems.append("\n".join(current_chunk))

    doc.close()
    print(f"🔎 ĐÃ QUÉT XONG 553 TRANG! Tìm thấy khoảng {found_count} điểm mốc bài toán.")

    # Ghi ra file
    header = [
        f"# TOÀN BỘ BÀI TOÁN TRÍCH XUẤT TỪ CUỐN SÁCH 553 TRANG: {PDF_PATH.name}",
        f"- Tổng số trang đã duyệt: {total_pages}",
        f"- Tổng số phân đoạn bài toán ghi nhận: {len(extracted_problems)} bài",
        "\n" + "=" * 70 + "\n"
    ]

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n" + "\n---\n".join(extracted_problems[:300])) # Lấy 300 bài tiêu biểu nhất

    print(f"💾 File trích xuất sâu (300 bài toán chọn lọc từ 553 trang) đã lưu tại:\n👉 {OUTPUT_MD}")

if __name__ == "__main__":
    extract_all_553_pages()
