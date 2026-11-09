# HỆ SINH THÁI STEM APP - TÀI LIỆU NGỮ CẢNH DỰ ÁN & LỘ TRÌNH PHÁT TRIỂN
**Cập nhật lần cuối:** 06/11/2026 (Hoàn tất GeoSolver 2D v3.4: Bổ sung Elip, Thang cân, Bình hành, Thoi, Vuông & Tái cấu trúc Toolbar Hàng 3)  
**Vị trí dự án:** `D:\AI DATA\STEM_APP`  
**Mục tiêu dài hạn:** Xây dựng bộ công cụ chuyển đổi số giáo dục STEM chuẩn mực sư phạm, đưa vào giảng dạy tại các trường THPT và Đại học Sư phạm, xuất bản độc lập từng phân hệ lên Microsoft Store.

---

## 1. TỔNG QUAN KIẾN TRÚC TOÀN HỆ THỐNG (SYSTEM OVERVIEW)

Hệ thống được thiết kế theo mô hình **Core - Multi-App (Một Lõi Dùng Chung - Đa Ứng Dụng Độc Lập)**:

```
D:\AI DATA\STEM_APP\
├── stem_shared_core/           # LÕI CÔNG NGHỆ CHUNG (Shared Engine)
│   ├── ai_model_hub.py         # AI Engine: DeepSeek-R1 (Local GGUF/Ollama) & Gemini API (Fallback)
│   ├── hf_downloader.py        # One-Click HuggingFace Downloader (Modal UI Dialog, Stream Progress)
│   ├── algebra_kernel.py       # Lõi Đại số & Giải tích: Khử nghiệm ngoại lai, lọc tiệm cận Canvas
│   ├── physics/                # Lõi Vật lý: Dao động, Sóng, Mạch RLC, Phân tích thứ nguyên
│   ├── chemistry/              # Lõi Hóa học: Cân bằng phản ứng Matrix Nullspace, Nồng độ, Redox
│   ├── biology/                # Lõi Sinh học: Di truyền Men-đen, Cân bằng Hacđi-Vanbec
│   ├── i18n/                   # Hệ thống Đa ngữ tập trung (vi.json, en.json, math_terms.json)
│   ├── curricula/              # Thư viện đề thi chuẩn SGK GDPT 2018 (Lớp 10, 11, 12) & Quốc tế
│   └── master_benchmark_runner.py # TRÌNH KIỂM ĐỊNH TỰ ĐỘNG ĐA MÔN (Đạt 100% PASS)
│
├── cad_math_v2/                # [APP 1] CAD Math Studio v2.1 (Đại số, Khảo sát hàm, Đồ thị Oxy)
├── geosolver/                  # [APP 2] GeoSolver Studio v3.3 (Hình học phẳng 2D, Suy luận tự động, Responsive Ribbon, Shoelace/Heron, Deductive Engine)
├── geosolver_3d/               # [APP 3 - TRỌNG TÂM] GeoSolver 3D (Hình học không gian THPT & Oxyz)
├── phys_solver/                # [APP 4] PhysLab Studio v1.0 (Thí nghiệm ảo & Mạch RLC - ĐÃ HOÀN TẤT GUI)
├── chem_solver/                # [APP 5] ChemLab Studio v1.0 (Cân bằng ma trận & Nồng độ - ĐÃ HOÀN TẤT GUI)
└── bio_solver/                 # [APP 6] BioLab Studio v1.0 (Bàn cờ Punnett & Hacđi-Vanbec - ĐÃ HOÀN TẤT GUI)
```

---

## 2. KẾT QUẢ KIỂM ĐỊNH SƯ PHẠM TOÀN DIỆN (100% PERFECT BENCHMARK)

Ngày 05/11/2026, trình `master_benchmark_runner.py` đã thực thi kiểm định toàn diện trên môi trường Python 3.14:
- **Độ chính xác Toán học**: **20/20 bài toán SGK GDPT 2018 (100.00%)**
  - Lớp 10 (Phương trình vô tỉ & trị tuyệt đối): 5/5 bài PASS
  - Lớp 11 (Phương trình lượng giác, hệ phương trình cấp số, đa thức): 5/5 bài PASS
  - Lớp 12 (Khảo sát sự biến thiên, cực trị hàm số, chứa tham số m): 10/10 bài PASS
