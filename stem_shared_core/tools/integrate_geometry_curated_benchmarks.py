# -*- coding: utf-8 -*-
"""
integrate_geometry_curated_benchmarks.py
========================================
Chuẩn hóa và tích hợp 14 bài toán Hình học kinh điển (2D & 3D) từ file:
gemini-code-1793959067652.json

Phân loại chuyên nghiệp:
1. Nhóm 3D (Châu Ngọc Hùng - Hình chóp, Lăng trụ, Nón, Trụ):
   -> Lưu vào: stem_shared_core/curricula/pedagogical_university/BENCHMARK_3D_CHAU_NGOC_HUNG.json
2. Nhóm 2D (IMO Shortlist, Sharygin Geometry Olympiad, Vietnam TST):
   -> Lưu vào: stem_shared_core/curricula/olympic_vmo_imo/BENCHMARK_2D_SHARYGIN_IMO_ELITE.json
3. Dọn dẹp file tạm để bảo đảm codebase chuyên nghiệp và sạch sẽ.
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
SOURCE_JSON = BASE_DIR / "stem_shared_core" / "evaluation" / "gemini-code-1793959067652.json"

DIR_3D = BASE_DIR / "stem_shared_core" / "curricula" / "pedagogical_university"
FILE_3D = DIR_3D / "BENCHMARK_3D_CHAU_NGOC_HUNG.json"

DIR_2D = BASE_DIR / "stem_shared_core" / "curricula" / "olympic_vmo_imo"
FILE_2D = DIR_2D / "BENCHMARK_2D_SHARYGIN_IMO_ELITE.json"

def process_and_distribute():
    if not SOURCE_JSON.exists():
        print(f"❌ Không tìm thấy {SOURCE_JSON}")
        return

    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        raw_problems = json.load(f)

    print(f"📥 Đang nạp và phân loại {len(raw_problems)} bài toán hình học đỉnh cao...")

    list_3d = []
    list_2d = []

    for item in raw_problems:
        p_id = item.get("problem_id", "")
        prompt = item.get("prompt", "")
        # Nếu prompt là string thì chuẩn hóa thành {"vi": prompt}
        if isinstance(prompt, str):
            prompt_obj = {"vi": prompt}
        else:
            prompt_obj = prompt

        clean_item = {
            "problem_id": p_id,
            "prompt": prompt_obj,
            "ground_truth": item.get("ground_truth", ""),
            "required_nodes": item.get("required_nodes", []),
            "pedagogical_rubric": item.get("pedagogical_rubric", "")
        }

        # Phân loại dựa trên problem_id hoặc nội dung
        if "CHAU_NGOC_HUNG" in p_id or "chóp" in str(prompt).lower() or "lăng trụ" in str(prompt).lower() or "nón" in str(prompt).lower() or "trụ" in str(prompt).lower():
            clean_item["dimension"] = "3D"
            clean_item["source"] = "Châu Ngọc Hùng - Hình học không gian THPT"
            list_3d.append(clean_item)
        else:
            clean_item["dimension"] = "2D"
            clean_item["source"] = "IMO Shortlist / Sharygin / TST Vietnam"
            list_2d.append(clean_item)

    # 1. Lưu kho 3D
    DIR_3D.mkdir(parents=True, exist_ok=True)
    payload_3d = {
        "dataset_metadata": {
            "dataset_id": "VN_GEOSOLVER_3D_CHAU_NGOC_HUNG_V1",
            "dimension": "3D",
            "total_problems": len(list_3d),
            "description": "Bộ bài toán Hình học Không gian 3D chuẩn mực sư phạm (Khoảng cách, Góc, Thể tích, Mặt nón, Mặt trụ) trích xuất từ tuyển tập Châu Ngọc Hùng."
        },
        "problems": list_3d
    }
    with open(FILE_3D, "w", encoding="utf-8") as f:
        json.dump(payload_3d, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã lưu {len(list_3d)} bài 3D vào:\n   👉 {FILE_3D}")

    # 2. Lưu kho 2D
    DIR_2D.mkdir(parents=True, exist_ok=True)
    payload_2d = {
        "dataset_metadata": {
            "dataset_id": "GLOBAL_OLYMPIC_2D_SHARYGIN_IMO_V1",
            "dimension": "2D",
            "total_problems": len(list_2d),
            "description": "Bộ bài toán Hình học Phẳng 2D đỉnh cao thế giới (Sharygin Geometry Olympiad, IMO Shortlist, Vietnam TST) kèm lời giải sư phạm và các bước dựng hình CAD."
        },
        "problems": list_2d
    }
    with open(FILE_2D, "w", encoding="utf-8") as f:
        json.dump(payload_2d, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã lưu {len(list_2d)} bài 2D vào:\n   👉 {FILE_2D}")

    # 3. Dọn dẹp file tạm
    if SOURCE_JSON.exists():
        SOURCE_JSON.unlink()
        print(f"🗑️ Đã dọn dẹp file tạm: {SOURCE_JSON.name}")

    print("🎉 TẤT CẢ DỮ LIỆU HÌNH HỌC ĐÃ ĐƯỢC CHUẨN HÓA VÀ BẢO LƯU 100%!")

if __name__ == "__main__":
    process_and_distribute()
