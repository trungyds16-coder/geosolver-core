# -*- coding: utf-8 -*-
"""
evaluate_solutions_with_gemini.py
=================================
Script tự động đóng gói hàng loạt bài toán và gửi tới Gemini API để chấm điểm
chất lượng sư phạm và phát hiện lỗi logic/nhảy cóc (Pedagogical Evaluation).
Không cần copy-paste thủ công bất kỳ bài nào!
"""

import os
import sys
import json
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from stem_shared_core.ai_model_hub import AIModelHub, ChunkKind
from stem_shared_core.evaluation.pedagogical_judge import generate_evaluation_payload

def evaluate_benchmarks_batch(dataset_rel_path: str, solutions_dict: dict, output_report_path: str):
    dataset_path = BASE_DIR / dataset_rel_path
    if not dataset_path.exists():
        print(f"❌ Không tìm thấy dataset tại {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    problems = data.get("problems", [])
    print(f"🚀 BẮT ĐẦU CHẤM ĐIỂM SƯ PHẠM QUA GEMINI BATCH CHO {len(problems)} BÀI TOÁN...")

    hub = AIModelHub()
    results = []

    for idx, prob in enumerate(problems, 1):
        p_id = prob.get("problem_id")
        sol_text = solutions_dict.get(p_id, "Hệ thống giải theo tọa độ Oxy nhưng thiếu câu dẫn dắt sư phạm.")
        
        # Bỏ qua bài invalid test
        if "INVALID" in p_id:
            continue

        print(f"\n[{idx}] Đang gửi bài '{p_id}' lên Gemini để thẩm định...")
        eval_prompt = generate_evaluation_payload(prob, sol_text)

        # Gọi Gemini stream hoặc direct
        full_response = ""
        try:
            for chunk in hub.stream(eval_prompt):
                if chunk.kind is ChunkKind.ANSWER:
                    full_response += chunk.text
            
            print(f"    ✅ Nhận kết quả thẩm định cho bài {p_id}.")
            results.append({
                "problem_id": p_id,
                "review": full_response
            })
        except Exception as e:
            print(f"    ⚠️ Lỗi khi gọi AI: {e}")
            results.append({
                "problem_id": p_id,
                "error": str(e)
            })

    # Lưu báo cáo thẩm định
    out_file = BASE_DIR / output_report_path
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 HOÀN TẤT! Toàn bộ đánh giá sư phạm đã được lưu tại: {out_file}")

if __name__ == "__main__":
    # Test mẫu với dataset hình học vừa tạo
    sample_solutions = {
        "GEO2D-G10-001": "Ta có vt(AB) = (-3; 4), vt(AC) = (8; 6). Tích vô hướng AB.AC = -3*8 + 4*6 = 0 => AB vuông góc AC. Diện tích S = 1/2 * AB * AC = 1/2 * 5 * 10 = 25.",
        "GEO2D-G10-002": "Tọa độ tâm O là nghiệm hệ trung trực. Giải ra O(2; 3), R = sqrt(13)."
    }
    evaluate_benchmarks_batch(
        dataset_rel_path="stem_shared_core/curricula/vn_gdpt2018/grade_10_geometry/sample_geo2d_bench.json",
        solutions_dict=sample_solutions,
        output_report_path="stem_shared_core/evaluation/SAMPLE_PEDAGOGICAL_REPORT.json"
    )
