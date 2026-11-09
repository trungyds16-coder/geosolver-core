# TỔNG QUAN DANH MỤC TÀI NGUYÊN ĐÃ KHỞI TẠO & GOM GỌN (SYSTEM INDEX)
**Ngày cập nhật:** 06/11/2026  
**Vị trí gốc:** `D:\AI DATA\STEM_APP\stem_shared_core`  

Tất cả các file được tạo trong các phiên làm việc (sáng và chiều) đã được tổ chức logic, chuẩn hóa vào các thư mục chức năng, không có file nào bị thất lạc.

---

## 1. THƯ MỤC KIỂM ĐỊNH HÌNH HỌC & BẢO CHỨNG AN TOÀN (`stem_shared_core/validation/`)
- `geometry_validator.py`: Lõi kiểm tra an toàn dựng hình Fail-Fast (Bắt lỗi thiếu nút, kiểm tra va chạm nhãn < 15px, phát hiện tam giác suy biến).
- `__init__.py`: Package export cho validator.

---

## 2. THƯ MỤC THẨM ĐỊNH SƯ PHẠM & BÀI BÁO KHOA HỌC (`stem_shared_core/evaluation/`)
- `pedagogical_judge.py`: Bộ tiêu chuẩn Rubric thang điểm 10 (Chính xác toán, Tính liên tục, Văn phong, Nghiệm ngoại lai).
- `PROMPT_HUONG_DAN_GEMINI.md`: Hướng dẫn prompt copy vào Gemini để chấm điểm lời giải.
- `PROMPTS_EXPANSION_SUITE.md`: Chùm prompt chuyên đề Olympic (VMO/IMO), Cao khảo (Gaokao) và Đại số khó (AIME).
- `TAP_DE_THI_UPLOAD_GEMINI.md`: File tổng hợp ban đầu gồm Hình học 2D và Đại số GDPT 2018.
- `TAP_DE_DAI_SO_VN_OLYMPIC_GEMINI.md`: File tổng hợp mới nhất trích xuất từ 8 file PDF (VMO 2021, BĐT Nguyễn Văn Mậu...).
- `GEMINI_PEDAGOGICAL_REVIEW.json`: Mẫu review chuẩn JSON từ AI.
- `gemini-code-1793928104035.json`: File dữ liệu 4 bài toán đặc trưng mẫu bạn vừa tải lên.
- `MASTER_1000_SCIENTIFIC_REPORT.md`: Báo cáo kết quả thực nghiệm khoa học 1000 bài toán (Đạt 100% Pass).
- `paper_artifacts/`:
  - `PAPER_OUTLINE_RESEARCH.md`: Đề cương chi tiết bài báo khoa học chuẩn IMRAD quốc tế.
  - `screenshots/FIGURE_1_BEFORE_AFTER_COMPARISON.png`: Ảnh so sánh trực quan minh chứng Before/After độ nét cao 300 DPI.
  - `screenshots/EXPERIMENTAL_LOG.jsonl`: Nhật ký lưu trữ bằng chứng khoa học qua từng phiên bản.

---

## 3. THƯ MỤC NGÂN HÀNG ĐỀ THI QUỐC TẾ (`stem_shared_core/curricula/`)
- `MASTER_SYNTHETIC_1000_BENCHMARK.json`: Kho 1.000 bài toán tham số hóa thực nghiệm (400 Gaokao Conic, 300 AIME, 300 VMO).
- `cn_gaokao/benchmark_cn_gaokao_curated.json`: Chuyên đề Cao khảo Trung Quốc.
- `olympic_vmo_imo/benchmark_olympic_vmo_imo_curated.json`: Chuyên đề Olympic VMO và IMO.
- `us_k12/benchmark_us_k12_curated.json`: Chuyên đề Toán Mỹ (AIME, AMC).
- `vn_gdpt2018/grade_10_geometry/sample_geo2d_bench.json`: Chuyên đề Hình học 2D Oxy Việt Nam.

---

## 4. BỘ CÔNG CỤ TỰ ĐỘNG HÓA (`stem_shared_core/tools/`)
- `system_self_check.py`: Trình khám sức khỏe tự động 1 lệnh cho toàn bộ hệ sinh thái.
- `run_master_1000_benchmark.py`: Trình chạy kiểm thử toàn diện trên 1.000 bài toán.
- `auto_snapshot_generator.py`: Tự động sinh ảnh minh chứng bài báo Before/After.
- `pdf_curriculum_extractor.py`: Trích xuất PDF từ `D:\AI DATA\đại số` thành Markdown.
- `distribute_benchmarks.py`: Tự động phân phối bài toán vào đúng thư mục chuyên đề.
- `procedural_benchmark_generator.py`: Trình sinh đề biến thiên tham số.
- `import_gemini_review_to_code.py`: Tự động đồng bộ đánh giá của Gemini vào code.
- `run_bench_and_validate.py`: Trình chạy thử nghiệm kiểm tra lỗi thiếu nút.
