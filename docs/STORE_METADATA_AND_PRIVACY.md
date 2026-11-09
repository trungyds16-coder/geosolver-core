# CHÍNH SÁCH QUYỀN RIÊNG TƯ & ĐẶC TẢ MICROSOFT STORE
## HỆ THỐNG PHẦN MỀM GEOSOLVER 2D
*Văn bản công bố chính thức phục vụ hồ sơ nộp và thẩm định trên Microsoft Store.*  
**Mã tài liệu:** STORE-PRIVACY-AGED-DECLARATION-2026  
**Ngày cập nhật:** 09/11/2026  
**Đơn vị phát triển / Xuất bản:** TLabtool Studio  
**Địa chỉ công bố trực tuyến:** https://tlabtool.com/geosolver/privacy  
**Email liên hệ hỗ trợ & Quyền riêng tư:** privacy@tlabtool.com / support@tlabtool.com  

---

## 1. CHÍNH SÁCH QUYỀN RIÊNG TƯ (PRIVACY POLICY)

### 1.1. Nguyên tắc cốt lõi: Bảo vệ Dữ liệu Cục bộ (Local-First Privacy)
Hệ thống **GeoSolver 2D** được thiết kế theo nguyên tắc Local-first: *Dữ liệu bản vẽ và bài toán của người dùng hoàn toàn thuộc quyền sở hữu của người dùng*. Ứng dụng không thu thập, không phân tích hành vi và không gửi telemetry về máy chủ của nhà phát triển.

### 1.2. Thu thập và Xử lý Dữ liệu Ngoại tuyến
* **Không thu thập Telemetry / Quảng cáo:** Ứng dụng không chứa bất kỳ SDK theo dõi hành vi, Google Analytics, Firebase Telemetry, hay mã theo dõi quảng cáo nào.
* **Xử lý Hình học CAD & CAS Ngoại tuyến:** Toàn bộ các thao tác dựng hình học phẳng (điểm, đoạn thẳng, tam giác, đường tròn, elip...), phát hiện bất biến hình học, đo đạc kích thước và tính toán đại số tượng trưng (SymPy) được xử lý hoàn toàn ngoại tuyến trên máy tính cục bộ của người dùng.
* **Mô hình AI Cục bộ (Local LLM - Tùy chọn):** Khi người dùng kích hoạt suy luận ngoại tuyến qua Ollama hoặc tệp mô hình GGUF cục bộ, toàn bộ dữ liệu suy luận được xử lý trực tiếp trên GPU/RAM cục bộ, không truyền dữ liệu ra Internet.

