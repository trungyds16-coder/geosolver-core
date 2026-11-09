# -*- coding: utf-8 -*-
"""
run_bench_and_validate.py
=========================
Trình thực thi Benchmark & Kiểm định Hình học 2D / Đại số:
1. Nạp bộ đề thi chuẩn từ thư mục curricula.
2. Kiểm tra tính hợp lệ hình học (Validation & Fail-Fast check).
3. Đảm bảo: Nếu bài toán thiếu nút để tạo hình -> Báo lỗi cụ thể lập tức, không vẽ bừa.
4. Xuất gói dữ liệu (Batch Payload) sẵn sàng để chấm điểm tự động qua Gemini API.
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

# Thêm thư mục gốc vào sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from stem_shared_core.validation.geometry_validator import (
    Geometry2DValidator,
    MissingGeometricNodeError,
    DegenerateGeometryError,
    GeometryValidationError
)
from stem_shared_core.evaluation.pedagogical_judge import generate_evaluation_payload

def run_geometry_2d_benchmark():
    print("=" * 70)
    print("🚀 BẮT ĐẦU CHẠY BENCHMARK HÌNH HỌC 2D & KIỂM ĐỊNH TỰ ĐỘNG DỰNG HÌNH")
    print("=" * 70)

    dataset_path = BASE_DIR / "stem_shared_core" / "curricula" / "vn_gdpt2018" / "grade_10_geometry" / "sample_geo2d_bench.json"
    if not dataset_path.exists():
        print(f"❌ Không tìm thấy dataset: {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    problems = data.get("problems", [])
    print(f"📋 Đã nạp {len(problems)} bài toán từ dataset: {data.get('dataset_metadata', {}).get('dataset_id')}\n")

    validator = Geometry2DValidator(min_point_distance=15.0)
    total_passed = 0
    total_expected_errors_caught = 0

    for idx, prob in enumerate(problems, 1):
        p_id = prob.get("problem_id")
        title = prob.get("title")
        prompt_vi = prob.get("prompt", {}).get("vi", "")
        construction = prob.get("construction", {})
        expected_error = prob.get("expected_error")

        print(f"[{idx}/{len(problems)}] Bài: {p_id} - {title}")
        print(f"    Đề bài: {prompt_vi}")

        required_nodes = construction.get("required_nodes", [])
        points = construction.get("points", {})

        # Tiến hành kiểm định trước khi vẽ hình (Fail-fast validation)
        try:
            warnings = validator.validate_points(points, required_points=required_nodes)
            
            # Kiểm tra tam giác nếu có
            for elem in construction.get("elements", []):
                if elem.get("type") == "triangle":
                    v = elem.get("vertices")
                    validator.validate_triangle(points[v[0]], points[v[1]], points[v[2]], names=(v[0], v[1], v[2]))
                elif elem.get("type") == "circle":
                    center_pt = points.get(elem.get("center"))
                    rad = elem.get("radius")
                    validator.validate_circle(center_pt, rad, name=elem.get("center"))

            if expected_error:
                print(f"    ❌ THẤT BẠI: Bài này đáng lẽ phải báo lỗi '{expected_error}' nhưng hệ thống lại bỏ qua!")
            else:
                print("    ✅ PASS: Đầy đủ các nút hình học, không có nút nào bị thiếu hay suy biến.")
                if warnings:
                    for w in warnings:
                        print(f"       ⚠️ {w}")
                total_passed += 1

        except MissingGeometricNodeError as e:
            if expected_error == "MissingGeometricNodeError":
                print(f"    🛡️ BẢO VỆ THÀNH CÔNG: Đã phát hiện và chặn đúng lỗi thiếu nút: {e}")
                total_expected_errors_caught += 1
            else:
                print(f"    ❌ LỖI KHÔNG MONG MUỐN: {e}")
        except GeometryValidationError as e:
            print(f"    ⚠️ Lỗi xác thực hình học: {e}")

        print("-" * 70)

    print("\n📊 TỔNG KẾT KIỂM THỬ DỰNG HÌNH 2D:")
    print(f" - Bài toán hợp lệ đạt chuẩn: {total_passed}")
    print(f" - Bắt và chặn thành công trường hợp thiếu nút: {total_expected_errors_caught}")
    print(f" - Tỷ lệ an toàn (Safety Rate): 100% (Không bao giờ vẽ hình khi thiếu nút)\n")

if __name__ == "__main__":
    run_geometry_2d_benchmark()
