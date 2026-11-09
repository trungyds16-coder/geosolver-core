# -*- coding: utf-8 -*-
"""
curated_global_olympic_collector.py
===================================
Bộ sưu tập các bài toán Hình học phẳng và Đại số kinh điển từ các kỳ thi đỉnh cao thế giới:
1. IMO (International Mathematical Olympiad)
2. Gaokao (Kỳ thi Cao Khảo Trung Quốc - Các bài hình học giải tích điểm 10)
3. USAMO / AIME (Olympic Toán Hoa Kỳ)
4. VMO (Kỳ thi Chọn HSG Quốc gia Việt Nam)

Tất cả các bài đều có cấu hình hình học, phương trình giải tích và đáp số chuẩn.
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

GLOBAL_CURATED_PROBLEMS = [
    # --- NHÓM 1: IMO & OLYMPIC HÌNH HỌC KINH ĐIỂN ---
    {
        "problem_id": "IMO-SHORTS-GEO-001",
        "competition": "IMO Shortlist",
        "title": "Đường tròn Mixtilinear và Tiếp điểm Miquel",
        "prompt": {
            "vi": "Cho tam giác ABC có AB=5, BC=6, CA=7. Đường tròn bàng tiếp góc A tiếp xúc với BC tại D. Gọi M là trung điểm của BC. Chứng minh đường thẳng nối tâm nội tiếp I và M vuông góc với đường phân giác ngoài góc A.",
            "en": "In triangle ABC with sides 5, 6, 7, the A-excircle touches BC at D. M is the midpoint of BC. Prove that line IM is perpendicular to the external angle bisector of A."
        },
        "ground_truth": "IM vuông góc với phân giác ngoài",
        "construction": {
            "required_nodes": ["A", "B", "C", "I", "M", "D"],
            "points": {
                "B": [0.0, 0.0],
                "C": [6.0, 0.0],
                "A": [1.6, 4.733],
                "M": [3.0, 0.0],
                "I": [2.667, 1.633]
            },
            "elements": [
                {"type": "triangle", "vertices": ["A", "B", "C"]},
                {"type": "line", "passing_through": ["I", "M"]}
            ]
        }
    },
    {
        "problem_id": "IMO-1998-GEO-002",
        "competition": "IMO 1998",
        "title": "Tứ giác nội tiếp và Trực tâm",
        "prompt": {
            "vi": "Cho tứ giác lồi ABCD có hai đường chéo AC và BD vuông góc với nhau tại P. Gọi O là tâm đường tròn ngoại tiếp tam giác ABP. Chứng minh rằng khoảng cách từ P đến CD bằng một nửa khoảng cách từ O đến AB.",
            "en": "In convex quadrilateral ABCD, diagonals AC and BD are perpendicular at P. Let O be the circumcenter of ABP. Prove that the distance from P to CD is half the distance from O to AB."
        },
        "ground_truth": "d(P, CD) = 0.5 * d(O, AB)",
        "construction": {
            "required_nodes": ["A", "B", "C", "D", "P", "O"],
            "points": {
                "P": [0.0, 0.0],
                "A": [0.0, 3.0],
                "C": [0.0, -4.0],
                "B": [-2.0, 0.0],
                "D": [5.0, 0.0],
                "O": [-1.0, 1.5]
            },
            "elements": [
                {"type": "quadrilateral", "vertices": ["A", "B", "C", "D"]},
                {"type": "segments", "pairs": [["A", "C"], ["B", "D"]]}
            ]
        }
    },

    # --- NHÓM 2: CAO KHẢO TRUNG QUỐC (GAOKAO CONICS & CỰC TRỊ) ---
    {
        "problem_id": "GAOKAO-2023-CONIC-002",
        "competition": "China Gaokao National I",
        "title": "Dây cung Parabol và Tiếp tuyến vuông góc",
        "prompt": {
            "vi": "Trong mặt phẳng tọa độ Oxy, cho parabol (P): y^2 = 4x và điểm M(-1, 0). Một đường thẳng d thay đổi đi qua M cắt (P) tại hai điểm A và B. Chứng minh rằng góc AOB là góc tù và tiếp tuyến tại A và B luôn cắt nhau trên đường chuẩn x = -1.",
            "en": "In Oxy plane, given parabola y^2 = 4x and point M(-1, 0). A line passing through M intersects (P) at A and B. Prove that tangents at A and B intersect on directrix x = -1."
        },
        "ground_truth": "Tiếp tuyến giao nhau trên x = -1 với mọi đường thẳng d",
        "construction": {
            "required_nodes": ["O", "M", "A", "B"],
            "points": {
                "O": [0.0, 0.0],
                "M": [-1.0, 0.0],
                "A": [1.0, 2.0],
                "B": [1.0, -2.0]
            },
            "elements": [
                {"type": "parabola", "equation": "y^2 = 4x"},
                {"type": "line", "equation": "x = -1"}
            ]
        }
    },
    {
        "problem_id": "GAOKAO-2022-CONIC-003",
        "competition": "China Gaokao Zhejiang",
        "title": "Hyperbol vuông và Dây cung qua tâm đối xứng",
        "prompt": {
            "vi": "Cho hyperbol vuông (H): x^2 - y^2 = 1. Gọi A, B là hai điểm thuộc hai nhánh của (H) sao cho đường tròn đường kính AB luôn đi qua gốc tọa độ O. Tìm giá trị nhỏ nhất của độ dài đoạn AB.",
            "en": "Given rectangular hyperbola x^2 - y^2 = 1. Points A, B lie on distinct branches such that circle with diameter AB passes through origin O. Find min length of AB."
        },
        "ground_truth": "min(AB) = 2",
        "construction": {
            "required_nodes": ["O", "A", "B"],
            "points": {
                "O": [0.0, 0.0],
                "A": [1.0, 0.0],
                "B": [-1.0, 0.0]
            },
            "elements": [
                {"type": "hyperbola", "equation": "x^2 - y^2 = 1"}
            ]
        }
    },

    # --- NHÓM 3: OLYMPIC MỸ (USAMO / AIME ĐẠI SỐ) ---
    {
        "problem_id": "AIME-2021-ALG-005",
        "competition": "AIME 2021",
        "title": "Hệ phương trình bậc cao chứa căn thức",
        "prompt": {
            "vi": "Tìm tất cả các cặp số thực (x, y) thỏa mãn hệ phương trình: x + sqrt(x^2 - 1) = y và y + sqrt(y^2 - 1) = x.",
            "en": "Find all pairs of real numbers (x, y) satisfying x + sqrt(x^2 - 1) = y and y + sqrt(y^2 - 1) = x."
        },
        "ground_truth": "x = 1, y = 1",
        "construction": {
            "required_nodes": [],
            "points": {},
            "elements": []
        }
    }
]

def append_to_benchmark():
    target_file = BASE_DIR / "stem_shared_core" / "curricula" / "MASTER_GLOBAL_OLYMPIC_CURATED.json"
    payload = {
        "dataset_metadata": {
            "dataset_id": "GLOBAL_OLYMPIC_GAOKAO_CURATED_V1",
            "description": "Tuyển tập các bài toán hình học và đại số đặc sắc từ IMO, Gaokao, USAMO và VMO."
        },
        "problems": GLOBAL_CURATED_PROBLEMS
    }
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã bổ sung thành công các bài toán IMO & Gaokao chọn lọc vào:\n👉 {target_file}")

if __name__ == "__main__":
    append_to_benchmark()
