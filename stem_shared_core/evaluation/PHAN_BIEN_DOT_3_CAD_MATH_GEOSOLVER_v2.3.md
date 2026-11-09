# Phản biện đợt 3: CAD Math Studio & GeoSolver 2D (báo cáo phiên bản 2.3)

**Tài liệu được phản biện:** `TONG_HOP_BAO_CAO_KHOA_HOC_CHO_CLAUDE_PHAN_BIEN.md`, phiên bản 2.3 (07/11/2026)

**Phạm vi và giới hạn:** Người phản biện chỉ có báo cáo, không có mã nguồn, bộ 30 bài hay số liệu thô. Các khẳng định kiểu "đã thực hiện trong mã nguồn" chưa thể kiểm chứng. Những gì kiểm tra được bằng tính toán độc lập (ma trận Diophantine, khoảng tin cậy Wilson) được ghi rõ ở mục 1.

---

## 0. Nhận định chung

Phiên bản 2.3 tốt hơn rõ rệt so với 2.2: thừa nhận đúng các lỗi lập luận (tính thừa của $\mathcal{D}_{\text{rad}}$, khoảng chặn đóng không tổng quát), đưa ma trận cụ thể để tái lập, thêm baseline SymPy `check=True`, báo cáo khoảng tin cậy, và thu hẹp phạm vi. Đây là cách làm khoa học đúng hướng.

Tuy nhiên, việc đưa thêm Nhánh C làm lộ ra một vấn đề lớn hơn: **trên chỉ tiêu đáp số, hệ thống đề xuất không hơn SymPy mặc định**. Đóng góp thực sự (nếu có) nằm ở lời giải sư phạm, mà phần này hiện **chưa có bất kỳ phép đo nào**. Đó là điểm cần giải quyết nhất.

---

## 1. Những điểm đã kiểm chứng và đã được giải quyết tốt

**Đã tự kiểm tra bằng tính toán độc lập (đều khớp báo cáo):**

- **Ca 1:** $x=\frac{7z-500}{3}$, $y=\frac{800-10z}{3}$; điều kiện nguyên cho $z\equiv2\pmod3$; miền $z\in[72,79]$ cho $z\in\{74,77\}$, nghiệm $(6,20,74)$ và $(13,10,77)$. Đúng.
- **Ca 2:** hạng của ma trận là 3; họ nghiệm $a=2d-10,\ b=20-2d,\ c=20-d$ thỏa cả ba phương trình với mọi $d$; bốn nghiệm nguyên dương $(2,8,14,6),(4,6,13,7),(6,4,12,8),(8,2,11,9)$. Đúng.
- **Ca 3:** $x=z-5,\ y=2$, nghiệm nguyên dương với $z\ge6$. Đúng.
- **Khoảng tin cậy Wilson 95%:** $[3.5\%, 25.6\%]$ cho 3/30 và $[88.6\%, 100\%]$ cho 30/30. Đúng.
- **Chênh thời gian D − C:** $16.31-15.10=1.21$ ms. Đúng số học.

**Đã giải quyết tốt về mặt lập luận:**

- Thừa nhận $\mathcal{D}_{\text{rad}}$ thừa và điều kiện then chốt là $g(r)\ge0$.
- Thừa nhận $|\sqrt{f(r)}-g(r)|=2\max(0,-g(r))$ và hạn chế của residual số thực.
- Chia hệ Diophantine thành các trường hợp thay vì luôn giả định miền chặn.
- Báo cáo thẳng kết quả Nhánh C = 100%, không giấu baseline mạnh.
- Mục "Hạn chế" cụ thể, có kế hoạch.

---

## 2. Các vấn đề còn lại, theo mức độ ưu tiên

### 2.1. Nhánh B là một đồng nhất thức toán học, không phải kết quả thực nghiệm (mức: cao)

