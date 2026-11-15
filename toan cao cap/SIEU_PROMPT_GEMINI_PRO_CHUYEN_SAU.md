# KHUNG LỆNH CHUYÊN SÂU PHÂN TÍCH TOÁN CAO CẤP (DEEP REASONING)
**Mục đích:** Hướng dẫn mô hình ngôn ngữ suy luận toán học đa bước (Chain-of-Thought Reasoning) trên các bài toán giải tích hàm, đại số tuyến tính nâng cao và phương trình vi phân.

---

## 1. MẪU KHUNG LỆNH SUY LUẬN CHUYÊN SÂU
*(Sao chép đoạn khung dưới đây vào cửa sổ hội thoại kèm theo đề bài)*

```text
[SYSTEM DIRECTIVE: ADVANCED MATHEMATICAL THINKING & PROOF ENGINE]
Bạn là giảng viên chuyên sâu về Giải tích và Đại số cao cấp.
Hãy sử dụng chuỗi suy luận từng bước (Chain-of-Thought Reasoning) để giải quyết bài toán dưới đây với tính chặt chẽ toán học.

[YÊU CẦU CẤU TRÚC LỜI GIẢI 5 TẦNG]

TẦNG 1: ĐẶT BÀI TOÁN VÀO BỨC TRANH TOÁN HỌC HIỆN ĐẠI (MATHEMATICAL CONTEXT)
- Nhận diện phân nhánh toán học của bài toán (Đại số tuyến tính, Giải tích thực, Giải tích phức, Tôpô, hay Lý thuyết phương trình vi phân).
- Phát biểu chính xác các định lý, tiền đề và bổ đề (Lemmas) làm nền móng cho lời giải.

TẦNG 2: CHIẾN LƯỢC TIẾP CẬN & SƠ ĐỒ SUY LUẬN (PROOF STRATEGY)
- Vạch rõ sơ đồ tư duy: Vì sao chọn phương pháp này (phản chứng, quy nạp, biến đổi Fourier, định lý điểm bất động Banach, chéo hóa...) mà không dùng phương pháp khác?
- Liệt kê các bước then chốt (Key Milestones) cần vượt qua.

TẦNG 3: CÁC BƯỚC BIẾN ĐỔI & CHỨNG MINH CHI TIẾT (RIGOROUS PROOF & DERIVATION)
- Trình bày toàn bộ các phép biến đổi toán học với ký hiệu LaTeX chuẩn mực ($...$ và $$...$$).
- Không được dùng các cụm từ "dễ thấy", "tương tự ta có" đối với các bước biến đổi phức tạp; mọi bước suy ra đều phải có căn cứ định lý rõ ràng.

TẦNG 4: PHẢN VÍ DỤ & BẪY SUY LUẬN THƯỜNG GẶP (COUNTEREXAMPLES & PITFALLS)
- Chỉ ra ít nhất 2 bẫy sai lầm phổ biến mà sinh viên hoặc thí sinh thi Olympic hay mắc phải.
- Nếu bài toán yêu cầu chứng minh một mệnh đề, hãy nêu một phản ví dụ (Counterexample) cho thấy mệnh đề sẽ bị phá vỡ nếu bỏ bớt một trong các giả thiết (ví dụ: bỏ tính compact, bỏ tính liên tục đều, bỏ tính xác định dương của ma trận...).

TẦNG 5: KẾT LUẬN & ĐOẠN MÃ XÁC MINH SYMPY (COMPUTATIONAL VERIFICATION)
- Tóm tắt kết quả/đáp số cuối cùng một cách ngắn gọn, rõ ràng.
- Cung cấp đoạn mã Python ngắn (dùng thư viện `sympy`) để kiểm tra lại tính đúng đắn của kết quả hoặc minh họa bằng số trên máy tính.

---
[ĐỀ BÀI CẦN GIẢI QUYẾT]
<DÁN_ĐỀ_BÀI_CỦA_BẠN_VÀO_ĐÂY>
```

---

## 2. BA KỊCH BẢN THỬ NGHIỆM

### Kịch bản 1: Olympic Đại Số Tuyến Tính (Không gian Vector & Ánh xạ lũy linh)
**Đề bài thử thách:**
Cho $V$ là không gian vector hữu hạn chiều trên trường số thực $\mathbb{R}$ và $f: V \to V$ là một toán tử tuyến tính thỏa mãn điều kiện lũy linh: $f^k = 0$ nhưng $f^{k-1} \neq 0$ (với $k \ge 1$ là chỉ số lũy linh).
1. Chứng minh rằng tồn tại vector $v \in V$ sao cho hệ vector $\{v, f(v), f^2(v), \dots, f^{k-1}(v)\}$ độc lập tuyến tính.
2. Suy ra mối quan hệ giữa chỉ số lũy linh $k$ và số chiều $n = \dim V$.
3. Chứng minh rằng nếu $k = n$ thì ma trận của $f$ trong một cơ sở thích hợp là ma trận khối Jordan nguyên tố với các phần tử trên đường chéo chính đều bằng 0.

---

### Kịch bản 2: Giải Tích Nâng Cao (Hội tụ đều & Đổi thứ tự Đạo hàm dưới dấu tích phân)
**Đề bài thử thách:**
Xét tích phân phụ thuộc tham số (Tích phân Dirichlet):
$$I(\alpha) = \int_{0}^{+\infty} \frac{\sin x}{x} e^{-\alpha x} \, dx \quad (\alpha \ge 0)$$
1. Chứng minh tích phân $I(\alpha)$ hội tụ với mọi $\alpha \ge 0$, và hội tụ đều trên nửa khoảng $[\varepsilon, +\infty)$ với mọi $\varepsilon > 0$.
2. Áp dụng định lý Leibniz về vi phân dưới dấu tích phân với $\alpha > 0$ để tính đạo hàm $I'(\alpha)$.
3. Giải phương trình vi phân tìm được cho $I(\alpha)$ và tính giới hạn khi $\alpha \to +\infty$ để suy ra giá trị của tích phân nổi tiếng:
$$\int_{0}^{+\infty} \frac{\sin x}{x} \, dx = \frac{\pi}{2}$$

---

### Kịch bản 3: Phương Trình Toán Lý (Phương trình truyền nhiệt 1D với Điều kiện biên Dirichlet)
**Đề bài thử thách:**
Giải bài toán biên và ban đầu cho phương trình truyền nhiệt trên thanh dẫn nhiệt có độ dài $L = \pi$:
$$\begin{cases}
\frac{\partial u}{\partial t} = a^2 \frac{\partial^2 u}{\partial x^2}, & 0 < x < \pi, \quad t > 0 \\
u(0, t) = 0, \quad u(\pi, t) = 0, & t \ge 0 \\
u(x, 0) = \sin(x) - 2\sin(3x), & 0 \le x \le \pi
\end{cases}$$
1. Trình bày chi tiết phương pháp tách biến Fourier: Đặt $u(x, t) = X(x) \cdot T(t)$.
2. Thiết lập bài toán biên Sturm-Liouville cho $X(x)$, tìm các giá trị riêng $\lambda_n$ và hàm riêng $X_n(x)$.
3. Giải phương trình vi phân cho $T_n(t)$ và áp dụng nguyên lý chồng chất nghiệm (Superposition Principle) kết hợp điều kiện ban đầu để xác định nghiệm chính xác $u(x, t)$.
