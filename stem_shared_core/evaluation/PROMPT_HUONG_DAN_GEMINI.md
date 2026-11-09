# HƯỚNG DẪN PROMPT THẨM ĐỊNH SƯ PHẠM VỚI GEMINI (GOOGLE AI STUDIO)

Tài liệu này chứa Prompt chuẩn mực được thiết kế riêng cho việc thẩm định chất lượng sư phạm của các phần mềm Toán học STEM.

---

## 1. FILE CẦN YÊU CẦU GEMINI XUẤT RA: `JSON` (Khuyên dùng nhất) hoặc `MARKDOWN`

Khi Gemini chấm xong, bạn hãy yêu cầu Gemini xuất ra định dạng **JSON** thuần túy (hoặc một khối code block JSON). 
- **Lý do**: File JSON có cấu trúc chuẩn, máy tính có thể đọc tự động (automated parser) và nạp thẳng lời giải mẫu mực vào mã nguồn của `GeoSolver` / `CAD Math Studio` mà bạn không cần phải copy tay từng câu.
- Tên file lưu khuyến nghị: `GEMINI_PEDAGOGICAL_REVIEW.json` (Lưu vào thư mục `stem_shared_core/evaluation/`).

---

## 2. PROMPT CHI TIẾT ĐỂ COPY VÀO GEMINI (DÙNG TRÊN GOOGLE AI STUDIO / GEMINI WEB)

> **Hướng dẫn thao tác**:
> 1. Kéo thả file `TAP_DE_THI_UPLOAD_GEMINI.md` vào khung chat.
> 2. Copy toàn bộ đoạn Prompt dưới đây dán vào và nhấn **Enter**.

```markdown
Bạn là Chuyên gia Khảo thí và Hội đồng Biên soạn Sách giáo khoa Toán THPT theo chương trình GDPT 2018 của Bộ Giáo dục & Đào tạo Việt Nam.

Nhiệm vụ của bạn là thẩm định toàn bộ các bài toán và lời giải trong file đính kèm với tư cách một Giáo viên chấm thi nghiêm khắc.

HÃY ĐÁNH GIÁ TỪNG BÀI TOÁN THEO 4 TIÊU CHÍ (THANG ĐIỂM 10):
1. Tính chính xác toán học (0 - 3 điểm): Không sai số học, áp dụng đúng định lý/tiên đề.
2. Tính liên tục & Không nhảy bước (0 - 3 điểm): Có viện dẫn căn cứ cho từng bước suy luận, không giải tắt/nhảy cóc khiến học sinh khó hiểu.
3. Văn phong sư phạm SGK Việt Nam (0 - 2 điểm): Câu chữ dẫn dắt gãy gọn, tự nhiên, mang tính sư phạm chuẩn mực.
4. Xử lý điều kiện & Nghiệm ngoại lai (0 - 2 điểm): Xét tập xác định đầy đủ, thử lại nghiêm túc và loại nghiệm triệt để.

---
YÊU CẦU XUẤT KẾT QUẢ:
Sau khi chấm xong, hãy xuất toàn bộ kết quả vào DUY NHẤT MỘT KHỐI CODE JSON theo đúng cấu trúc sau (không kèm lời giải thích ngoài code block để tôi tải về dùng script nạp vào phần mềm):

```json
{
  "dataset_evaluation_report": {
    "total_problems": 7,
    "evaluator_role": "Hội đồng Thẩm định Sách giáo khoa GDPT 2018",
    "overall_comment": "Nhận xét tổng quan về chất lượng giải của phần mềm"
  },
  "evaluations": [
    {
      "problem_id": "GEO2D-G10-001",
      "math_score": 3.0,
      "logic_continuity_score": 2.5,
      "pedagogical_tone_score": 1.5,
      "constraint_score": 2.0,
      "total_score": 9.0,
      "passed_pedagogical_standard": true,
      "detected_flaws": [
        "Chỉ rõ bước nào giải tắt, cộc lốc hoặc thiếu câu viện dẫn định lý"
      ],
      "improved_pedagogical_solution": "Viết lại lời giải hoàn chỉnh, mẫu mực chuẩn sách giáo khoa (dùng LaTeX $...$ cho công thức) để học sinh đọc là hiểu ngay."
    }
  ]
}
```
```

---

## 3. CÁCH SỬ DỤNG KẾT QUẢ SAU KHI GEMINI CHẤM XONG

1. Trên màn hình Gemini, ở góc trên bên phải của khung code JSON, bạn bấm nút **Copy code** (hoặc nút **Download** nếu có).
2. Mở Notepad hoặc trình soạn thảo, dán nội dung vào và lưu lại với tên:
   `D:\AI DATA\STEM_APP\stem_shared_core\evaluation\GEMINI_PEDAGOGICAL_REVIEW.json`
3. Chạy script đồng bộ tự động của hệ thống:
   ```powershell
   python stem_shared_core/tools/import_gemini_review_to_code.py
   ```
4. Script này sẽ tự động phân tích kết quả, lọc ra các bài nào bị Gemini chấm điểm thấp (dưới 8đ), và tự động trích xuất phần `improved_pedagogical_solution` để bạn làm template mẫu cho engine sinh lời giải!
