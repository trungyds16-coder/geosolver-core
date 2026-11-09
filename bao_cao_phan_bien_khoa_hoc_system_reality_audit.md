# BÁO CÁO PHẢN BIỆN KHOA HỌC -- SYSTEM REALITY AUDIT

**Đối tượng đánh giá:** Phần mềm hỗ trợ giải toán Đại số và Hình học
phẳng 2D trên Windows.

**Góc nhìn:** Reviewer trong lĩnh vực Khoa học máy tính, phần mềm giáo
dục và AI ứng dụng.

## I. Kết luận sơ bộ của phản biện

Theo mô tả hiện tại, dự án phù hợp nhất với các nhóm:

-   Applied Software Engineering.
-   Computer-Assisted Mathematics Education.
-   Educational Software / Technology-Enhanced Learning.
-   Tool Development and Experimental Evaluation.

Dự án có giá trị kỹ thuật ứng dụng, nhưng **chưa đủ cơ sở để tuyên bố có
đóng góp thuật toán hoặc phương pháp AI mới**.

Việc tích hợp nhiều công nghệ không đồng nghĩa với tạo ra một đóng góp
khoa học mới. Muốn vượt khỏi phạm vi đồ án lập trình, tác giả cần chứng
minh hệ thống giải quyết một vấn đề cụ thể tốt hơn hoặc đáng tin cậy hơn
những cách tiếp cận hiện có.

## II. Phản biện kỹ thuật: Sai lệch trong mô tả xử lý phương trình căn

Ví dụ:

\[ `\sqrt{x-1}`{=tex}=3-x \]

Sau khi bình phương:

\[ x-1=(3-x)\^2 \]

Suy ra:

\[ x\^2-7x+10=0 \]

Do đó:

\[ x`\in`{=tex}{2,5} \]

Điều kiện xác định của căn là:

\[
`\mathcal `{=tex}D={x`\mid `{=tex}x-1`\geq 0`{=tex}}=\[1,+`\infty`{=tex})
\]

Tuy nhiên, **(x=5) vẫn thuộc tập xác định**, nên chỉ dùng điều kiện dưới
căn không âm thì không thể loại nghiệm này.

Với phương trình:

\[ `\sqrt{f(x)}`{=tex}=g(x) \]

cần có đồng thời:

\[ f(x)`\geq0`{=tex},`\qquad `{=tex}g(x)`\geq0`{=tex} \]

Sau đó vẫn phải thay nghiệm vào phương trình ban đầu.

Trong ví dụ trên:

\[ 3-x`\geq0`{=tex}`\Rightarrow `{=tex}x`\leq3`{=tex} \]

Vì vậy (x=5) bị loại, còn (x=2) được chấp nhận.

### Quy trình nên triển khai

1.  Phân tích điều kiện xác định của tất cả biểu thức.
2.  Bổ sung điều kiện dấu cần thiết khi biến đổi, đặc biệt trước khi
    bình phương.
3.  Sinh nghiệm ứng viên bằng SymPy.
4.  Đối chiếu nghiệm với các điều kiện cần.
5.  Thay nghiệm vào phương trình gốc để xác nhận.

Với hệ phương trình căn, phải xử lý điều kiện trên từng phương trình và
kiểm tra đồng thời toàn bộ hệ.

Không nên mô tả hệ thống như một bộ giải phương trình tổng quát nếu chưa
kiểm định phạm vi hỗ trợ.

## III. Đánh giá bản chất đóng góp khoa học

### 1. Phân hệ Đại số

  -----------------------------------------------------------------------
  Thành phần                          Nhận định khoa học
  ----------------------------------- -----------------------------------
  Sử dụng SymPy để giải phương trình  Ứng dụng công nghệ có sẵn

  Tự động xác định điều kiện xác định Kỹ thuật xử lý bài toán toán học

  Lọc nghiệm ngoại lai                Có giá trị nếu quy trình đầy đủ và
                                      được kiểm thử

  Khảo sát hàm bậc ba                 Tích hợp tính toán và trực quan hóa

  Sử dụng NumPy/SciPy                 Ứng dụng thuật toán số có sẵn

  Giao diện Tkinter                   Phát triển sản phẩm phần mềm
  -----------------------------------------------------------------------

