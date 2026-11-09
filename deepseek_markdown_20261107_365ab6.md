# Lời giải bài toán "Trăm trâu trăm cỏ"

## Đề bài

> Trăm trâu, trăm cỏ  
> Trâu đứng ăn năm  
> Trâu nằm ăn ba  
> Lụ khụ trâu già  
> Ba con một bó  
> Hỏi có bao nhiêu con trâu đứng, trâu nằm, trâu già?

---

## Lời giải

### 1. Đặt ẩn

Gọi:

- \(x\): số trâu đứng
- \(y\): số trâu nằm
- \(z\): số trâu già

Điều kiện: \(x, y, z\) là các số nguyên dương.

### 2. Lập phương trình

Tổng số trâu là 100:

\[
x + y + z = 100 \quad (1)
\]

Tổng số bó cỏ là 100:

- Trâu đứng ăn 5 bó → \(5x\)
- Trâu nằm ăn 3 bó → \(3y\)
- Trâu già: 3 con ăn 1 bó → \(\dfrac{z}{3}\)

Nên:

\[
5x + 3y + \frac{z}{3} = 100 \quad (2)
\]

### 3. Giải hệ phương trình

Nhân (2) với 3:

\[
15x + 9y + z = 300 \quad (3)
\]

Lấy (3) trừ (1):

\[
(15x + 9y + z) - (x + y + z) = 300 - 100
\]

\[
14x + 8y = 200
\]

\[
7x + 4y = 100 \quad (4)
\]

Từ (4):

\[
y = \frac{100 - 7x}{4}
\]

Để \(y\) nguyên thì \(100 - 7x\) chia hết cho 4. Vì \(100 \equiv 0 \pmod{4}\) nên \(7x \equiv 0 \pmod{4}\), suy ra \(x \equiv 0 \pmod{4}\).

Đặt \(x = 4k\) (\(k\) nguyên dương). Thay vào (4):

\[
7(4k) + 4y = 100 \Rightarrow 28k + 4y = 100 \Rightarrow 7k + y = 25
\]

\[
y = 25 - 7k
\]

Và:

\[
z = 100 - x - y = 100 - 4k - (25 - 7k) = 75 + 3k
\]

### 4. Tìm nghiệm

Điều kiện dương:

- \(x = 4k > 0 \Rightarrow k \ge 1\)
- \(y = 25 - 7k > 0 \Rightarrow k \le 3\)
- \(z = 75 + 3k > 0\) luôn đúng với \(k \ge 1\)

Vậy \(k \in \{1, 2, 3\}\).

Ta có các nghiệm:

| \(k\) | Trâu đứng (\(x\)) | Trâu nằm (\(y\)) | Trâu già (\(z\)) |
|-------|------------------|------------------|------------------|
| 1     | 4                | 18               | 78               |
| 2     | 8                | 11               | 81               |
| 3     | 12               | 4                | 84               |

### 5. Kiểm tra lại

- **(4, 18, 78):** \(4+18+78=100\); cỏ: \(5\cdot4 + 3\cdot18 + 78/3 = 20+54+26=100\) ✓
- **(8, 11, 81):** \(8+11+81=100\); cỏ: \(40+33+27=100\) ✓
- **(12, 4, 84):** \(12+4+84=100\); cỏ: \(60+12+28=100\) ✓

### 6. Kết luận

Bài toán có **3 đáp án**:

1. Trâu đứng: **4**, trâu nằm: **18**, trâu già: **78**
2. Trâu đứng: **8**, trâu nằm: **11**, trâu già: **81**
3. Trâu đứng: **12**, trâu nằm: **4**, trâu già: **84**