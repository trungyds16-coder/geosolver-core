# -*- coding: utf-8 -*-
"""
distribute_benchmarks.py
========================
Tự động đọc file JSON bạn vừa tạo (gemini-code-1793928104035.json) và phân loại
chuẩn xác vào các thư mục chuyên môn tương ứng:
- cn_gaokao (Cao khảo Trung Quốc)
- olympic_vmo_imo (Toán Olympic quốc tế & VMO)
- us_k12 (Toán Mỹ: AIME, AMC)
"""

import sys
import json
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_JSON = BASE_DIR / "stem_shared_core" / "evaluation" / "gemini-code-1793928104035.json"

def distribute():
    if not SOURCE_JSON.exists():
        print(f"❌ Không tìm thấy {SOURCE_JSON}")
        return

    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        problems = json.load(f)

    print(f"📥 Đang nạp {len(problems)} bài toán đặc trưng từ {SOURCE_JSON.name}...")

    grouped = {
        "cn_gaokao": [],
        "olympic_vmo_imo": [],
        "us_k12": [],
        "vn_gdpt2018": []
    }

    for p in problems:
        p_id = p.get("problem_id", "").upper()
        if "GAOKAO" in p_id:
            grouped["cn_gaokao"].append(p)
        elif "IMO" in p_id or "VMO" in p_id:
            grouped["olympic_vmo_imo"].append(p)
        elif "AIME" in p_id or "AMC" in p_id or "US" in p_id:
            grouped["us_k12"].append(p)
        else:
            grouped["vn_gdpt2018"].append(p)

    for cat, prob_list in grouped.items():
        if not prob_list:
            continue
        target_dir = BASE_DIR / "stem_shared_core" / "curricula" / cat
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"benchmark_{cat}_curated.json"
        
        # Đọc dữ liệu cũ nếu có để gộp
        existing_problems = []
        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    existing_problems = old_data.get("problems", [])
            except Exception:
                existing_problems = []

        # Hợp nhất theo problem_id
        existing_ids = {p["problem_id"] for p in existing_problems}
        for p in prob_list:
            if p["problem_id"] not in existing_ids:
                existing_problems.append(p)
                existing_ids.add(p["problem_id"])

        payload = {
            "dataset_metadata": {
                "source": cat,
                "total_problems": len(existing_problems),
                "curriculum_category": cat
            },
            "problems": existing_problems
        }
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"✅ Đã lưu {len(prob_list)} bài vào {target_file}")

if __name__ == "__main__":
    distribute()