Báo cáo viết rằng kết quả của Nhánh B là "minh chứng thực nghiệm sinh động". Điều này không chính xác. Vì mọi nghiệm của $f=g^2$ đều có $f(r)=g(r)^2\ge0$, bộ lọc $f(x)\ge0$ **không bao giờ loại được nghiệm nào**. Do đó, Nhánh B ≡ Nhánh A trên **mọi** đầu vào, và việc cả hai cùng đạt 3/30 là hệ quả tất yếu, không cần chạy thực nghiệm để biết.

**Đề xuất:**

- Gộp A và B thành một dòng ("bình phương rồi nhận hết; lọc điều kiện dưới căn không làm khác kết quả") và nêu rõ đây là **mệnh đề toán học**, kèm chứng minh một dòng.
- Nếu muốn mô phỏng sai lầm của học sinh, hãy lấy bằng chứng từ **bài làm thật của học sinh** (ngay cả 20–30 bài làm ẩn danh) thay vì mô phỏng bằng thuật toán.

### 2.2. Đóng góp thực sự chưa được đo (mức: cao)

Bảng 3.2 cho thấy C và D cùng 30/30 và cùng 0 False-Positive. Báo cáo chuyển trọng tâm sang "lời giải sư phạm", nhưng:

1. Hàng "Năng lực giải thích sư phạm" chỉ là **ô đánh dấu Có/Không**, không phải phép đo chất lượng.
2. Khảo sát giáo viên vẫn ở dạng **kế hoạch** (mục 6), chưa có dữ liệu.
3. Chưa so sánh với các công cụ **đã có lời giải từng bước** (theo hiểu biết của tôi, một số công cụ như Wolfram Alpha bản có lời giải chi tiết, Symbolab, Maple, GeoGebra có chức năng này ở nhiều mức). Phát biểu "khắc phục tính hộp đen của CAS hiện hành" chỉ đúng với `sp.solve`, không đúng với toàn bộ CAS. Cần định vị lại: so sánh với công cụ nào, ở khía cạnh nào (ví dụ: có nêu *vì sao* nghiệm bị loại bằng ngôn ngữ cấp THPT không).

**Đề xuất:** Đưa vào ít nhất một phép đo: 5–10 giáo viên chấm lời giải của hệ thống và của một công cụ so sánh trên cùng 10 bài, theo rubric 3 tiêu chí (đúng, đủ, dễ hiểu), chấm mù (không biết nguồn). Báo cáo trung vị và dải điểm. Cho đến khi có dữ liệu này, nên viết "hướng tới hỗ trợ dạy học", không viết như đã đạt.

### 2.3. Xác định dấu đại số: cần mô tả hành vi dự phòng và các ca biên (mức: cao)

Việc thay residual số thực bằng xác định dấu ký hiệu là đúng hướng. Các điểm cần làm rõ:

1. **`sp.ask(Q.nonnegative(...))` trên biểu thức chứa căn có thể trả `None`** trong một số ca (theo hiểu biết của tôi, cần thử nghiệm trên phiên bản đang dùng). Với nghiệm hữu tỷ, dùng `Rational` là chính xác tuyệt đối. Với nghiệm vô tỷ, thuộc tính `expr.is_nonnegative` hoặc đánh giá số với độ chính xác tăng dần là cách thực tế, nhưng riêng trường hợp **bằng đúng 0** cần kiểm tra ký hiệu (`simplify`, `minimal_polynomial`, hoặc `equals`).
2. **Khi suy diễn ký hiệu "chưa xác định được", hệ thống làm gì?** Báo cáo nói dùng residual số thực làm kênh phụ. Nếu kết quả phụ này vẫn quyết định nhận hay loại thì lỗi ban đầu vẫn tồn tại ở nhánh dự phòng. Thiết kế an toàn: trả về trạng thái **"không xác định được"** và hiển thị cho người dùng, **không âm thầm nhận hoặc loại**.
3. **Cần có ca kiểm thử biên:** $g(r)=0$ đúng tại nghiệm (khi đó $f(r)=0$ cũng đúng, nghiệm hợp lệ); $g(r)$ rất nhỏ nhưng âm; hệ số lớn; nghiệm vô tỷ dạng $a+b\sqrt{c}$ với $g(r)$ gần 0.

