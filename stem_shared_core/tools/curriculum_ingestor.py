# -*- coding: utf-8 -*-
"""
curriculum_ingestor.py
======================
Trình nạp và chuẩn hóa đề thi đa nguồn (Universal Problem Ingestor):
1. Đọc file văn bản thô (.txt, .md, .docx, .json) từ người dùng dán vào.
2. Tự động chuyển đổi thành cấu trúc chuẩn problem_schema.json.
3. Hỗ trợ sinh đề tự động (Procedural Generation) từ các dạng toán Olympic/Gaokao kinh điển.
"""

from __future__ import annotations
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def parse_raw_text_to_problems(raw_text: str, source_category: str = "olympic_vmo") -> List[Dict[str, Any]]:
    """
    Tự động phân tách các bài toán từ văn bản thô theo cú pháp:
    [Bài 1] hoặc Bài 1: hoặc Problem 1:
    """
    problems = []
    lines = raw_text.splitlines()
    problems = []
    current_num = None
    current_lines = []

    def flush_problem():
        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                p_id = f"{source_category.upper()}-{int(current_num or len(problems)+1):04d}"
                problems.append({
                    "problem_id": p_id,
                    "source": source_category,
                    "prompt": {"vi": text},
                    "parsed_status": "ready"
                })

    for line in lines:
        stripped = line.strip()
        m = re.match(r'^(?:Bài|Câu|Problem)\s*(\d+)[:\.\-]\s*(.*)$', stripped, re.IGNORECASE)
        if not m:
            m = re.match(r'^\[(\d+)\]\s*(.*)$', stripped)
        if m:
            flush_problem()
            current_num = m.group(1)
            current_lines = [m.group(2)] if m.group(2) else []
        else:
            if current_lines or stripped:
                current_lines.append(line)

    flush_problem()
    return problems

def save_ingested_problems(problems: List[Dict[str, Any]], target_file_path: Path):
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_metadata": {
            "source": "curriculum_ingestor",
            "total_problems": len(problems)
        },
        "problems": problems
    }
    with open(target_file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã nạp thành công {len(problems)} bài toán vào: {target_file_path}")

if __name__ == "__main__":
    sample_text = """
    Bài 1: Cho tam giác ABC nhọn nội tiếp đường tròn (O). Đường cao AH cắt (O) tại D. Chứng minh rằng tứ giác BCDE là hình thang cân.
    Bài 2: Giải hệ phương trình x^3 - 3x = y^3 - 3y và x^6 + y^6 = 1.
    Bài 3: Tìm tất cả các giá trị của tham số m để bất phương trình nghiệm đúng với mọi x thuộc R.
    """
    parsed = parse_raw_text_to_problems(sample_text, source_category="vmo_math")
    print(f"Đã phân tích được {len(parsed)} bài toán mẫu.")
