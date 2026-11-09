# PROMPT CHUYÊN DỤNG CHO HÌNH HỌC 2D & 3D (SHARYGIN, IMO SHORTLIST, HÌNH KHÔNG GIAN)
**Dành cho:** Google AI Studio (Model: **Gemini 1.5 Pro** hoặc **Gemini 2.5 Pro**)  
**Tài liệu đính kèm:** `TAP_DE_HINH_HOC_OLYMPIC_2D_3D_GEMINI.md`  

---

## HƯỚNG DẪN THAO TÁC:
1. Mở [Google AI Studio](https://aistudio.google.com/).
2. Bấm nút `+` (Insert / Add files) và chọn file:  
   `D:\AI DATA\STEM_APP\stem_shared_core\evaluation\TAP_DE_HINH_HOC_OLYMPIC_2D_3D_GEMINI.md`
3. Copy toàn bộ nội dung trong khung dưới đây và dán vào ô chat của Gemini:

```markdown
Bạn là Chuyên gia Hình học của Hội đồng Olympic Toán học Quốc tế (IMO) và Chuyên gia Hình học Không gian THPT.

Trong file tài liệu đính kèm là tuyển tập các bộ đề hình học đỉnh cao thế giới:
- Sharygin Geometry Olympiad (Kỳ thi Hình học thuần túy danh giá nhất thế giới).
- IMO Shortlist Geometry (2001 - 2024).
- Tuyển tập Hình học không gian 3D kinh điển (Châu Ngọc Hùng: Góc, Khoảng cách, Thể tích chóp/lăng trụ).
- Vietnam IMO Booklet.

NHIỆM VỤ CỦA BẠN:
1. Chọn ra 15 đến 20 bài toán ĐẶC SẮC NHẤT (gồm cả Hình học phẳng 2D và Hình học không gian 3D).
2. Với mỗi bài toán, hãy giải chi tiết chuẩn mực sư phạm, nêu rõ các bước dựng hình và các điểm mấu chốt để phần mềm CAD tự động vẽ được.
3. Xuất kết quả DUY NHẤT ở định dạng MỘT KHỐI CODE JSON theo mẫu sau (để tôi tải về nạp tự động vào phần mềm):

[
  {
    "problem_id": "GEO-2D-SHARYGIN-001",
    "dimension": "2D",
    "competition": "Sharygin Geometry Olympiad",
    "prompt": {
      "vi": "Đề bài bằng tiếng Việt có công thức LaTeX $...$",
      "en": "English problem statement"
    },
    "ground_truth": "Tính chất hình học cần chứng minh hoặc giá trị góc/khoảng cách chính xác",
    "construction": {
      "required_nodes": ["A", "B", "C", "H", "O", "I"],
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
        "Bước 1: Chứng minh các tứ giác nội tiếp hoặc tam giác đồng dạng liên quan.",
        "Bước 2: Sử dụng góc nội tiếp và trục đẳng phương để suy ra tính chất thẳng hàng/vuông góc."
      ],
      "exclusion_conditions": [
        "Chỉ rõ các trường hợp hình học suy biến (tam giác có góc tù, điểm trùng nhau) cần phòng vệ."
      ]
    }
  },
  {
    "problem_id": "GEO-3D-SPACE-001",
    "dimension": "3D",
    "competition": "Châu Ngọc Hùng - Hình học không gian 3D",
    "prompt": {
      "vi": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại B, SA vuông góc với mặt phẳng đáy (ABC). Cho SA=a, AB=a, BC=a*sqrt(3). Tính khoảng cách từ điểm A đến mặt phẳng (SBC).",
      "en": "Given pyramid S.ABC with base ABC right-angled at B, SA perp (ABC)..."
    },
    "ground_truth": "d(A, (SBC)) = a*sqrt(2)/2",
    "construction": {
      "required_nodes": ["S", "A", "B", "C", "H"],
      "points_3d": {
        "A": [0, 0, 0],
        "B": [1, 0, 0],
        "C": [1, 1.732, 0],
        "S": [0, 0, 1]
      },
      "elements_3d": [
        {"type": "pyramid", "apex": "S", "base": ["A", "B", "C"]},
        {"type": "perpendicular_segment", "from": "A", "to_plane": ["S", "B", "C"], "foot": "H"}
      ]
    },
    "pedagogical_rubric": {
      "core_steps": [
        "Bước 1: Chứng minh BC vuông góc với mặt phẳng (SAB) (do BC vuông góc AB và BC vuông góc SA).",
        "Bước 2: Kẻ AH vuông góc với SB tại H. Suy ra AH vuông góc với mặt phẳng (SBC).",
        "Bước 3: Khoảng cách từ A đến (SBC) chính là độ dài đoạn thẳng AH. Tính AH qua hệ thức lượng trong tam giác vuông SAB."
      ],
      "exclusion_conditions": [
        "Học sinh hay nhầm lẫn khoảng cách từ A đến (SBC) là đoạn AC hoặc AB."
      ]
    }
  }
]
```
