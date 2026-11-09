# BỘ CHÙM PROMPT CHI TIẾT ĐỂ MỞ RỘNG NGÂN HÀNG BÀI TOÁN KHOA HỌC (PROMPT SUITE)

Dưới đây là bộ các Prompt chuyên biệt được thiết kế để bạn copy vào **Google AI Studio (Model: Gemini 1.5 Pro / 2.5 Pro)**. Bạn chỉ cần chọn chuyên đề bạn muốn và copy prompt tương ứng.

---

### PROMPT 1: CHUYÊN ĐỀ HÌNH HỌC PHẲNG OLYMPIC (VMO / IMO / USAMO)
```markdown
Bạn là Chuyên gia Hình học Phẳng của Đội tuyển Olympic Toán Quốc tế (IMO / VMO).

Nhiệm vụ: Hãy biên soạn 10 bài toán Hình học Phẳng kinh điển đặc trưng của các kỳ thi VMO và IMO (tứ giác nội tiếp, trục đẳng phương, tâm bàng tiếp, đường tròn Mixtilinear, điểm Miquel, đường thẳng Simson).

YÊU CẦU:
Với mỗi bài toán, xuất ra đúng định dạng JSON sau:
[
  {
    "problem_id": "IMO-GEO-00X",
    "prompt": {
      "vi": "Đề bài bằng Tiếng Việt (dùng LaTeX $...$)",
      "en": "English problem statement"
    },
    "ground_truth": "Đáp số đại số hoặc tính chất cần chứng minh",
    "construction": {
      "required_nodes": ["A", "B", "C", "D", "H", "O"],
      "points": {
        "A": [0, 0], "B": [4, 0], "C": [1, 3]
      },
      "elements": [
        {"type": "triangle", "vertices": ["A", "B", "C"]},
        {"type": "circle", "name": "circumcircle"}
      ]
    },
    "pedagogical_rubric": {
      "core_steps": [
        "Bước 1: Viện dẫn định lý và góc nội tiếp.",
        "Bước 2: Chứng minh tứ giác nội tiếp."
      ],
      "exclusion_conditions": [
        "Các trường hợp suy biến điểm hoặc đường kính vuông góc cần loại trừ."
      ]
    }
  }
]
```

---

### PROMPT 2: CHUYÊN ĐỀ HÌNH HỌC GIẢI TÍCH CAO KHẢO TRUNG QUỐC (GAOKAO OXY CONICS)
```markdown
Bạn là Chuyên gia Biên soạn Đề thi Tuyển sinh Đại học Trung Quốc (Cao Khảo - Gaokao Mathematics).

Nhiệm vụ: Biên soạn 10 bài toán Hình học Giải tích Oxy cực khó đặc trưng của đề thi Cao Khảo (phần Conic: Elip, Parabol, Hyperbol, dây cung đi qua tiêu điểm, cực trị diện tích tam giác).

YÊU CẦU:
Xuất ra khối code JSON chuẩn gồm:
- `problem_id`: GAOKAO-CONIC-00X
- `prompt`: Đề bài chi tiết chứa phương trình Conic.
- `ground_truth`: Giá trị lớn nhất / nhỏ nhất chính xác.
- `construction`: Tọa độ tiêu điểm, đỉnh, phương trình đường chuẩn.
- `pedagogical_rubric`: Các bước đặt phương trình tham số đường thẳng $x = my + c$ và hệ thức Viète.
```

---

### PROMPT 3: CHUYÊN ĐỀ ĐẠI SỐ & HỆ PHƯƠNG TRÌNH KHÓ (AIME / SAT ADVANCED / HSG QUỐC GIA)
```markdown
Bạn là Chuyên gia Khảo thí Đại số của Kỳ thi AIME (American Invitational Mathematics Examination) và VMO.

Nhiệm vụ: Biên soạn 10 bài toán Đại số đặc sắc (Hệ phương trình đối xứng, Bất đẳng thức chứa tham số, Đa thức nghiệm nguyên, Phương trình vô tỉ có nghiệm ngoại lai phức tạp).

YÊU CẦU:
Xuất ra khối code JSON chuẩn gồm:
- `problem_id`: AIME-ALG-00X
- `prompt`: Hệ phương trình hoặc phương trình tham số.
- `ground_truth`: Số nghiệm thực hoặc khoảng giá trị tham số $m$.
- `pedagogical_rubric`:
  + `core_steps`: Phân tích nhân tử, đặt ẩn phụ đối xứng, khảo sát hàm đặc trưng.
  + `exclusion_conditions`: Chỉ rõ điều kiện xác định và nghiệm ngoại lai cần loại bỏ.
```