### 2.4. Phân loại hệ Diophantine: còn các lỗ hổng logic (mức: cao)

Ba trường hợp trong mục 2.3 của báo cáo tiến bộ, nhưng quy tắc nêu ra chưa đủ:

1. **Quy tắc "hệ số tham số đều không âm ⇒ vô hạn nghiệm" sai khi có biểu thức hằng.** Ví dụ $x-z=-5,\ y=0$ (ma trận $\begin{bmatrix}1&0&-1\\0&1&0\end{bmatrix}$, $\mathbf{b}=(-5,0)^T$): mọi hệ số của $z$ đều không âm nhưng $y\equiv0$ không dương, nên hệ **vô nghiệm**. Phải kiểm tra các ràng buộc có hệ số bằng 0 (hằng số phải $>0$) trước khi kết luận.
2. **Thiếu trường hợp "vô nghiệm nguyên dù có nghiệm thực dương".** Ví dụ $2x-2z=1,\ y=5$: nghiệm thực dương tồn tại, nhưng $x=z+\tfrac12$ không bao giờ nguyên. Báo cáo chỉ liệt kê `INFEASIBLE_EMPTY` cho miền rỗng hoặc hệ không nhất quán. Cần thêm trạng thái kiểu `INFEASIBLE_NO_INTEGER_POINT` khi hệ đồng dư vô nghiệm. Điều này cũng ảnh hưởng đến `UNBOUNDED_INFINITE`: chỉ kết luận vô hạn khi tồn tại ít nhất một lớp đồng dư thỏa.
3. **Điều kiện đồng dư không phải luôn là một modulus đơn $D$.** Mỗi biến phụ thuộc cho một đồng dư tuyến tính $a p\equiv b \pmod m$ có thể vô nghiệm hoặc cho nhiều lớp; cần giải hệ bằng CRT (hoặc hợp nhất từng cặp, với kiểm tra tương thích). Một chốt an toàn rẻ: **thế ngược từng nghiệm liệt kê vào hệ gốc bằng số hữu tỷ chính xác** trước khi in.
4. **Các trường hợp ngoài phạm vi phải thất bại an toàn.** Phạm vi đã giới hạn ở $d=1$. Cần nêu hành vi khi $d=0$ (nghiệm duy nhất: chỉ cần kiểm tra dương và nguyên) và $d\ge2$ (thông báo "chưa hỗ trợ", **không** trả kết quả sai hoặc im lặng sai).
5. **Chọn tham số:** nêu rõ tham số tự do được chọn là một biến gốc nguyên hay một tham số hữu tỷ, vì điều này quyết định điều kiện nguyên.
6. **Bộ ca kiểm thử nên mở rộng** vượt 3 ca đã nêu (cả 3 đều dương và $d=1$): thêm hệ không nhất quán, vô nghiệm nguyên, hệ số hằng bằng 0 hoặc âm, $d=0$, $d=2$ (kiểm tra thất bại an toàn), hệ số lớn.

### 2.5. Thiết kế đánh giá: các điểm chưa được giải quyết (mức: trung bình – cao)

