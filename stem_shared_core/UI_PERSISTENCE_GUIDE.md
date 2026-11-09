# HƯỚNG DẪN & NHẬT KÝ LƯU TRỮ TRẠNG THÁI GIAO DIỆN HỆ THỐNG STEM APPS
**STEM Shared UI Persistence & Geometry/Tab Memory System**
*Ngày phát hành: Tháng 11/2026*

---

## 1. Mục Tiêu & Yêu Cầu Thiết Kế
1. **Giữ nguyên Tab khi thao tác**: Khi người dùng dựng hình (dựng điểm tỉ lệ, chân đường cao, tia góc, đoạn vuông góc chung,...), sau khi hiển thị thông báo kết quả thì **không đóng hộp thoại** (`self.destroy()`). Cửa sổ và tab hiện tại được giữ nguyên để người dùng tiếp tục dựng thêm các đường phụ mới mà không phải mở lại.
2. **Tự động cập nhật danh sách chọn**: Các điểm hoặc đối tượng phụ vừa được sinh ra phải lập tức xuất hiện trong tất cả các hộp thả xuống (OptionMenu / Combobox) trên tất cả các tab mà không cần đóng mở lại ứng dụng.
3. **Ghi nhớ kích thước & vị trí cửa sổ (Geometry Memory)**: Người dùng đã kéo giãn cửa sổ đến kích thước nào hoặc di chuyển đến vị trí nào trên màn hình thì lần sau mở lên phải giữ đúng nguyên trạng thái đó (`width x height + x + y`).
4. **Ghi nhớ Tab đang kích hoạt (Tab Memory)**: Nếu người dùng đang làm việc ở Tab 2 (Mặt phẳng & Khoảng cách) hoặc Chuyên đề 5 (Hình cầu nội tiếp), lần mở tiếp theo phải tự động chuyển ngay về Tab/Chuyên đề đó.
5. **Chống tràn màn hình (Off-Screen Clamping)**: Tự động phát hiện độ phân giải màn hình, không bao giờ để cửa sổ bị tràn ra ngoài cạnh hoặc mất hút khi người dùng đổi độ phân giải màn hình hoặc ngắt kết nối màn hình phụ.

---

## 2. Kiến Trúc `UIStateManager` (`stem_shared_core/tools/ui_state_manager.py`)

Module dùng chung cung cấp các phương thức tĩnh:
- `UIStateManager.restore_window(window, window_key, default_geometry, min_width, min_height)`: Phục hồi kích thước & vị trí an toàn.
- `UIStateManager.attach_window_tracking(window, window_key, get_extra_state_fn, on_close_callback)`: Tự động bắt sự kiện `WM_DELETE_WINDOW` để lưu lại kích thước và các trường mở rộng (tab, ngôn ngữ, chuyên đề,...).
- `UIStateManager.get_active_tab(window_key, default)` & `save_active_tab(window_key, tab_id)`: Quản lý tab đang mở.
- `UIStateManager.get_state(window_key)` & `save_state(window_key, **kwargs)`: Đọc/ghi thuộc tính tùy biến ra file JSON cấu hình.

---

## 3. Mẫu Tích Hợp 3 Bước Cho Các App Khác (`bio_solver`, `chem_solver`, `phys_solver`)

### Bước 1: Import module
```python
try:
    from stem_shared_core.tools.ui_state_manager import UIStateManager
    _UI_STATE_AVAILABLE = True
except Exception:
    _UI_STATE_AVAILABLE = False
    UIStateManager = None
```

### Bước 2: Tích hợp vào cửa sổ chính (`tk.Tk`)
```python
class MyStemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(1024, 700)
        
        # Khôi phục kích thước và tùy chọn đã lưu
        if _UI_STATE_AVAILABLE and UIStateManager:
            UIStateManager.restore_window(self, "MyStemApp", default_geometry="1200x800", min_width=1024, min_height=700)
            saved_state = UIStateManager.get_state("MyStemApp")
            # Phục hồi ngôn ngữ hoặc các thiết lập khác nếu có
            if "lang" in saved_state:
                self.current_lang = saved_state["lang"]
        else:
            self.geometry("1200x800")
            
        # ... Khởi tạo các widget và thanh công cụ ...
        
        # Gắn theo dõi tự động lưu khi đóng app
        if _UI_STATE_AVAILABLE and UIStateManager:
            UIStateManager.attach_window_tracking(
                self,
                "MyStemApp",
                get_extra_state_fn=lambda: {"lang": getattr(self, "current_lang", "vi")},
                on_close_callback=self.destroy,
            )
```

### Bước 3: Tích hợp vào hộp thoại (`tk.Toplevel`) có nhiều Tab
```python
class MyToolDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.minsize(600, 450)
        self.transient(parent)
        
        # 1. Khôi phục kích thước và tab trước đó
        if _UI_STATE_AVAILABLE and UIStateManager:
            UIStateManager.restore_window(self, "MyToolDialog", default_geometry="700x550", min_width=600, min_height=450)
            saved_tab = int(UIStateManager.get_active_tab("MyToolDialog", default=1))
        else:
            self.geometry("700x550")
            saved_tab = 1
            
        self._build_ui()
        self._switch_tab(saved_tab)  # Mở đúng tab người dùng đã chọn
        
        # 2. Gắn theo dõi khi người dùng đóng hộp thoại
        if _UI_STATE_AVAILABLE and UIStateManager:
            UIStateManager.attach_window_tracking(
                self,
                "MyToolDialog",
                get_extra_state_fn=lambda: {"active_tab": self.active_tab_idx},
            )

    def _switch_tab(self, idx: int) -> None:
        self.active_tab_idx = idx
        # Hiển thị frame tương ứng ...
        if _UI_STATE_AVAILABLE and UIStateManager:
            UIStateManager.save_active_tab("MyToolDialog", idx)

    def _on_action_complete(self) -> None:
        # Thực hiện tác vụ ...
        # LÀM MỚI DANH SÁCH DỮ LIỆU
        self._refresh_all_dropdowns()
        messagebox.showinfo("Thành công", "Đã thực hiện xong!")
        # KHÔNG GỌI self.destroy() ĐỂ NGƯỜI DÙNG TIẾP TỤC DỰNG TIẾP
```

---

## 4. Nhật Ký Triển Khai Hiện Tại
* **`geosolver_3d`**:
  - `GeoSolver3DApp`: Lưu & phục hồi kích thước, vị trí, ngôn ngữ (VN/EN), trạng thái thanh Ribbon.
  - `Construction3DDialog`: Lưu & phục hồi kích thước, vị trí, tab đang chọn (Tab 1, Tab 2, Tab 3). Sau khi dựng điểm, hạ đường cao, kẻ song song, đo góc... **giữ nguyên hộp thoại và tab**, tự động cập nhật điểm mới vào toàn bộ dropdown.
  - `Deductive3DDialog`: Lưu & phục hồi kích thước, vị trí và chuyên đề đang chọn (1 trong 12 chuyên đề suy luận).
  - `Win32AIHubDialog`: Lưu & phục hồi kích thước, vị trí cửa sổ AI Hub.
* **`geosolver` (2D)**:
  - `GeoSolverApp`: Đã tích hợp `UIStateManager` lưu & phục hồi kích thước và vị trí kéo thả của cửa sổ làm việc 2D.
* **Các app tiếp theo (`bio_solver`, `chem_solver`, `phys_solver`)**:
  - Sẵn sàng tích hợp theo mẫu chuẩn 3 bước ở mục 3 trên.