Điểm có tiềm năng nhất không nằm ở việc gọi `solve()` của SymPy, mà nằm
ở **lớp kiểm soát toán học được xây dựng xung quanh bộ giải**.

Có thể nghiên cứu pipeline:

\[ `\text{Input}`{=tex} `\rightarrow`{=tex}
`\text{Domain Analysis}`{=tex} `\rightarrow`{=tex}
`\text{Symbolic Solving}`{=tex} `\rightarrow`{=tex}
`\text{Candidate Filtering}`{=tex} `\rightarrow`{=tex}
`\text{Original Equation Verification}`{=tex} `\rightarrow`{=tex}
`\text{Explanation}`{=tex} \]

Nếu pipeline này được thiết kế rõ ràng, kiểm thử có hệ thống và chứng
minh giảm nghiệm sai so với cách gọi SymPy trực tiếp, nó có thể trở
thành một đóng góp kỹ thuật đáng trình bày.

Tuy nhiên, cần gọi đúng bản chất: đây là quy trình kiểm soát và hậu xử
lý lời giải, chưa phải thuật toán giải đại số mới.

Đối với Nelder--Mead, cần lưu ý đây là phương pháp tối ưu số dựa trên
simplex, không phải bằng chứng hệ thống đã tìm được cực trị toàn cục.
Kết quả phụ thuộc vào bài toán, điểm khởi tạo và tiêu chuẩn hội tụ. Nên
đánh giá trên nhiều điểm khởi tạo và đối chiếu với bài toán có nghiệm
chuẩn.

### 2. Phân hệ Hình học phẳng 2D

Cần phân biệt:

-   Kiểm tra dữ liệu hình học.
-   Dựng hình và trực quan hóa.
-   Giải bài toán hình học hoặc chứng minh định lý.

Những gì được mô tả hiện thuộc hai nhóm đầu, chưa chứng minh được nhóm
thứ ba.

  -----------------------------------------------------------------------
  Chức năng               Giá trị thực tế         Giới hạn
  ----------------------- ----------------------- -----------------------
  Kiểm tra thiếu đỉnh     Ngăn dữ liệu không đầy  Kiểm tra đầu vào
                          đủ                      

  Phát hiện tam giác suy  Ngăn hình sai cấu trúc  Chưa phải chứng minh
  biến                                            hình học

  Kiểm tra khoảng cách    Cảnh báo điểm gần nhau  Chưa kiểm tra chính xác
  điểm                                            va chạm nhãn

  Canvas 2D               Dựng và trình bày hình  Không tự suy luận định
                                                  lý
  -----------------------------------------------------------------------

**Ngưỡng diện tích (10\^{-4}):** Ngưỡng tuyệt đối phụ thuộc hệ đơn vị và
tỷ lệ tọa độ. Nên sử dụng tiêu chuẩn suy biến tương đối, có xét kích
thước hình và sai số số học.

**Ngưỡng 15 px:** Khoảng cách giữa hai điểm không tương đương với việc
hai nhãn bị đè lên nhau. Độ dài nhãn, kích thước font, DPI và mức zoom
đều ảnh hưởng. Nên đo vùng bao của chữ sau khi chuyển đổi tọa độ Canvas.

Bộ dữ liệu có 400 bài Conic nhưng phần mô tả chức năng chưa chỉ ra hệ
thống thực hiện thao tác gì trên các bài toán Conic. Nếu chỉ dùng chúng
làm dữ liệu kiểm thử thì cần nói rõ, không nên khiến người đọc hiểu rằng
hệ thống đã có bộ giải Conic hoàn chỉnh.

