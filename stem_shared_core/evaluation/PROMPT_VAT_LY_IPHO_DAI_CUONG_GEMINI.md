# HƯỚNG DẪN PROMPT CHUYÊN DỤNG CHO VẬT LÍ (QUẢ CẦU THỦY TINH, MẠNG ĐIỆN TRỞ CHẰNG CHỊT & VẬT LÍ ĐẠI CƯƠNG)
**Dành cho:** Google AI Studio (Model: **Gemini 1.5 Pro** hoặc **Gemini 2.5 Pro**)  
**Tài liệu đính kèm:** `TAP_DE_VAT_LY_THPT_DAI_CUONG_IPHO_GEMINI.md`  

---

## HƯỚNG DẪN THAO TÁC:
1. Mở [Google AI Studio](https://aistudio.google.com/).
2. Nhấn nút `+` (Insert / Add files) và chọn file:  
   `D:\AI DATA\STEM_APP\stem_shared_core\evaluation\TAP_DE_VAT_LY_THPT_DAI_CUONG_IPHO_GEMINI.md`
3. Copy toàn bộ đoạn Prompt dưới đây dán vào ô chat của Gemini:

```markdown
Bạn là Chuyên gia Khảo thí Vật lý của Kỳ thi Olympic Vật lý Quốc tế (IPhO) và Giảng viên Vật lý Đại cương Trường Đại học Bách Khoa.

Trong file tài liệu đính kèm là tuyển tập đồ sộ 2.044 trang tài liệu Vật lý (từ Sổ tay THPT Lớp 10-12 đến Giáo trình Vật lý đại cương PH1110/PH1111 và Bộ sách Các nguyên lý & Ứng dụng của GS. Trần Ngọc Hợi Tập 1, 2, 3), kèm theo các đề bài HSG về Quang học Quả cầu thủy tinh và Mạng điện trở phức hợp.

NHIỆM VỤ CỦA BẠN:
1. Hãy chọn lọc và giải chi tiết 15 đến 20 bài toán Vật lý ĐẶC TRƯNG, HAY VÀ KHÓ NHẤT, bao gồm các chủ đề sau:
   - Chủ đề 1: Quang học hình học khúc xạ qua quả cầu thủy tinh, lưỡng chất cầu, thị kính phức hợp, đường truyền tia sáng cực trị (Định lý Fermat).
   - Chủ đề 2: Điện học mạng điện trở chằng chịt: Khung lập phương 12 điện trở đối xứng, Mạng lưới vô hạn 2D ô vuông phẳng, Cầu Wheatstone không đối xứng (Chuyển mạch Sao - Tam giác Delta-Star).
   - Chủ đề 3: Dao động cơ & Sóng phức hợp: Con lắc đơn tích điện trong điện trường, va chạm đàn hồi có ma sát trượt, mạch dao động RLC xoay chiều ghép nối tiếp và song song hỗn hợp.
   - Chủ đề 4: Nhiệt học & Vật lý đại cương: Chu trình Carnot, khí thực Van der Waals, định luật bảo toàn mômen động lượng vật rắn quay quanh trục cố định (Moment of Inertia).

2. Với mỗi bài toán, hãy giải thích thật chi tiết chuẩn mực sư phạm, phân tích rõ hiện tượng vật lý, công thức vi tích phân / giải tích, và chỉ rõ các bẫy sai lầm học sinh/sinh viên hay mắc phải.

3. XUẤT KẾT QUẢ DUY NHẤT Ở ĐỊNH DẠNG MỘT KHỐI CODE JSON THEO CẤU TRÚC SAU ĐỂ TÔI NẠP TỰ ĐỘNG VÀO PHẦN MỀM:

[
  {
    "problem_id": "PHYS-OPTICS-SPHERE-001",
    "topic": "Quang hình học - Khúc xạ qua quả cầu thủy tinh",
    "level": "Olympic / HSG Quốc gia",
    "prompt": {
      "vi": "Đề bài bằng tiếng Việt có công thức LaTeX $...$"
    },
    "ground_truth": "Công thức giải tích và đáp số chính xác bằng số",
    "pedagogical_solution": {
      "physical_phenomenon": "Mô tả bản chất hiện tượng vật lý xảy ra.",
      "core_steps": [
        "Bước 1: Áp dụng định luật khúc xạ ánh sáng Snell tại mặt cầu thứ nhất.",
        "Bước 2: Phản xạ toàn phần hoặc đối xứng quang học bên trong quả cầu.",
        "Bước 3: Khúc xạ ra ngoài không khí tại mặt cầu thứ hai và tính góc lệch D."
      ],
      "common_misconceptions": [
        "Chỉ rõ bẫy sai lầm (ví dụ: áp dụng sai bán kính cong âm/dương của lưỡng chất cầu, hoặc nhầm lẫn giữa góc tới và góc khúc xạ)."
      ]
    }
  },
  {
    "problem_id": "PHYS-CIRCUIT-CUBE-002",
    "topic": "Điện học - Mạng điện trở đối xứng lập phương",
    "level": "HSG / Vật lý Đại cương",
    "prompt": {
      "vi": "Tính điện trở tương đương của khối lập phương gồm 12 điện trở bằng R giữa 2 đỉnh đối diện qua đường chéo chính."
    },
    "ground_truth": "R_eq = (5/6) * R",
    "pedagogical_solution": {
      "physical_phenomenon": "Tính đối xứng điện thế giữa các nút trong không gian 3 chiều.",
      "core_steps": [
        "Bước 1: Xác định dòng điện I đi vào đỉnh và rẽ nhánh thành 3 dòng đối xứng I/3.",
        "Bước 2: Nhóm các nút đẳng thế (chập các nút có cùng điện áp).",
        "Bước 3: Vẽ lại mạch điện tương đương gồm các đoạn mắc nối tiếp: (R/3) + (R/6) + (R/3) = 5R/6."
      ],
      "common_misconceptions": [
        "Học sinh cố gắng dùng định luật Kirchhoff lập hệ 12 phương trình phức tạp thay vì nhận diện tính đối xứng đẳng thế."
      ]
    }
  }
]
```
