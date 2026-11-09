# -*- coding: utf-8 -*-
"""
pedagogical_judge.py
====================
Bộ thẩm định chất lượng sư phạm của lời giải toán học (Pedagogical Solution Evaluator).
Sử dụng LLM (Gemini API hoặc Local fallback) theo bộ tiêu chuẩn (Rubric) sư phạm THPT.

TIÊU CHÍ CHẤM ĐIỂM (Thang 10):
1. Tính chính xác toán học (Mathematical Accuracy - 3đ): Không sai số học, áp dụng đúng định lý.
2. Tính liên tục & Không nhảy cóc (Logical Continuity - 3đ): Có luận cứ rõ ràng cho từng bước suy ra.
3. Văn phong sư phạm chuẩn SGK (Pedagogical Tone - 2đ): Dẫn dắt tự nhiên, không cộc lốc, dễ hiểu cho học sinh.
4. Xử lý điều kiện & Nghiệm ngoại lai (Constraint & Domain Handling - 2đ): Đặt điều kiện xác định đầy đủ, thử lại nghiêm túc.
"""

from __future__ import annotations
import json
from typing import Dict, Any, Optional

RUBRIC_PROMPT_TEMPLATE = """Bạn là một chuyên gia khảo thí và biên soạn sách giáo khoa Toán THPT của Bộ Giáo dục & Đào tạo Việt Nam.
Hãy đóng vai một Giáo viên chấm thi khắt khe để thẩm định lời giải của một phần mềm giải toán tự động dưới đây.

ĐỀ BÀI:
{problem_prompt}

LỜI GIẢI CỦA HỆ THỐNG:
{solution_text}

ĐÁP SỐ CHUẨN (GROUND TRUTH):
{ground_truth}

---
YÊU CẦU ĐÁNH GIÁ (Thang điểm 10):
1. Tính chính xác toán học (0 - 3 điểm): Kết quả đúng hay sai? Có nhầm lẫn định lý không?
2. Tính liên tục & Không nhảy bước (0 - 3 điểm): Các bước suy luận có đủ căn cứ không? Có bước nào biến đổi tắt làm học sinh không hiểu không?
3. Văn phong sư phạm (0 - 2 điểm): Lời giải có câu chữ dẫn dắt tự nhiên như giáo viên giảng bài không? Hay chỉ là những dòng công thức khô khan?
4. Đầy đủ điều kiện / nghiệm ngoại lai (0 - 2 điểm): Có xét điều kiện xác định, kiểm tra tính suy biến/nghiệm ngoại lai không?

HÃY TRẢ VỀ KẾT QUẢ DUY NHẤT Ở ĐỊNH DẠNG JSON NHƯ SAU (không bọc trong markdown codeblock nếu có thể, hoặc dùng block json):
{{
  "math_score": 3.0,
  "logic_continuity_score": 2.5,
  "pedagogical_tone_score": 1.5,
  "constraint_score": 2.0,
  "total_score": 9.0,
  "passed_pedagogical_standard": true,
  "detected_flaws": [
    "Mô tả cụ thể bước giải bị nhảy cóc hoặc văn phong chưa đạt (nếu có)"
  ],
  "improved_suggestion": "Đoạn văn phong sư phạm viết lại mẫu để hệ thống học tập"
}}
"""

def generate_evaluation_payload(problem: Dict[str, Any], solution_text: str) -> str:
    """Tạo nội dung prompt gửi tới Gemini API để thẩm định một bài toán."""
    prompt_str = problem.get("prompt", {}).get("vi", str(problem.get("prompt")))
    gt_str = json.dumps(problem.get("ground_truth", {}), ensure_ascii=False, indent=2)
    return RUBRIC_PROMPT_TEMPLATE.format(
        problem_prompt=prompt_str,
        solution_text=solution_text,
        ground_truth=gt_str
    )

def create_batch_evaluation_suite(problem_list: list, solutions_dict: dict) -> list:
    """
    Chuẩn bị dữ liệu để nạp đồng loạt (batch) vào Gemini API một lần duy nhất,
    tận dụng triệt để cửa sổ context lớn của Gemini mà không phải gửi lẻ tẻ.
    """
    suite = []
    for prob in problem_list:
        p_id = prob["problem_id"]
        sol = solutions_dict.get(p_id, "Chưa có lời giải.")
        suite.append({
            "problem_id": p_id,
            "evaluation_prompt": generate_evaluation_payload(prob, sol)
        })
    return suite