## IV. Những điểm yếu cốt tử mà Reviewer có thể bắt bẻ

### 1. Chưa có bằng chứng hệ thống tốt hơn công cụ hiện có

Reviewer có thể hỏi:

> Why should users choose this system instead of using SymPy directly,
> GeoGebra, Wolfram Alpha, or existing mathematics software?

Giao diện dễ sử dụng, nhiều chức năng và tích hợp AI chưa đủ để chứng
minh ưu thế khoa học.

Cần chỉ ra giá trị bổ sung, chẳng hạn:

-   Hạn chế nghiệm ngoại lai thông qua quy trình kiểm soát điều kiện
    toán học.
-   Phát hiện và ngăn lỗi dữ liệu hình học trước khi dựng hình.
-   Kết hợp kết quả tính toán có cấu trúc với lời giải dễ hiểu.
-   Chạy cục bộ các chức năng tính toán cốt lõi, không phụ thuộc dịch vụ
    đám mây.

Các tuyên bố này phải được kiểm chứng bằng thử nghiệm.

### 2. Dữ liệu kiểm định chưa đủ sức chứng minh độ tin cậy

1.000 bài toán tự sinh và khoảng 40 bài toán đề thi thật là nền tảng tốt
cho bộ kiểm thử ban đầu, nhưng chưa tự động trở thành benchmark khoa học
có giá trị cao.

Reviewer sẽ hỏi:

-   Bài toán có đáp án chuẩn được xác minh độc lập không?
-   Các bài tự sinh có trùng cấu trúc và chỉ khác tham số không?
-   Độ khó được phân loại theo tiêu chí nào?
-   Bài thi thật được chuyên gia đối chiếu hay chỉ chạy thử?
-   Có trường hợp trả về nghiệm sai nhưng vẫn đánh dấu thành công không?
-   Có trường hợp không giải được nhưng vẫn sinh lời giải có vẻ hợp lý
    không?

Không nên chia dữ liệu ngẫu nhiên đơn thuần nếu nhiều bài được sinh từ
cùng một mẫu. Nên giữ riêng một số họ bài toán hoặc cấu trúc tham số để
kiểm tra khả năng xử lý những trường hợp chưa dùng trong quá trình phát
triển.

### 3. Thiếu đối chứng và số liệu định lượng

Không nên chỉ báo cáo rằng hệ thống giải thành công 1.040 bài toán.

Các chỉ số nên có:

  Chỉ số                    Ý nghĩa
  ------------------------- -------------------------------------------
  Exact solution accuracy   Tỷ lệ tìm đúng toàn bộ tập nghiệm
  False positive rate       Tỷ lệ chấp nhận nghiệm sai
  False negative rate       Tỷ lệ bỏ sót nghiệm đúng
  Solve coverage            Tỷ lệ bài thuộc phạm vi hỗ trợ được xử lý
  Execution time            Thời gian xử lý
  Failure rate              Tỷ lệ lỗi hoặc không đưa ra kết quả

Với hình học, đánh giá thêm tỷ lệ phát hiện đúng hình suy biến, tỷ lệ
cảnh báo nhầm và tỷ lệ va chạm nhãn thực tế.

Một thử nghiệm có giá trị là so sánh:

1.  SymPy trực tiếp.
2.  SymPy kết hợp lớp xử lý điều kiện xác định.
3.  SymPy kết hợp điều kiện, lọc nghiệm và kiểm tra lại phương trình
    gốc.

Nếu phiên bản thứ ba giảm nghiệm ngoại lai mà không làm mất nghiệm đúng,
bạn có bằng chứng thực nghiệm cho giá trị của lớp xử lý do mình phát
triển.

### 4. Chưa có đánh giá tác động giáo dục

Nếu gửi vào hội nghị giáo dục, Reviewer có thể hỏi:

> Does the proposed software actually improve students' mathematical
> learning?