1. **Oracle đáp án vẫn chưa được mô tả.** "Bài đúng" được xác định bằng cách nào (giải tay hai người, quét số độc lập, hay chính SymPy)? Nếu C được dùng làm chuẩn thì "C đúng 100%" là tự quy chiếu. Cần nêu rõ.
2. **Chưa có tập giữ riêng thực sự.** Mục 6 mới là kế hoạch 100 bài ngẫu nhiên. Lưu ý các bài sinh ngẫu nhiên có phân phối khác bài sách giáo khoa; nên có **cả hai**: tập sinh ngẫu nhiên (đo độ bền và tính đầy đủ) và tập bài thực tế chưa dùng khi phát triển (đo tính ứng dụng). Với ngẫu nhiên, nên báo cáo tỷ lệ bài có nghiệm ngoại lai trong mẫu.
3. **Số liệu thời gian:** thiếu cấu hình máy, số lần lặp, trung vị và độ lệch. Chênh A–B là 1.37 ms cho một phép lọc không làm gì (theo 2.1), cho thấy dao động đo đạc có thể cùng bậc với chênh D–C (1.21 ms). Cần đo lặp nhiều lần trước khi kết luận.
4. **Timeout 2.0 giây:** nếu cài bằng thread thì thường không dừng được tác vụ SymPy đang chạy. Nên chạy từng ca trong tiến trình con (`multiprocessing`/`subprocess`) có thể bị kết thúc khi quá giờ.
5. **Thiếu bất biến về tính đầy đủ (completeness):** mọi nghiệm thực của phương trình gốc có nằm trong kết quả không? Kiểm tra bằng quét số dày đặc trên miền xác định hoặc bằng cài đặt tham chiếu dạng đóng cho $\sqrt{ax+b}=cx+d$.

### 2.6. Thuật toán AABB (mức: trung bình)

Việc chuyển sang `get_window_extent` và đổi về tọa độ dữ liệu là cải tiến đúng. Còn thiếu:

1. **Chưa có đánh giá định lượng:** ví dụ "số cặp nhãn chồng lấn trước/sau" trên một bộ hình đa dạng (số điểm, độ dài nhãn, mức zoom), thay vì chỉ ảnh minh họa.
2. **Chưa nêu hành vi khi cả 8 hướng đều thất bại** (vùng dày đặc), cũng như độ phức tạp $O(n^2)$ cho số nhãn lớn.
3. **Cơ chế Fail-Fast** vẫn chưa có ví dụ cụ thể (đầu vào thiếu điểm → thông báo gì).
4. **Hộp bao phụ thuộc lần vẽ:** `get_window_extent` cần renderer và thường cần ít nhất một lần `draw`; nên mô tả chu trình vẽ → đo → dịch → vẽ lại, và điều kiện dừng.
5. **Mới xét va chạm nhãn–nhãn:** báo cáo đã tự nêu hạn chế này, nên giữ như một hạn chế chính thức.

### 2.7. Ngôn ngữ và cách trình bày (mức: trung bình)

1. **Từ tuyệt đối vẫn còn**, trái với "tôn chỉ" đã tuyên bố ở đầu: "**tuyệt đối** không chạy vòng lặp vô nghĩa" (2.3), "**hoàn toàn** vô hiệu", "**hoàn toàn** không thể hiện" (2.1, 3.2), "tiếp thu **toàn diện**/**trọn vẹn**". Nên thay bằng mô tả hành vi cụ thể ("hệ thống phát hiện trường hợp không chặn trên và xuất họ nghiệm tham số").
2. **Cụm "đã thực hiện trong mã nguồn"** cần kèm bằng chứng kiểm chứng được: tên hàm, tên test, đường dẫn, hoặc kết quả chạy. Nếu không, đây chỉ là khẳng định.
3. **Cụm "phản biện độc lập".** Các đợt phản biện hiện đến từ công cụ AI (Claude, ChatGPT) do chính nhóm tác giả đặt câu hỏi. Đây là **tư vấn kỹ thuật hữu ích**, nhưng chưa phải thẩm định độc lập: tôi không chạy được mã, không có bằng chứng thực nghiệm của riêng mình, và có thể sai. Trong hồ sơ nộp, nên ghi nhận như "tham vấn bằng công cụ AI" và bổ sung **ít nhất một phản biện của người thật** (giáo viên hướng dẫn, giảng viên toán/tin).
4. **Tên tệp và tiêu đề hướng tới "Claude phản biện"** không phù hợp với tài liệu nộp cho hội đồng; nên tách bản nội bộ và bản nộp.

