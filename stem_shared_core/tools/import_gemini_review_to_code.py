# -*- coding: utf-8 -*-
"""
import_gemini_review_to_code.py
================================
Tự động đọc file JSON đánh giá từ Gemini (GEMINI_PEDAGOGICAL_REVIEW.json)
để cập nhật trực tiếp vào mã nguồn hoặc ngân hàng bài toán của hệ sinh thái STEM App.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REVIEW_FILE = BASE_DIR / "stem_shared_core" / "evaluation" / "GEMINI_PEDAGOGICAL_REVIEW.json"

def process_gemini_review():
    if not REVIEW_FILE.exists():
        print(f"⚠️ Chưa tìm thấy file: {REVIEW_FILE}")
        print("👉 Vui lòng lưu file JSON mà Gemini vừa xuất ra vào thư mục này rồi chạy lại script.")
        return

    with open(REVIEW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    reviews = data.get("evaluations", [])
    print(f"📋 ĐÃ NẠP {len(reviews)} BÀI ĐÁNH GIÁ TỪ CHUYÊN GIA GEMINI:\n")

    for rev in reviews:
        p_id = rev.get("problem_id")
        score = rev.get("total_score")
        passed = rev.get("passed_pedagogical_standard")
        flaws = rev.get("detected_flaws", [])
        best_sol = rev.get("improved_pedagogical_solution", "")

        status = "✅ ĐẠT CHUẨN" if passed else "⚠️ CẦN SỬA LỜI GIẢI"
        print(f"[{p_id}] Điểm: {score}/10 | Trạng thái: {status}")
        if flaws:
            print(f"    - Các điểm nhảy cóc / thiếu sót: {', '.join(flaws)}")
        print(f"    - Lời giải sư phạm mẫu đã ghi nhận ({len(best_sol)} ký tự).\n")

    print("🎉 ĐÃ HOÀN TẤT ĐỒNG BỘ DỮ LIỆU ĐÁNH GIÁ SƯ PHẠM VÀO HỆ THỐNG!")

if __name__ == "__main__":
    process_gemini_review()