Cần phân biệt:

-   Hệ thống có giải được bài toán hay không.
-   Học sinh có hiểu cách giải hơn hay không.
-   Học sinh có tiến bộ sau khi sử dụng hay không.

Một công cụ giải toán chính xác chưa chắc là công cụ dạy toán hiệu quả.

Để chứng minh tác động giáo dục, nên thử nghiệm với học sinh và giáo
viên, đánh giá mức độ dễ sử dụng, thời gian hoàn thành, khả năng hiểu
lời giải và kết quả kiểm tra trước/sau. Nếu kết luận về tác động học
tập, cần thiết kế đối chứng phù hợp.

### 5. Mâu thuẫn trong tuyên bố offline

Phần mềm chạy offline nhưng Gemini/DeepSeek API cần Internet. Nên phân
biệt:

-   Các chức năng tính toán, xử lý biểu thức và dựng hình chạy cục bộ.
-   Chức năng tạo lời giải bằng AI cần kết nối Internet và dịch vụ API.

Cách viết phù hợp:

> Core mathematical computation runs locally; optional AI-assisted
> explanation requires an external API connection.

Cần công khai điều này vì liên quan đến triển khai, quyền riêng tư dữ
liệu và phụ thuộc nhà cung cấp.

## V. Vì sao không nên dùng Neuro-Symbolic, Formal Verification và Deep Learning?

  -----------------------------------------------------------------------
  Thuật ngữ               Có thể dùng?            Lý do
  ----------------------- ----------------------- -----------------------
  Symbolic Computation    Có                      Sử dụng SymPy xử lý
                                                  biểu thức và phương
                                                  trình ký hiệu

  LLM-assisted            Có                      Dùng API mô hình ngôn
  Explanation                                     ngữ diễn đạt lời giải

  Hybrid CAS--LLM System  Có                      Mô tả việc phối hợp CAS
                                                  và LLM

  Neuro-Symbolic AI       Chưa đủ cơ sở           Chưa có tích hợp thực
                                                  chất giữa học thần kinh
                                                  và suy luận ký hiệu

  Formal Verification     Không                   Chưa có đặc tả hình
                                                  thức và bộ kiểm chứng
                                                  chứng minh

  Deep Learning Method    Không phải đóng góp của Không phát triển hay
                          dự án                   huấn luyện phương pháp
                                                  học sâu mới
  -----------------------------------------------------------------------

### 1. Neuro-Symbolic AI

Neuro-Symbolic AI là hướng nghiên cứu kết hợp năng lực học từ dữ liệu
của mô hình thần kinh với biểu diễn tri thức và suy luận ký hiệu.

Trong dự án:

-   SymPy giải toán.
-   LLM nhận dữ liệu kết quả rồi diễn đạt bằng ngôn ngữ tự nhiên.

Việc hai thành phần xuất hiện trong cùng phần mềm chưa đủ chứng minh có
kiến trúc Neuro-Symbolic.

Cách viết phù hợp:

-   *An LLM-assisted symbolic mathematics software system.*
-   *A hybrid CAS--LLM architecture for mathematical problem-solving
    assistance.*

### 2. Formal Verification

Không nên dùng thuật ngữ này cho `geometry_validator.py`.

Kiểm tra thiếu đỉnh, diện tích tam giác và khoảng cách là kiểm tra điều
kiện đầu vào và chất lượng hiển thị. Chúng không đồng nghĩa với xác minh
hình thức một chứng minh toán học.

Tương tự, thay nghiệm vào phương trình gốc là cách xác nhận nghiệm ứng
viên, nhưng không tự động chứng minh hệ thống đã tìm đủ tất cả nghiệm.

Cách viết phù hợp:

-   Mathematical Constraint Validation.
-   Symbolic Solution Verification.
-   Geometric Input Validation.
-   Solution Consistency Checking.

### 3. Deep Learning

