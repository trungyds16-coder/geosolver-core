# -*- coding: utf-8 -*-
"""
Công cụ tính toán độ tin cậy liên thẩm định viên (Inter-Rater Reliability)
Hỗ trợ:
- Cohen's Kappa (áp dụng cho từng cặp thẩm định viên)
- Fleiss' Kappa (áp dụng cho hội đồng >= 3 thẩm định viên)
- Phân loại mức độ đồng thuận theo chuẩn Landis & Koch (1977)
"""

import sys

def compute_cohen_kappa(rater_a, rater_b, categories=None):
    """
    Tính hệ số Cohen's Kappa giữa 2 thẩm định viên trên N mẫu đánh giá.
    rater_a, rater_b: Danh sách điểm số/phân loại của từng mẫu.
    """
    if len(rater_a) != len(rater_b):
        raise ValueError("Hai danh sách đánh giá phải có cùng số lượng mẫu.")
    
    n = len(rater_a)
    if n == 0:
        return 1.0

    if categories is None:
        categories = sorted(list(set(rater_a).union(set(rater_b))))

    # Bảng phân phối chéo (contingency table)
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)
    table = [[0] * k for _ in range(k)]

    for a, b in zip(rater_a, rater_b):
        table[cat_to_idx[a]][cat_to_idx[b]] += 1

    # Tính xác suất quan sát đồng thuận (Po)
    po = sum(table[i][i] for i in range(k)) / n

    # Tính xác suất kỳ vọng ngẫu nhiên (Pe)
    pe = 0.0
    for i in range(k):
        p_row = sum(table[i][j] for j in range(k)) / n
        p_col = sum(table[j][i] for j in range(k)) / n
        pe += p_row * p_col

    if pe == 1.0:
        return 1.0

    kappa = (po - pe) / (1.0 - pe)
    return kappa

def compute_fleiss_kappa(ratings_matrix, categories=None):
    """
    Tính hệ số Fleiss' Kappa cho n đối tượng được đánh giá bởi m thẩm định viên.
    ratings_matrix: Ma trận n x m (mỗi hàng là 1 đối tượng, mỗi cột là điểm từ 1 thẩm định viên).
    """
    n_subjects = len(ratings_matrix)
    if n_subjects == 0:
        return 1.0
    n_raters = len(ratings_matrix[0])

    if categories is None:
        cats_set = set()
        for row in ratings_matrix:
            cats_set.update(row)
        categories = sorted(list(cats_set))

    cat_to_idx = {c: i for i, c in enumerate(categories)}
    k_cats = len(categories)

    # Ma trận n x k (số rater chọn từng category cho từng subject)
    n_matrix = [[0] * k_cats for _ in range(n_subjects)]
    for i, row in enumerate(ratings_matrix):
        for val in row:
            n_matrix[i][cat_to_idx[val]] += 1

    # 1. Tỷ lệ phân loại rơi vào category j trên toàn bộ dữ liệu (pj)
    total_ratings = n_subjects * n_raters
    pj = [sum(n_matrix[i][j] for i in range(n_subjects)) / total_ratings for j in range(k_cats)]

    # 2. Mức độ đồng thuận nội bộ cho từng subject i (Pi)
    pi_list = []
    for i in range(n_subjects):
        sum_sq = sum(n_matrix[i][j] * (n_matrix[i][j] - 1) for j in range(k_cats))
        pi = sum_sq / (n_raters * (n_raters - 1)) if n_raters > 1 else 1.0
        pi_list.append(pi)

    # 3. Trung bình quan sát P_bar
    p_bar = sum(pi_list) / n_subjects

    # 4. Trung bình kỳ vọng ngẫu nhiên Pe_bar
    pe_bar = sum(p**2 for p in pj)

    if pe_bar == 1.0:
        return 1.0

    kappa = (p_bar - pe_bar) / (1.0 - pe_bar)
    return kappa

def interpret_kappa(kappa):
    """Phân loại mức độ đồng thuận theo Landis & Koch (1977)."""
    if kappa < 0.0:
        return "Kém (Poor / Disagreement)"
    elif kappa <= 0.20:
        return "Rất thấp (Slight agreement)"
    elif kappa <= 0.40:
        return "Trung bình thấp (Fair agreement)"
    elif kappa <= 0.60:
        return "Vừa phải (Moderate agreement)"
    elif kappa <= 0.80:
        return "Đáng kể (Substantial agreement - MỤC TIÊU ĐẠT)"
    else:
        return "Gần như tuyệt đối (Almost perfect agreement)"

def demo():
    print("=" * 80)
    print("CHƯƠNG TRÌNH KIỂM CHỨNG CÔNG CỤ TÍNH ĐỘ TIN CẬY LIÊN THẨM ĐỊNH VIÊN (INTER-RATER)")
    print("=" * 80)

    # Dữ liệu thử nghiệm: 5 bài x 5 tiêu chí = 25 mục đánh giá bởi 3 giáo viên
    # Thang điểm: 4 hoặc 5 (rất cao)
    gv1 = [5, 4, 5, 5, 5,  4, 4, 4, 4, 5,  5, 5, 5, 4, 5,  5, 5, 4, 5, 5,  4, 5, 5, 5, 5]
    gv2 = [5, 4, 4, 5, 5,  4, 4, 4, 4, 4,  5, 5, 5, 4, 5,  5, 4, 4, 5, 5,  4, 4, 5, 5, 5]
    gv3 = [4, 4, 5, 5, 5,  4, 4, 4, 4, 5,  5, 5, 4, 4, 5,  5, 5, 4, 4, 5,  4, 5, 5, 5, 5]

    # Ma trận đối tượng x rater (25 x 3)
    matrix = [[gv1[i], gv2[i], gv3[i]] for i in range(len(gv1))]

    print(f"Tổng số mục đánh giá: {len(gv1)} mục (5 bài toán x 5 tiêu chí sư phạm)")
    print(f"Số lượng giáo viên tham gia: 3 giáo viên độc lập\n")

    # Tính Cohen's Kappa từng cặp
    k_12 = compute_cohen_kappa(gv1, gv2)
    k_23 = compute_cohen_kappa(gv2, gv3)
    k_13 = compute_cohen_kappa(gv1, gv3)

    print(f"• Cohen's Kappa (GV 1 - GV 2): {k_12:.4f} -> {interpret_kappa(k_12)}")
    print(f"• Cohen's Kappa (GV 2 - GV 3): {k_23:.4f} -> {interpret_kappa(k_23)}")
    print(f"• Cohen's Kappa (GV 1 - GV 3): {k_13:.4f} -> {interpret_kappa(k_13)}")

    # Tính Fleiss' Kappa toàn hội đồng
    f_kappa = compute_fleiss_kappa(matrix)
    print(f"\n==> Fleiss' Kappa toàn hội đồng (3 GV): {f_kappa:.4f}")
    print(f"    Đánh giá mức độ đồng thuận: {interpret_kappa(f_kappa)}")
    print("=" * 80)

if __name__ == '__main__':
    demo()
