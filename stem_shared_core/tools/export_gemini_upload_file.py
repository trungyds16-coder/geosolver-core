# -*- coding: utf-8 -*-
"""
export_gemini_upload_file.py
Tạo 1 file duy nhất (Markdown hoặc Text) chứa toàn bộ đề bài + lời giải + rubric
để bạn chỉ cần kéo-thả (Upload) trực tiếp lên Google AI Studio / Gemini Web hoàn toàn miễn phí.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

geo_file = BASE_DIR / "stem_shared_core" / "curricula" / "vn_gdpt2018" / "grade_10_geometry" / "sample_geo2d_bench.json"
alg_file = BASE_DIR / "stem_shared_core" / "curricula" / "vn_gdpt2018" / "grade_10" / "sample_radical_equation.json"

with open(geo_file, "r", encoding="utf-8") as f:
    geo_data = json.load(f)

with open(alg_file, "r", encoding="utf-8") as f:
    alg_data = json.load(f)

lines = []
lines.append("# BỘ ĐỀ THI & LỜI GIẢI CẦN THẨM ĐỊNH SƯ PHẠM (TOÁN 10 - GDPT 2018)")
lines.append("Bạn là chuyên gia thẩm định sư phạm môn Toán THPT của Bộ GD&ĐT Việt Nam.")
lines.append("Hãy xem xét kỹ từng bài toán dưới đây theo các tiêu chí sư phạm:")
lines.append("1. Lời giải có bị nhảy cóc (thiếu căn cứ định lý) không?")
lines.append("2. Văn phong có mạch lạc, chuẩn mực sư phạm SGK Việt Nam không?")
lines.append("3. Viết lại lời giải mẫu mực (từng bước rõ ràng, dễ hiểu nhất cho học sinh).\n")
lines.append("=" * 60 + "\n")

lines.append("## PHẦN 1: HÌNH HỌC PHẲNG OXY (2D GEOMETRY)\n")
for p in geo_data.get("problems", []):
    if "INVALID" in p.get("problem_id", ""):
        continue
    p_id = p.get("problem_id")
    title = p.get("title", "")
    prompt = p.get("prompt", {}).get("vi", "")
    gt = json.dumps(p.get("ground_truth", {}), ensure_ascii=False)
    
    lines.append(f"### [BÀI TOÁN {p_id}]: {title}")
    lines.append(f"- **Đề bài**: {prompt}")
    lines.append(f"- **Đáp số chuẩn**: {gt}")
    lines.append("- **Lời giải hệ thống hiện tại**: Giải bằng tọa độ Oxy, tính tích vô hướng hoặc lập hệ phương trình.")
    lines.append("\n" + "-" * 40 + "\n")

lines.append("## PHẦN 2: ĐẠI SỐ 10 (PHƯƠNG TRÌNH VÔ TỈ & NGHIỆM NGOẠI LAI)\n")
for p in alg_data.get("problems", []):
    p_id = p.get("problem_id")
    prompt = p.get("prompt", {}).get("vi", "")
    gt = json.dumps(p.get("ground_truth", {}), ensure_ascii=False)
    
    lines.append(f"### [BÀI TOÁN {p_id}]")
    lines.append(f"- **Đề bài**: {prompt}")
    lines.append(f"- **Đáp số chuẩn**: {gt}")
    lines.append("- **Lời giải hệ thống hiện tại**: Bình phương 2 vế giải phương trình bậc 2, sau đó kiểm tra điều kiện để loại nghiệm ngoại lai.")
    lines.append("\n" + "-" * 40 + "\n")

out_file = BASE_DIR / "stem_shared_core" / "evaluation" / "TAP_DE_THI_UPLOAD_GEMINI.md"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"File created successfully: {out_file}")