Có thể nói phần mềm sử dụng dịch vụ LLM được xây dựng trên mô hình học
sâu, nếu đúng với dịch vụ thực tế.

Nhưng không nên tuyên bố dự án phát triển phương pháp Deep Learning.

-   *The system integrates a pretrained LLM API for natural-language
    explanation.* --- phù hợp.
-   *The system proposes a novel deep learning model for mathematical
    reasoning.* --- không được dữ liệu dự án hỗ trợ.

**Khuyến nghị:** Không thêm thuật ngữ công nghệ cao chỉ để làm bài báo
có vẻ hiện đại. Dùng đúng thuật ngữ và có kết quả thực nghiệm rõ ràng sẽ
thuyết phục hơn.

## VI. Nên công bố ở đâu?

Nên chia thành ba cấp độ, dựa trên mức độ hoàn thiện thực tế.

### 1. Hội nghị quốc tế

**IEEE TALE -- Teaching, Assessment and Learning for Engineering**

-   Phù hợp có điều kiện.
-   Có phạm vi giáo dục STEM, công nghệ giáo dục và ứng dụng AI trong
    dạy học.
-   Cần bổ sung đánh giá sử dụng phần mềm trong dạy và học, thay vì chỉ
    mô tả lập trình.
-   TALE 2026 diễn ra ngày 2--4/12/2026 tại Pattaya; hạn nhận bài đã
    qua.

**ICCE -- International Conference on Computers in Education**

-   Rất đáng cân nhắc.
-   Phân hội C1 -- Artificial Intelligence in Education / Intelligent
    Tutoring Systems có phạm vi gần với hệ thống hỗ trợ học tập thông
    minh, LLM trong giáo dục và đánh giá hệ thống AI giáo dục.
-   ICCE 2026 diễn ra 30/11--4/12/2026; hạn nộp bài chính 31/5/2026 đã
    qua.
-   Việc gửi kỷ yếu để xem xét lập chỉ mục không phải cam kết mọi bài
    được lập chỉ mục.

**ICETOE -- International Conference on Educational Technology and
Online Education**

-   Là hướng trong nước đáng xem xét.
-   Phù hợp với công nghệ giáo dục, học tập số và ứng dụng công nghệ
    trong dạy học.
-   Cần phân biệt kỷ yếu hội nghị và cơ hội được xem xét cho số chuyên
    đề tạp chí; hai hình thức có quy trình phản biện riêng.
-   Hạn nộp bài toàn văn năm 2026 là 22/8/2026, đã qua.

Lưu ý: Các mốc trên là thông tin của mùa hội nghị 2026, không phải lịch
cho mùa tiếp theo. Cần kiểm tra thông báo chính thức của từng kỳ mới.

### 2. Hội thảo khoa học trong nước

Các nhóm hội thảo phù hợp:

-   Ứng dụng CNTT trong giáo dục.
-   Công nghệ giáo dục và chuyển đổi số.
-   Phương pháp giảng dạy Toán có ứng dụng phần mềm.
-   Hệ thống hỗ trợ học tập thông minh.

Đây là hướng có thể tập trung vào một đóng góp kỹ thuật cụ thể, chưa
nhất thiết phải chứng minh tác động giáo dục quy mô lớn.

Cần kiểm tra quy trình phản biện, đơn vị xuất bản, phạm vi đánh giá khoa
học và tính hợp lệ của kỷ yếu.

### 3. Đồ án tốt nghiệp, báo cáo sáng tạo và sản phẩm nghiên cứu ứng dụng

Ở trạng thái hiện tại, đây là cấp độ phù hợp nhất.

Một phần mềm do cá nhân phát triển, có kiến trúc rõ ràng, chức năng hoạt
động thực tế, bộ kiểm thử và tài liệu kỹ thuật có thể là đồ án hoặc sản
phẩm sáng tạo tốt.

