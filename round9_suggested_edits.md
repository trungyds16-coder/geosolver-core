# Gợi ý sửa Round 9 cho `classify_triangle` (chưa chạy trên repo thật)

Các đoạn dưới đây viết dựa trên bản `classify_triangle` trong báo cáo Round 8.
Hãy sửa trên một nhánh git riêng, rồi chạy `tests/test_round9_taint_validation.py`.

---

## Sửa 1. Thêm helper ở đầu file (ngoài hàm), thay cho logic cờ nằm trong `get_xy_name_exact`

```python
_FREE_SOURCES = ("free", "mouse", "dragged")
_EXACT_SOURCES = ("typed", "grid_snap", "snapped", "exact")
_DERIVED_SOURCES = ("midpoint", "intersection", "formula")


def _finite(v, label, p):
    """Ép về float, từ chối None / chuỗi rác / NaN / inf."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"Tọa độ '{label}' không hợp lệ: {p!r}")
    if not math.isfinite(f):
        raise ValueError(f"Tọa độ '{label}' phải hữu hạn (không NaN/inf): {p!r}")
    return f


def _point_flag(p, _depth=0):
    """True = chính xác, False = vẽ tay (taint), None = không rõ nguồn.

    Điểm dựng hình (midpoint/intersection/formula) kế thừa cờ từ điểm cha
    qua khóa "parents". Không có "parents" thì coi là không rõ (None),
    trừ khi có exact=True tường minh.
    """
    if not isinstance(p, dict):
        return None
    if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
        return False
    if p.get("source") in _DERIVED_SOURCES and p.get("parents") and _depth < 8:
        flags = [_point_flag(q, _depth + 1) for q in p["parents"]]
        if any(f is False for f in flags):
            return False
        if all(f is True for f in flags):
            return True
        return None
    if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
        return True
    return None
```

## Sửa 2. Trong `classify_triangle`, thay toàn bộ `get_xy_name_exact`

```python
    def get_xy_name_exact(p, default_name):
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Điểm thiếu thuộc tính tọa độ 'x' hoặc 'y': {p}")
            return (_finite(p["x"], "x", p), _finite(p["y"], "y", p),
                    str(p.get("name") or default_name), _point_flag(p))
        if len(p) < 2:
            raise ValueError(f"Tọa độ điểm phải có ít nhất 2 phần tử (x, y): {p}")
        return _finite(p[0], "x", p), _finite(p[1], "y", p), default_name, None
```

## Sửa 3. Ép điểm vẽ tay đi qua nhánh dung sai

Tìm dòng:

```python
    is_discrete = (scaled_coords is not None)
```

thay bằng (đặt SAU khối tính `pt_flags` / `user_declared_exact`, nên cần dời
đoạn đó lên trước nếu hiện đang nằm sau):

```python
    # Điểm vẽ tay có tọa độ rơi vào lưới pixel/40 sẽ lọt nhánh "rời rạc"
    # và bị so sánh bằng chính xác. Ép về nhánh dung sai tương đối.
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)
```

Lưu ý khi áp dụng:
- Thứ tự trong hàm phải là: đọc điểm, tính `user_declared_exact`, tính
  `scaled_coords`, rồi mới đặt `is_discrete`.
- Bộ test cũ có thể có assert `is_discrete == True` cho điểm `free` có tọa độ
  nguyên (test 17, 24). Nếu fail thì đó là assert cần đổi theo ngữ nghĩa mới,
  không phải lỗi của patch.
- `scale_factor` vẫn trả về như cũ.

## Sửa 4. Phía giao diện (cần làm tay, tôi chưa thấy mã canvas)

- Khi kéo thả (`<B1-Motion>` / `<ButtonRelease-1>`) một điểm `typed` hoặc
  `grid_snap` mà không bật snap, gán lại `source="dragged"`, `exact=False`.
- Khi tạo điểm midpoint/intersection, lưu `parents=[điểm_cha_1, điểm_cha_2]`.
- Điểm dựng hình cũ không có `parents` sẽ ra cờ `None` (chuyển sang heuristic),
  khác với trước đây là `True` vô điều kiện.