---

## 3. Đề xuất sửa câu chữ (mẫu)

| Đoạn hiện tại | Đề xuất |
| :--- | :--- |
| "Kết quả Nhánh B … chính là minh chứng thực nghiệm sinh động" | "Do $f(r)=g(r)^2\ge0$ tại mọi nghiệm của phương trình hệ quả, bộ lọc $f\ge0$ không loại được nghiệm nào; do đó Nhánh B trùng Nhánh A (mệnh đề toán học, không phải kết quả thực nghiệm)." |
| "Hệ thống tuyệt đối không chạy vòng lặp vô nghĩa" | "Khi miền nghiệm không chặn trên, hệ thống xuất họ nghiệm tham số và ba nghiệm nhỏ nhất, không liệt kê vô hạn." |
| "Khắc phục tính hộp đen của các CAS hiện hành" | "Bổ sung lời giải từng bước cho `sp.solve`; việc so sánh với các công cụ có lời giải từng bước khác là công việc tiếp theo." |
| "Hệ thống đạt độ chính xác tương đương SymPy `check=True` nhưng bổ sung được chuỗi giải thích" | Giữ nguyên, thêm: "Chất lượng chuỗi giải thích chưa được đánh giá bởi người dùng; khảo sát giáo viên đang được thực hiện." |

---

## 4. Danh sách việc cần làm, theo thứ tự ưu tiên

| # | Việc | Mức ưu tiên |
|---|------|-------------|
| 1 | Gộp A và B, trình bày là mệnh đề toán học; bỏ cụm "thực nghiệm sinh động" | Cao |
| 2 | Có ít nhất một phép đo sư phạm (giáo viên chấm mù, rubric, so sánh với công cụ có lời giải từng bước) | Cao |
| 3 | Mô tả hành vi dự phòng của xác định dấu ("không xác định được", không im lặng quyết định) và thêm ca biên $g(r)=0$ | Cao |
| 4 | Sửa phân loại Diophantine: ràng buộc hằng, vô nghiệm nguyên, $d=0$, $d\ge2$ thất bại an toàn; CRT; thế ngược xác minh | Cao |
| 5 | Nêu oracle đáp án; tạo tập giữ riêng (ngẫu nhiên + bài thực tế); thêm bất biến về tính đầy đủ | Cao |
| 6 | Đo thời gian đúng chuẩn (cấu hình máy, lặp, trung vị, độ lệch); timeout bằng tiến trình con | Trung bình |
| 7 | Đánh giá định lượng AABB; mô tả hành vi dự phòng và Fail-Fast bằng ví dụ | Trung bình |
| 8 | Loại các từ tuyệt đối còn sót; gắn bằng chứng cho mọi "đã thực hiện" | Trung bình |
| 9 | Bổ sung phản biện của người thật; ghi nhận đúng vai trò của công cụ AI | Trung bình |

---

## 5. Kết luận

Báo cáo đã trưởng thành rõ về trung thực học thuật và có các ví dụ kiểm chứng được. Hai việc quyết định chất lượng cuối cùng của hồ sơ là: **(a)** chứng minh giá trị sư phạm bằng dữ liệu thay vì bảng có/không, vì về đáp số hệ thống chỉ bằng SymPy `check=True`; và **(b)** làm chặt các ca biên của bộ giải Diophantine và xác định dấu, nơi các khẳng định hiện tại vẫn rộng hơn bằng chứng.

Nếu bạn dán mã nguồn của bộ xác định dấu và bộ phân loại Diophantine (hoặc danh sách 30 bài đã ẩn danh), tôi có thể rà soát cụ thể từng hàm và đề xuất ca kiểm thử.

---

*Phản biện này dựa hoàn toàn trên nội dung báo cáo và các phép kiểm tra độc lập nêu ở mục 1. Nhận định về hành vi của SymPy cần được đối chiếu với phiên bản và mã nguồn thực tế của dự án.*