- **Tỷ lệ khử nghiệm ngoại lai**: **9/9 bài toán | 10/10 nghiệm ngoại lai bị loại bỏ triệt để (100.00%)**
- **Kiểm định 3 Lõi Khoa học (Lý - Hóa - Sinh)**: **6/6 test PASS (100.00%)**
  - Dao động điều hòa, mạch RLC xoay chiều
  - Cân bằng phản ứng hóa học ma trận hạt nhân, nồng độ mol dung dịch
  - Phép lai Men-đen phân ly độc lập, cân bằng di truyền quần thể Hacđi-Vanbec
- **Tổng thời gian thực thi toàn bộ 26 bài test**: **2055 ms (~2 giây)**
- **Báo cáo chi tiết**: Đã xuất bản tại `D:\AI DATA\STEM_APP\stem_shared_core\MASTER_PEDAGOGICAL_REPORT.md`

---

## 3. HIỆN TRẠNG 3 ỨNG DỤNG MỚI (PHYSICS, CHEMISTRY, BIOLOGY)

Cả 3 ứng dụng Desktop đã được xây dựng hoàn chỉnh giao diện Tkinter theo phong cách **MS Office 2003 / Technical CAD**:
1. `phys_solver/app.py`: Toolbar icon trên caption dưới (`⚡\nDao động`, `🔌\nMạch RLC`), Canvas vẽ sóng x(t), tính Z, I, P, cos(phi), nút One-Click AI `🤖\nTải AI`.
2. `chem_solver/app.py`: Toolbar (`⚗️\nCân bằng`, `🧪\nNồng độ`), bảng bảo toàn nguyên tố 2 vế, tính nồng độ CM, C%.
3. `bio_solver/app.py`: Toolbar (`🧬\nMen-đen`, `📊\nHacđi-Vanbec`), Canvas vẽ Bàn cờ Punnett lưới giao tử màu sắc nhã nhặn, bảng phân tích tần số alen p, q.

---

## 4. NHIỆM VỤ CHIẾN LƯỢC TIẾP THEO: GEOSOLVER 3D (HÌNH HỌC KHÔNG GIAN)

> **Mục tiêu:** Xây dựng phần mềm giải toán và trực quan hóa **Hình học không gian (Solid Geometry)** chuẩn chương trình SGK Lớp 11, 12 và Đại học Sư phạm.

### 4.1. Kiến Trúc Phân Hệ GeoSolver 3D (`geosolver_3d/`)
- `geometry3d_kernel.py`:
  - Biểu diễn Điểm 3D `(x, y, z)`, Vector 3D, Mặt phẳng `Ax + By + Cz + D = 0`, Đoạn thẳng/Đường thẳng.
  - Các phép toán giải tích không gian: Tích có hướng, tích vô hướng, khoảng cách điểm đến mặt, khoảng cách 2 đường chéo nhau, góc giữa 2 mặt phẳng.
  - Thuật toán dựng hình khối cơ bản:
    - Hình chóp tam giác (tứ diện), chóp tứ giác, chóp có $SA \perp (ABC)$, chóp đều $S.ABCD$.
    - Lăng trụ tam giác, lăng trụ đứng, hình hộp chữ nhật, hình lập phương.
    - Mặt cầu, hình nón, hình trụ.
  - Thuật toán tìm **Thiết diện (Cross-section)** cắt bởi mặt phẳng $(\alpha)$.
- `projection_engine.py`:
  - Phép chiếu phối cảnh (Perspective) và trục đo (Isometric) từ 3D sang 2D Canvas Tkinter.
  - Tự do xoay hình trong không gian (3D Orbit Rotation) bằng kéo chuột trái.
  - Thuật toán xác định mặt khuất: Tự động chuyển các cạnh bị che khuất thành **nét đứt (`dash=(4, 4)`)** chuẩn SGK Toán Việt Nam.
- `app.py`:
  - Giao diện Tkinter MS Office 2003 / CAD Studio với Canvas 3D tương tác.

---

## 5. LỘ TRÌNH THỰC HIỆN TIẾP THEO (MILESTONES)