Có thể phát triển tiếp thành bài báo thực nghiệm thay vì chỉ dừng ở
trình diễn phần mềm.

## VII. Định hướng viết bài báo được đề xuất

Không khuyến nghị tiêu đề:

> A Novel Neuro-Symbolic AI System for Automated Mathematical Theorem
> Proving Using Deep Learning and Formal Verification.

Tiêu đề này không phù hợp với thực trạng và tạo ra kỳ vọng mà hệ thống
chưa đáp ứng.

### Tiêu đề đề xuất

**Design and Evaluation of a CAS-Assisted Desktop Tool for High-School
Algebra and 2D Geometry Validation**

*Thiết kế và đánh giá công cụ máy tính để bàn hỗ trợ giải đại số bằng
CAS và kiểm tra hình học phẳng 2D.*

Định vị: Applied Mathematics Software + Educational Technology.

### 1. Bốn đóng góp chính

  -----------------------------------------------------------------------
  Đóng góp                            Nội dung cần chứng minh
  ----------------------------------- -----------------------------------
  C1 -- System Architecture           Kiến trúc tích hợp bộ giải ký hiệu,
                                      xử lý điều kiện và sinh lời giải

  C2 -- Mathematical Validation       Quy trình kiểm soát điều kiện, lọc
                                      và xác nhận nghiệm ứng viên

  C3 -- Geometry Validation           Cơ chế kiểm tra đầu vào hình học,
                                      phát hiện suy biến và hỗ trợ chất
                                      lượng dựng hình

  C4 -- Experimental Evaluation       Đánh giá có hệ thống trên bộ dữ
                                      liệu tự sinh và bài toán thực tế
  -----------------------------------------------------------------------

AI viết lời giải nên được mô tả là một lớp hỗ trợ riêng. Chỉ xem nó là
đóng góp đáng kể khi đánh giá được độ chính xác toán học, tính nhất quán
và tỷ lệ nội dung AI tự ý thêm hoặc làm sai.

### 2. Thiết kế bộ thực nghiệm

**Thử nghiệm A -- Đại số**

So sánh SymPy nguyên bản với pipeline của hệ thống trên:

-   Phương trình vô tỉ.
-   Hệ phương trình.
-   Trường hợp có nghiệm ngoại lai.
-   Trường hợp không có nghiệm thực.
-   Trường hợp có nhiều nghiệm và điều kiện xác định phức tạp.

Báo cáo độ chính xác tập nghiệm, nghiệm sai bị chấp nhận, nghiệm đúng bị
bỏ sót, tỷ lệ giải thành công và thời gian xử lý.

**Thử nghiệm B -- Hình học**

Tạo các tình huống có kiểm soát:

-   Đủ và thiếu đỉnh.
-   Tam giác không suy biến.
-   Ba điểm thẳng hàng.
-   Ba điểm gần thẳng hàng.
-   Hai nhãn gần nhau.
-   Các mức zoom và kích thước màn hình khác nhau.

Đối chiếu cảnh báo của hệ thống với kết quả xác minh độc lập.

**Thử nghiệm C -- Chất lượng lời giải AI**

Đánh giá hai phương diện riêng biệt:

-   Độ chính xác toán học.
-   Độ rõ ràng, logic và phù hợp với trình độ học sinh.

Không mặc định rằng lời giải viết hay đồng nghĩa với lời giải đúng.

### 3. Cấu trúc bài báo

  -----------------------------------------------------------------------
  Phần                                Nội dung
  ----------------------------------- -----------------------------------
  1\. Introduction                    Vấn đề và nhu cầu phần mềm hỗ trợ
                                      toán học

  2\. Related Work                    SymPy, phần mềm toán học, công cụ
                                      học tập và giải toán

  3\. System Architecture             Kiến trúc tổng thể và các module

  4\. Mathematical Processing         Cơ chế xử lý đại số và kiểm tra
                                      nghiệm

  5\. Geometry Validation             Cơ chế kiểm tra và trực quan hóa
                                      hình học

  6\. Experimental Design             Bộ dữ liệu, phương pháp và tiêu chí
                                      đánh giá

  7\. Results and Discussion          Kết quả, đối chứng, hạn chế

  8\. Conclusion                      Đóng góp, phạm vi ứng dụng và hướng
                                      phát triển
  -----------------------------------------------------------------------

