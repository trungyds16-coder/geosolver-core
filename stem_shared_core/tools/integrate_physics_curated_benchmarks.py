# -*- coding: utf-8 -*-
"""
integrate_physics_curated_benchmarks.py
=======================================
Tự động nạp, sửa lỗi escape LaTeX trong JSON, gộp 2 file:
- gemini-code-1793971367663.json
- gemini-code-1793971420972.json

Thành 1 kho chuẩn duy nhất:
-> stem_shared_core/curricula/olympic_vmo_imo/BENCHMARK_PHYSICS_IPHO_ELITE.json
Sau đó tự động xóa các file tạm gemini-code-*.json để đảm bảo tính chuyên nghiệp.
"""

from __future__ import annotations
import sys
import re
import json
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVAL_DIR = BASE_DIR / "stem_shared_core" / "evaluation"
TARGET_DIR = BASE_DIR / "stem_shared_core" / "curricula" / "olympic_vmo_imo"
TARGET_FILE = TARGET_DIR / "BENCHMARK_PHYSICS_IPHO_ELITE.json"

FILE_1 = EVAL_DIR / "gemini-code-1793971367663.json"
FILE_2 = EVAL_DIR / "gemini-code-1793971420972.json"

def load_and_fix_json(path: Path) -> list:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Dùng strict=False trong json.loads để cho phép các ký tự điều khiển
    # Sửa triệt để các chuỗi escape bằng cách duyệt từng ký tự:
    result = []
    i = 0
    in_str = False
    escaped = False
    valid_escapes = {'"', '\\', '/', 'b', 'f', 'n', 'r', 't'}

    while i < len(text):
        c = text[i]
        if not in_str:
            if c == '"':
                in_str = True
            result.append(c)
            i += 1
        else:
            if escaped:
                result.append(c)
                escaped = False
                i += 1
            else:
                if c == '\\':
                    # Kiểm tra ký tự tiếp theo
                    if i + 1 < len(text):
                        nxt = text[i + 1]
                        if nxt in valid_escapes:
                            result.append(c)
                            escaped = True
                            i += 1
                        elif nxt == 'u' and i + 5 < len(text) and all(ch in '0123456789abcdefABCDEF' for ch in text[i+2:i+6]):
                            result.append(c)
                            escaped = True
                            i += 1
                        else:
                            # Ký tự escape không hợp lệ (ví dụ \frac, \_ ...) -> biến thành \\
                            result.append('\\\\')
                            i += 1
                    else:
                        result.append('\\\\')
                        i += 1
                elif c == '"':
                    in_str = False
                    result.append(c)
                    i += 1
                else:
                    result.append(c)
                    i += 1

    sanitized = "".join(result)
    return json.loads(sanitized, strict=False)

def run_integration():
    all_problems = []
    seen_ids = set()

    for fpath in [FILE_1, FILE_2]:
        if not fpath.exists():
            continue
        print(f"📥 Đang nạp và chuẩn hóa dữ liệu từ: {fpath.name}...")
        probs = load_and_fix_json(fpath)
        for p in probs:
            pid = p.get("problem_id")
            if pid not in seen_ids:
                # Chuẩn hóa prompt nếu là string
                if isinstance(p.get("prompt"), str):
                    p["prompt"] = {"vi": p["prompt"]}
                all_problems.append(p)
                seen_ids.add(pid)
        print(f"   -> Đã trích xuất {len(probs)} bài toán Vật lí xuất sắc.")

    print(f"\n📊 Tổng số bài toán Vật lí độc bản thu được: {len(all_problems)} bài.")

    # Lưu vào thư mục chuẩn học thuật
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_metadata": {
            "dataset_id": "GLOBAL_PHYSICS_IPHO_VPHO_ELITE_2026_V1",
            "curriculum": "Olympic Vật lý Quốc tế (IPhO) & Vật lý Đại cương Đại học (Bách Khoa PH1110/PH1111)",
            "total_problems": len(all_problems),
            "description": "Kho bài toán Vật lí tinh hoa tuyển chọn: Quang hình học quả cầu thủy tinh, Mạng điện trở khối lập phương đối xứng, Mạng lưới phẳng vô hạn, Con lắc điện trường vi tích phân, và Khí thực Van der Waals."
        },
        "problems": all_problems
    }

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✅ ĐÃ LƯU BỘ DỮ LIỆU VẬT LÍ CHUYÊN NGHIỆP TẠI:\n   👉 {TARGET_FILE}")

    # Xóa 2 file tạm
    for fpath in [FILE_1, FILE_2]:
        if fpath.exists():
            fpath.unlink()
            print(f"🗑️ Đã dọn dẹp file tạm: {fpath.name}")

    print("🎉 QUY TRÌNH TÍCH HỢP VẬT LÍ HOÀN TẤT 100%!")

if __name__ == "__main__":
    run_integration()