- [x] **Giai đoạn 1**: Chuẩn hóa `stem_shared_core`, i18n, Hugging Face Downloader, lõi 4 môn.
- [x] **Giai đoạn 2**: `master_benchmark_runner.py` đạt **100% PASS**; hoàn thiện GUI Tkinter cho PhysLab, ChemLab, BioLab.
- [x] **Giai đoạn 3 (HOÀN TẤT TOÀN DIỆN GEOSOLVER 3D v1.0 CHUẨN SƯ PHẠM SGK GDPT 2018 & QUỐC TẾ)**:
  - Viết geosolver_3d/geometry3d_kernel.py (Lõi toán học giải tích 3D, mặt cầu, thiết diện, đa diện, định lý Girard).
  - Viết geosolver_3d/deductive3d_engine.py (Engine suy luận diễn dịch sư phạm song ngữ VN & EN, 8/8 unit tests 100% PASS, bổ sung tính khoảng cách điểm đến mặt phẳng, góc đường-mặt, góc 2 mặt phẳng).
  - Viết geosolver_3d/app.py (~136 KB):
    + 100% Giao diện Cổ điển Win32 CAD / MS Office 2003 (#ECE9D8, ribbon 2 hàng, nút [ AI ] đơn sắc, bảng chọn màu Win32 swatch, hoàn toàn KHÔNG có emoji màu mè).
    + Chuyển đổi công thức LaTeX thành Ký hiệu toán học tự nhiên (Natural Math: √, phân số, π, ⊥, ∥, ∠, Δ, ², ³, ≈).
    + Nét đứt SGK cho khối đa diện và nét đứt chuẩn cho thiết diện khi cắt qua các mặt khuất.
    + Khử răng cưa / nét gãy khi kéo thả (Smooth Dragging with subpixel float math & round joins/caps).
    + Bộ chỉnh kích thước cạnh & tỉ lệ thời gian thực (Dimension Editor h, a, b trên Side Panel).
    + Hộp thoại Dựng hình 3D (Construction3DDialog) 3 Tab: Trung điểm M, Đường song song PQ // AB, Hình chiếu PK ⊥ AB, Chân đường cao PH ⊥ (ABC), Đoạn vuông góc chung Δ1/Δ2, Tâm & Đường tròn ngoại tiếp, Tâm & Đường tròn nội tiếp đáy (vẽ đường tròn 3D trên Canvas).
    + Hộp thoại Suy luận 3D (Deductive3DDialog) với 12 chuyên đề chuẩn SGK + SAT/AP/Gaokao, trang bị nút [ Lấy số đo từ Canvas 3D ] để tự động nạp kích thước thực tế từ Canvas vào bài toán.
    + Phím tắt thu gọn Ribbon (▲ / ▼) và Xuất ảnh Canvas độ phân giải cao PNG in ấn.
- [x] **Giai đoạn 3.5 (HOÀN THIỆN ĐA DẠNG HÌNH HỌC & AI AGENT GEOSOLVER 2D v3.5)**:
  - Bổ sung trọn vẹn: Hình Elip (3 điểm chuẩn, diện tích chính xác, chu vi Ramanujan, vẽ smooth 72 điểm), Hình thang cân (thuật toán phản chiếu trung trực), Hình bình hành, Hình thoi, Hình vuông.
  - Tự động nhận diện Đề bài từ Thanh công cụ (Goal Type, Targets, Presets) đồng bộ lên giao diện.
  - Cơ chế Ghi Nối Tiếp Lời Giải (Append Mode) cho phép so sánh trực tiếp Python vs AI mà không mất dữ liệu.
  - AI Agent Tự Động Vẽ Hình Phụ Trực Tiếp Trên Canvas (Đường nét đứt màu đỏ, trung điểm, đường cao, đường tròn).
  - Quản lý trạng thái nút bấm và luồng chạy, chặn triệt để 100% ký tự chữ Hán rò rỉ từ LLM.
  - Bổ sung trọn vẹn: Hình Elip (3 điểm chuẩn, diện tích chính xác, chu vi Ramanujan, vẽ smooth 72 điểm), Hình thang cân (thuật toán phản chiếu trung trực), Hình bình hành, Hình thoi, Hình vuông.
  - Tái quy hoạch Toolbar Hàng 3 thành 4 cụm logic rõ ràng (Đa giác & Conic, Đường tròn & Tiếp tuyến, Tâm tam giác đặc biệt, Đo đạc & Màu sắc).
  - Khắc phục lỗi hiển thị Ribbon Toolbar, chuẩn hóa nút thu gọn ▲/▼ và loại bỏ toàn bộ từ ngữ vi phạm bản quyền.
  - Tích hợp `stem_shared_core/ai_local_manager.py` (26/26 unit tests PASS): Định tuyến 100% về ổ D (`D:\AI DATA\STEM_APP\models`), quản lý RAM qua ctypes/psutil, giải phóng keep_alive=0, điều phối 4 profiles (Python, Gemini, DeepSeek-R1 7B, DeepSeek-R1 1.5B).
- [x] **Giai đoạn 3.6 (HOÀN TẤT BẢN ĐẶC TẢ TỔNG THỂ & PROMPT THI CÔNG PHÒNG THÍ NGHIỆM VẬT LÍ SỐ)**:
  - Xuất bản tài liệu `PHYSICS_VIRTUAL_LAB_MASTER_BLUEPRINT.md` tổng hợp toàn diện bài học, bẫy kỹ thuật từ 2D, 3D, CAD, Math.
  - Khảo sát ma trận khung chương trình Vật lí THCS, THPT GDPT 2018 và mở rộng Vật lí Đại cương Đại học (KHTN 6-9, Vật lí 10, 11, 12, Đại cương A1/A2).
  - Hoàn thiện tệp mã nguồn lõi toàn năng `stem_shared_core/physics/physics_engine_ultimate.py` (Vector3D, RK4, Quỹ đạo hạt Lorentz 3D, Giao thoa sóng Hypebol & Sóng dừng, Mạng điện Kirchhoff ma trận DC & AC RLC phức, Ném xiên Parabol, Tán sắc lăng kính Cauchy & Ánh xạ bước sóng sang màu RGB thực tế, Thấu kính mỏng, Mẫu Bohr quang phổ Hydro & Cân bằng phản ứng hạt nhân).
  - Đạt 10/10 bài kiểm thử tự động (100% PASS) kiểm định trực tiếp trên môi trường Python 3.14.
- [x] **Giai đoạn 3.7 (TÍCH HỢP TOÀN DIỆN CƠ CHẾ AI CO-PILOT CHO PHÒNG THÍ NGHIỆM VẬT LÍ SỐ - PHYSLAB STUDIO v2.0)**:
  - Kế thừa trọn vẹn kiến trúc AI Neuro-Symbolic từ GeoSolver 2D v3.5 sang `phys_solver/app.py`.
- [x] **Giai đoạn 4 (HOÀN THÀNH TOÀN DIỆN CHUYÊN ĐỀ TOÁN CAO CẤP ĐẠI HỌC - HIGHER MATH STUDIO v1.0 & TÍCH HỢP CAD MATH v2.2)**:
  - Hoàn thiện `stem_shared_core/higher_math_kernel.py`: Bao trọn 6 chuyên đề Đại học (Đại số tuyến tính, Giải tích 1, Chuỗi số & Fourier, Giải tích đa biến, Lý thuyết trường & Tích phân mặt, Phương trình vi phân & Laplace).
  - Hoàn thiện `stem_shared_core/higher_math_benchmark.py`: Bộ kiểm định tự động 20/20 bài toán mẫu chuẩn giáo trình ĐHBK Hà Nội, ĐHQG, Sư Phạm và GRE Mathematics (100% PASS trong 1.27s).
  - Hoàn thiện `stem_shared_core/higher_math_dialog.py`: Hộp thoại Win32 CAD Studio tối ưu không gian nhập liệu, tích hợp Quick Symbol Palette và ví dụ mẫu chuẩn 1 chạm.
  - Tích hợp Menu Chuyên Đề phân cấp và nút One-Click `[ 🏛️ Toán Cao Cấp ]` trên thanh công cụ của `cad_math_v2/cad_math_v2.py`.
  - Xuất bản báo cáo kiểm định sư phạm sẵn sàng bàn giao cho Claude thẩm định tại `stem_shared_core/HIGHER_MATH_PEDAGOGICAL_BENCHMARK_REPORT.md` và nhật ký `HIGHER_MATH_INTEGRATION_LOG.md`.
  - Tích hợp 4 Profile AI chuẩn: 0. Thuần Python CAS (Ground Truth 100%), 1. Gemini Cloud (0 MB RAM), 2. DeepSeek-R1 7B (Ollama), 3. DeepSeek-R1 1.5B (Ollama / GGUF).
  - Bổ sung thanh công cụ AI trên Right HUD: combobox chọn profile, nút `[ 🤖 AI Phân Tích & Giảng Giải ]`, nút `[ ⏹ Dừng AI ]`, nút `[ 📋 Copy ]`, nút `[ ↺ Phục hồi ]`.
  - Bổ sung nút truy cập nhanh `[ 🤖 Cấu hình AI Hub ]` trên Top Title Bar và `[ 🤖 AI Giảng Giải ]` trên Bottom Toolbar.
  - Hộp thoại Minh bạch Tài nguyên & Cấu hình AI (Resource Transparency Control Panel): GGUF weights (`D:\AI DATA\STEM_APP\models\gguf`), Ollama Engine status (`127.0.0.1:11434`), Gemini API Key, RAM Monitor qua `ctypes` GlobalMemoryStatusEx, Test Inference stream trực tiếp.
  - Cơ chế Ghi Nối Tiếp Lời Giải (Append Mode): Giữ nguyên ground truth giải tích của Python, nối tiếp phân tích sư phạm sâu sắc của AI.
  - Bẫy ngắt vòng lặp token, chống rò rỉ ký tự lạ/chữ Hán, luồng nền daemon không đơ giao diện Tkinter.
  - Xuất bản file khởi chạy tiện lợi: `run_phys_solver.bat` tại thư mục gốc và `phys_solver/run.bat`.
  - Bộ kiểm thử tự động `phys_solver/test_ai_features.py` đạt 4/4 test (100% PASS).
- [x] **Giai đoạn 3.8 (TÍCH HỢP TOÀN DIỆN CƠ CHẾ AI CO-PILOT CHO CAD MATH STUDIO v2.1)**:
  - Nâng cấp trọn vẹn cơ chế AI Neuro-Symbolic cho `cad_math_v2/cad_math_v2.py`.
  - Tích hợp 4 Profile AI chuẩn: 0. Thuần Python CAS (SymPy 100% Ground Truth), 1. Gemini Cloud (0 MB RAM), 2. DeepSeek-R1 7B (Ollama), 3. DeepSeek-R1 1.5B (Ollama / GGUF).
  - Bổ sung Thanh công cụ AI Co-Pilot Toolbar trực quan nằm giữa Header và 6 Tab: Combobox chọn Profile, nút `[ 🤖 AI Giảng Giải & Phân Tích Sư Phạm (F5) ]`, nút `[ ⏹ Dừng AI ]`, `[ 📋 Copy Lời giải ]`, `[ ↺ Phục hồi CAS Gốc ]`.
  - Nút truy cập nhanh `[ 🤖 Cấu hình AI Hub ]` trên Header và trong Menu Tools (phím tắt F5).
  - Hộp thoại Minh bạch Tài nguyên & Cấu hình AI (Resource Transparency Control Panel): GGUF weights (`D:\AI DATA\STEM_APP\models\gguf`), Ollama Engine status, Gemini API Key, RAM Monitor qua `ctypes` GlobalMemoryStatusEx, Test Box live streaming.
  - Khả năng trích xuất thông tin bài toán và kết quả giải tích tự động trên cả 6 Tab (Phương trình/BPT, Cực trị VDC tham số m, Vi tích phân, Đại số tuyến tính, Thống kê, Khảo sát hàm Oxy).
  - Xuất bản file khởi chạy nhanh `run_cad_math.bat` tại thư mục gốc và `cad_math_v2/run.bat`.
  - Bộ kiểm thử tự động `cad_math_v2/test_ai_features.py` đạt 4/4 test (100% PASS), bộ kiểm thử chất lượng 20/20 test (100% PASS).
- [x] **Giai đoạn 3.9 (TỐI ƯU HÓA GIAO DIỆN & KHẮC PHỤC LỖI HIỂN THỊ GEOSOLVER 3D)**:
  - Thống nhất tên gọi phần mềm duy nhất: `GeoSolver 3D` trên toàn bộ cửa sổ và tài liệu.
  - Khắc phục lỗi thứ tự hiển thị lớp (Z-Order Layering): Chuyển các mảng đa giác tô màu mờ và gạch chéo xuống lớp đáy trước khi vẽ các cạnh khuất nét đứt và cạnh thấy nét liền, đảm bảo đường nét đứt luôn hiển thị rõ ràng trên nền diện tích đã tô màu.
  - Bổ sung công cụ kẻ gạch chéo và tô màu diện tích: Đổi nhãn nút trên thanh công cụ thành `[ ▨ Tô màu & Gạch chéo CAD ]`, thêm nút truy cập nhanh ở thanh bên trái, mở rộng hộp thoại hỗ trợ chọn nhanh các mặt khối đa diện và hỗ trợ đa giác 3 hoặc 4 đỉnh.
  - Bảo vệ phím tắt `H` tránh kích hoạt ngoài ý muốn khi gõ văn bản; trực quan hóa trạng thái nút bấm nét khuất.
  - Tạo bộ khởi chạy nhanh `run_geosolver_3d.bat` tại thư mục gốc và biểu tượng lối tắt (Desktop Shortcut) `GeoSolver 3D.lnk`.
  - Bộ kiểm thử tự động `geosolver_3d/test_all_features.py` hoàn thành 10/10 test.
- [ ] **Giai đoạn 4**: Đóng gói MSIX độc lập cho cả 6 phần mềm và đưa lên Microsoft Store.


---

## 6. QUY ƯỚC & NGUYÊN TẮC XUẤT PROMPT CHO ARGON (ONE-SHOT FILE GENERATION)

> **NGUYÊN TẮC BẮT BUỘC:** Bất cứ khi nào người dùng yêu cầu xuất prompt (để bàn giao cho **Argon** hoặc các công cụ AI sinh mã), Agent **PHẢI** xuất ra bản đặc tả prompt hoàn chỉnh 100% (Fully Self-Contained), chi tiết và đầy đủ để Argon có thể tạo ra file mã nguồn hoàn chỉnh ngay trong một lần thực thi duy nhất (One-Shot), tuyệt đối không để người dùng phải tự chắp vá hoặc yêu cầu sửa đổi nhiều lần.

### 6.1. Năm Yếu Tố Bắt Buộc Trong Prompt Xuất Ra:
1. **Toàn Bộ Mã Nguồn Đầy Đủ (Zero Truncation / No Ellipsis):**
   - Không được dùng các đoạn tóm tắt như `# ... giữ nguyên code cũ ...`, `// TODO: implement remaining logic`.
   - Viết trọn vẹn toàn bộ các lệnh `import`, định nghĩa hằng số, cấu trúc lớp (Class), phương thức xử lý sự kiện và khối thực thi chính `if __name__ == '__main__':`.
2. **Đặc Tả Kỹ Thuật & Cấu Trúc Dữ Liệu Rõ Ràng (Strict Data Schema):**
   - Nêu rõ cấu trúc từ điển/đối tượng (Point, Segment, Circle, Polygon, Matrix...), các trường định danh (`id`, `name`, `x`, `y`, `z`).
   - Quy định chặt chẽ về hệ tọa độ (Oxy/Oxyz), phép chiếu hình học và giới hạn tham số.
3. **Cơ Chế Bắt Lỗi & Xử Lý Tình Huống Biên (Robust Edge-Case Handling):**
   - Xử lý các phép toán nhạy cảm: Chia cho 0, căn bậc hai số âm, điểm trùng nhau, ma trận suy biến.
   - Hiển thị thông báo sư phạm thân thiện bằng cả Tiếng Việt và Tiếng Anh thay vì làm sập ứng dụng (Zero Unhandled Crashes).
4. **Bộ Kiểm Thử Đi Kèm (Self-Verification Tests):**
   - Trong prompt luôn bao gồm mã kiểm thử đơn vị (`pytest` hoặc hàm test độc lập) với các giá trị mẫu cụ thể để Argon có thể tự chạy kiểm định ngay sau khi tạo file.
5. **Hướng Dẫn Môi Trường Thực Thi (Runtime & Dependencies):**
   - Chỉ rõ phiên bản Python (3.10+ / 3.14), danh sách package cần cài (`requirements.txt` hoặc lệnh `pip install`) và lệnh chạy file.