## VIII. Đánh giá tổng thể theo góc nhìn Reviewer

Bảng nhận định định tính dựa trên thông tin hiện có, không phải điểm số
chấm bài chính thức.

  Tiêu chí                      Đánh giá hiện tại
  ----------------------------- ------------------------------------
  Tính thực tiễn                Tốt
  Khả năng ứng dụng             Tốt
  Tính hoàn thiện kỹ thuật      Có nền tảng
  Thuật toán mới                Chưa có
  Đóng góp AI mới               Chưa có
  Thiết kế thực nghiệm          Chưa đủ
  Khả năng tái lập nghiên cứu   Chưa chứng minh
  Giá trị giáo dục              Có tiềm năng, chưa được kiểm chứng

### Ba việc cần làm trước tiên

**Thứ nhất: Chứng minh tính đúng đắn của hệ thống.**

Sửa mô tả tập điều kiện xác định, xây dựng các trường hợp kiểm thử có
đáp án chuẩn và thống kê sai số thực tế.

**Thứ hai: Chứng minh giá trị của kiến trúc tích hợp.**

Không chỉ chứng minh hệ thống chạy được, mà cần chứng minh từng thành
phần bổ sung giá trị gì so với việc sử dụng SymPy trực tiếp.

**Thứ ba: Có đánh giá thực tế về người sử dụng.**

Nếu định hướng là phần mềm hỗ trợ học sinh phổ thông, cần có ý kiến của
giáo viên hoặc học sinh. Nếu không, chỉ nên kết luận về độ tin cậy kỹ
thuật, không kết luận rằng phần mềm nâng cao năng lực toán học.

## IX. Kết luận cuối cùng

Không phải cứ phát minh ra thuật toán mới mới có thể công bố bài báo
khoa học.

Trong nghiên cứu khoa học máy tính, có những đóng góp đáng giá nằm ở
thiết kế hệ thống, phương pháp tích hợp, quy trình kiểm soát độ tin cậy,
bộ dữ liệu đánh giá và kết quả thực nghiệm.

Dự án có cơ sở để phát triển theo hướng này. Nhưng ở thời điểm hiện tại,
chưa có cơ sở để tuyên bố:

-   Phát triển thuật toán giải toán mới.
-   Đề xuất phương pháp Neuro-Symbolic mới.
-   Xác minh hình thức chứng minh toán học.
-   Phát triển mô hình Deep Learning giải toán.
-   Chứng minh phần mềm nâng cao kết quả học tập.

Cách định vị trung thực hơn:

> This work presents an applied desktop mathematics software system that
> integrates symbolic computation, mathematical constraint validation,
> geometric input validation, and LLM-assisted solution explanation. Its
> effectiveness is investigated through a reproducible test corpus
> covering algebraic problems and planar geometry scenarios.

Đây là phát biểu có thể bảo vệ được nếu tác giả hoàn thiện các thử
nghiệm đã nêu.

**Lời khuyên cuối cùng:** Với tư cách một người phát triển độc lập, bạn
không cần cố chứng minh mình là nhà nghiên cứu AI hay nhà toán học lý
thuyết. Hãy chứng minh rằng bạn đã nhận diện một vấn đề kỹ thuật thực
sự, xây dựng được giải pháp và có số liệu độc lập cho thấy giải pháp
hoạt động đáng tin cậy.

Đó là con đường khả thi và thuyết phục hơn nhiều so với việc cố gắn cho
phần mềm những nhãn công nghệ cao chưa thực sự có.
