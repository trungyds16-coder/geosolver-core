# -*- coding: utf-8 -*-
"""
integrate_vmo_curated_benchmark.py
==================================
Chuẩn hóa và đồng bộ 15 bài toán Đại số đỉnh cao (VMO / Olympic / Vận dụng cao Việt Nam)
từ file tạm thời sang định dạng chuyên nghiệp:
- Đặt tên chuẩn học thuật: BENCHMARK_VN_VMO_ALGEBRA_ELITE.json
- Tích hợp vào thư mục: stem_shared_core/curricula/olympic_vmo_imo/
- Xóa bỏ các file tạm thời (gemini-code-*.json) để đảm bảo tính chuyên nghiệp.
"""

from __future__ import annotations
import sys
import json
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVAL_DIR = BASE_DIR / "stem_shared_core" / "evaluation"
NEW_TEMP_FILE = EVAL_DIR / "gemini-code-1793950153724.json"
OLD_TEMP_FILE = EVAL_DIR / "gemini-code-1793928104035.json"

TARGET_BENCHMARK_DIR = BASE_DIR / "stem_shared_core" / "curricula" / "olympic_vmo_imo"
TARGET_BENCHMARK_FILE = TARGET_BENCHMARK_DIR / "BENCHMARK_VN_VMO_ALGEBRA_ELITE.json"

def refine_and_integrate():
    if not NEW_TEMP_FILE.exists():
        print(f"❌ Không tìm thấy file nguồn: {NEW_TEMP_FILE}")
        return

    with open(NEW_TEMP_FILE, "r", encoding="utf-8") as f:
        problems = json.load(f)

    print(f"📂 Đang tinh chỉnh {len(problems)} bài toán Đại số VMO đỉnh cao...")

    # Chuẩn hóa cấu trúc gói dữ liệu
    payload = {
        "dataset_metadata": {
            "dataset_id": "VN_VMO_ALGEBRA_ELITE_2026_V1",
            "curriculum": "Vietnam National Mathematical Olympiad & High School Advanced",
            "total_problems": len(problems),
            "description": "Bộ 15 bài toán Đại số đỉnh cao (Hệ đối xứng, Phương trình vô tỉ đẳng cấp, Lượng giác hóa, Bất đẳng thức & Bẫy nghiệm ngoại lai) tuyển chọn từ tài liệu VMO và chuyên đề vận dụng cao."
        },
        "problems": problems
    }

    # Lưu vào thư mục curricula chuẩn
    TARGET_BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)
    with open(TARGET_BENCHMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✅ ĐÃ LƯU BỘ DỮ LIỆU CHUYÊN NGHIỆP TẠI:\n   👉 {TARGET_BENCHMARK_FILE}")

    # Xóa các file rác / tạm thời để giữ codebase gọn gàng
    files_to_clean = [NEW_TEMP_FILE, OLD_TEMP_FILE]
    for temp_f in files_to_clean:
        if temp_f.exists():
            temp_f.unlink()
            print(f"🗑️ Đã dọn dẹp file tạm: {temp_f.name}")

    print("🎉 QUY TRÌNH TINH CHỈNH & LÀM SẠCH HOÀN TẤT 100%!")

if __name__ == "__main__":
    refine_and_integrate()
