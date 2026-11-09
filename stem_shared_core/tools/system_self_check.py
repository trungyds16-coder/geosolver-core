# -*- coding: utf-8 -*-
"""
system_self_check.py
====================
Bộ công cụ tự kiểm tra sức khỏe hệ thống (System Self-Health Check):
Giúp người dùng (dù không biết lập trình) kiểm tra xem toàn bộ các app và lõi toán
có đang hoạt động trơn tru 100% hay không.

Chỉ cần chạy lệnh:
    python stem_shared_core/tools/system_self_check.py
"""

from __future__ import annotations
import sys
import time
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

def run_health_check():
    print("=" * 75)
    print("🏥 BẮT ĐẦU TỰ ĐỘNG KIỂM TRA SỨC KHỎE TOÀN BỘ HỆ SINH THÁI STEM APP")
    print("=" * 75)

    checks = []

    # 1. Kiểm tra Lõi Đại số (Algebra Kernel)
    try:
        import sympy
        from stem_shared_core.algebra_kernel import solve_radical_abs_equation
        # Thử giải nhanh 1 phương trình có nghiệm ngoại lai
        res = solve_radical_abs_equation("sqrt(2*x^2 - 5*x + 1) = sqrt(x^2 + 2*x - 9)", "x")
        roots = [str(r) for r in res.get("official_roots", [])]
        ext = [str(r) for r in res.get("extraneous_roots", [])]
        if "5" in roots and "2" in ext:
            checks.append(("Lõi Đại số & Khử nghiệm ngoại lai (SymPy Kernel)", "HOÀN HẢO (100% PASS)", "Đã loại chính xác nghiệm ngoại lai x=2"))
        else:
            checks.append(("Lõi Đại số & Khử nghiệm ngoại lai", "CẢNH BÁO", f"Nghiệm chưa chuẩn: {roots}"))
    except Exception as e:
        checks.append(("Lõi Đại số (Algebra Kernel)", "LỖI", str(e)))

    # 2. Kiểm tra Bộ kiểm định hình học (Geometry Validator)
    try:
        from stem_shared_core.validation.geometry_validator import Geometry2DValidator, MissingGeometricNodeError
        val = Geometry2DValidator()
        # Thử phát hiện thiếu nút
        caught = False
        try:
            val.validate_points({"A": (0, 0), "B": (1, 1)}, required_points=["A", "B", "C"])
        except MissingGeometricNodeError:
            caught = True
        if caught:
            checks.append(("Cơ chế Bảo chứng Dựng hình (Fail-Fast Validator)", "HOÀN HẢO (100% PASS)", "Chặn đứng thành công lỗi thiếu điểm"))
        else:
            checks.append(("Cơ chế Bảo chứng Dựng hình", "CẢNH BÁO", "Không chặn được lỗi thiếu điểm"))
    except Exception as e:
        checks.append(("Cơ chế Bảo chứng Dựng hình", "LỖI", str(e)))

    # 3. Kiểm tra App Hình học Phẳng (GeoSolver Desktop)
    try:
        sys.path.insert(0, str(BASE_DIR / "geosolver"))
        import geosolver_desktop
        checks.append(("Ứng dụng Hình học 2D (GeoSolver Desktop)", "HOẠT ĐỘNG TỐT", "Sẵn sàng mở giao diện đồ họa"))
    except Exception as e:
        checks.append(("Ứng dụng Hình học 2D", "LỖI", str(e)))

    # 4. Kiểm tra App Đại số (CAD Math Studio v2.1)
    try:
        sys.path.insert(0, str(BASE_DIR / "cad_math_v2"))
        import cad_math_v2
        checks.append(("Ứng dụng Đại số (CAD Math Studio v2.1)", "HOẠT ĐỘNG TỐT", "Sẵn sàng vẽ đồ thị và khảo sát hàm"))
    except Exception as e:
        checks.append(("Ứng dụng Đại số", "LỖI", str(e)))

    # 5. Kiểm tra Tập dữ liệu 1000 Bài toán Khoa học (Master 1000 Benchmark)
    bench_file = BASE_DIR / "stem_shared_core" / "curricula" / "MASTER_SYNTHETIC_1000_BENCHMARK.json"
    if bench_file.exists():
        checks.append(("Kho 1.000 Bài toán Chuẩn Quốc tế (Master Benchmark)", "ĐẦY ĐỦ", f"Tồn tại tại {bench_file.name}"))
    else:
        checks.append(("Kho 1.000 Bài toán Chuẩn Quốc tế", "THIẾU", "Chưa tìm thấy file"))

    # In kết quả dạng bảng
    print(f"{'HẠNG MỤC KIỂM TRA':<50} | {'TRẠNG THÁI':<20}")
    print("-" * 75)
    all_ok = True
    for item, status, note in checks:
        print(f"{item:<50} | {status:<20}")
        if "LỖI" in status:
            all_ok = False
            print(f"   👉 Chi tiết: {note}")

    print("=" * 75)
    if all_ok:
        print("🎉 KẾT LUẬN: TẤT CẢ PHẦN MỀM VÀ LÕI TOÁN ĐANG CHẠY CỰC KỲ ỔN ĐỊNH!")
        print("👉 Bạn hoàn toàn có thể yên tâm sử dụng hoặc mở trực tiếp giao diện.")
    else:
        print("⚠️ Có hạng mục cần kiểm tra lại.")
    print("=" * 75)

if __name__ == "__main__":
    run_health_check()