### 1.3. Khai báo các luồng truyền dữ liệu qua Mạng (Network Data Flows)
Ứng dụng chỉ phát sinh kết nối mạng ra bên ngoài trong 2 tình huống người dùng chủ động kích hoạt:
1. **Dịch vụ AI Đám mây (Google Gemini API - Tùy chọn):**
   - Khi người dùng chủ động cấu hình khóa API Gemini và yêu cầu giải toán qua AI đám mây, nội dung câu hỏi hình học được gửi trực tiếp tới endpoint chính thức của Google (`generativelanguage.googleapis.com`) qua giao thức mã hóa HTTPS/TLS 1.3.
   - Khóa API cá nhân của người dùng được lưu trữ cục bộ trên máy tính bằng cơ chế mã hóa cấp hệ điều hành Windows Data Protection API (DPAPI - `CryptProtectData`).
   - Việc xử lý dữ liệu của Google Gemini tuân thủ theo các điều khoản dịch vụ chính thức của Google: [Google AI Studio Terms of Service](https://ai.google.dev/terms) và [Google Privacy Policy](https://policies.google.com/privacy).
2. **Tải Mô hình Ngoại tuyến (Hugging Face Model Hub - Tùy chọn):**
   - Khi người dùng chủ động tải các tệp trọng số mô hình AI nguồn mở (.gguf) về máy, ứng dụng tải trực tiếp qua HTTPS từ máy chủ chính thức `huggingface.co`. Quá trình tải kiểm tra mã băm SHA-256 để bảo đảm tính toàn vẹn tệp tin.

### 1.4. Thời hạn lưu trữ dữ liệu (Data Retention)
* **Tệp dự án & hình học (.geo):** Do người dùng toàn quyền quyết định vị trí lưu trữ trên ổ đĩa. Ứng dụng không tự động xóa hay thay đổi file khi chưa có thao tác của người dùng.
* **Khóa API và cấu hình người dùng:** Được lưu trữ cục bộ dưới dạng DPAPI blob tại `%LOCALAPPDATA%\geosolver` (hoặc thư mục dữ liệu cục bộ của gói MSIX). Dữ liệu này tồn tại cho đến khi người dùng chọn "Xóa khóa API" trong giao diện Cấu hình AI hoặc gỡ cài đặt ứng dụng.

### 1.5. Chính sách bảo vệ trẻ em và học sinh dưới 18 tuổi (COPPA / GDPR-K / Nghị định 13/2023/NĐ-CP)
* GeoSolver 2D là phần mềm hỗ trợ học tập bộ môn Toán & STEM phục vụ học sinh THCS, THPT và sinh viên.
* Ứng dụng **không thu thập bất kỳ thông tin nhận dạng cá nhân nào (PII)** của trẻ em hay học sinh (không yêu cầu họ tên, ngày sinh, trường lớp, số điện thoại, email đăng ký tài khoản).
* Không có tính năng mạng xã hội, chat công cộng hay chia sẻ vị trí, hoàn toàn an toàn và tuân thủ các quy định bảo vệ trẻ em trên môi trường mạng.

### 1.6. Hành vi khi gỡ cài đặt (Uninstall Behavior & GGUF Storage)
* **Gói MSIX:** Khi người dùng gỡ cài đặt ứng dụng qua Windows Settings / Apps, toàn bộ dữ liệu ứng dụng cô lập trong `%LOCALAPPDATA%\Packages\TLabtool.GeoSolverCAD_...\` sẽ được Windows tự động thu hồi và xóa sạch.
* **Tệp mô hình GGUF tải thêm:** Nếu người dùng tải các tệp mô hình GGUF kích thước lớn (~1.1 GB đến 4 GB), người dùng có thể xóa trực tiếp qua nút "Dọn dẹp mô hình" trong hộp thoại *Cấu hình AI* hoặc xóa thủ công thư mục mô hình hiển thị trong hộp thoại để giải phóng toàn bộ dung lượng ổ đĩa.

---

## 2. BẢNG KHAI BÁO KHẢO SÁT ĐỘ TUỔI IARC (IARC AGE RATING QUESTIONNAIRE)

Bảng kê khai thông tin phục vụ khảo sát IARC (International Age Rating Coalition) trên Microsoft Partner Center:

| Tiêu chí khảo sát IARC | Khai báo thực tế của GeoSolver 2D | Đánh giá nội bộ |
| :--- | :---: | :---: |
| **Bạo lực (Violence)** | Không | Không chứa bất kỳ hình ảnh/yếu tố bạo lực |
| **Nội dung nhạy cảm / Tình dục** | Không | Không |
| **Ngôn ngữ thô tục (Profanity)** | Không | Thuần túy thuật ngữ toán học STEM |
| **Chất kích thích / Rượu bia** | Không | Không |
| **Giao dịch trả phí trong app (IAP)** | Không | Không chứa mua hàng trong ứng dụng |
| **Chia sẻ vị trí địa lý (Location)** | Không | Không sử dụng định vị GPS/IP |
| **Tương tác trực tuyến giữa người dùng** | Không | Không có tính năng chat mạng xã hội |

*Dự kiến phân loại IARC:* **IARC 3+ (Mọi lứa tuổi / All Ages)** — Phân loại chính thức sẽ do hệ thống Partner Center cấp sau khi hoàn thành bảng câu hỏi trực tuyến khi nộp gói.

---

## 3. GIẢI TRÌNH CAPABILITY VÀ TUÂN THỦ WACK

1. **Giải trình Restricted Capability `runFullTrust`:**
   - *Lý do kỹ thuật:* GeoSolver 2D là ứng dụng Win32 truyền thống được đóng gói để phân phối qua Microsoft Store thông qua công nghệ chuyển đổi **Desktop Bridge (Centennial)**.
   - Do bản chất là ứng dụng để bàn hoàn chỉnh (thực thi Python runtime độc lập, gọi DPAPI hệ thống, tải mô hình AI cục bộ), cơ chế Desktop Bridge bắt buộc phải khai báo capability `runFullTrust` trong `AppxManifest.xml` để khởi chạy tiến trình chính.
2. **Tuân thủ quy chuẩn WACK (Windows App Certification Kit):**
   - Tắt nén UPX (`upx=False`) trong cấu hình PyInstaller để tránh cảnh báo nhận diện nhầm từ Windows Defender và SmartScreen.
   - Hỗ trợ đầy đủ cơ chế VFS Virtualization của Desktop Bridge: thư mục ứng dụng trong `WindowsApps` là Read-Only, các thao tác ghi dữ liệu nhật ký và khóa DPAPI được lưu trữ an toàn trong `%LOCALAPPDATA%` (được Windows tự động chuyển hướng về thư mục dữ liệu cô lập của gói).
   - Mã lệnh kiểm thử WACK chuẩn cho gói MSIX:  
     `appcert.exe test -appxpackagepath <Đường_dẫn_tệp_MSIX> -reportoutputpath <Đường_dẫn_báo_cáo_XML>`
