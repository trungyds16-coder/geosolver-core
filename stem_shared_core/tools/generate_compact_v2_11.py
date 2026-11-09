import os, sys

def generate_compact():
    full_path = r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\paper_artifacts\BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_11.md"
    compact_path = r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\paper_artifacts\BAN_TOM_TAT_THAM_DINH_v2_11_COMPACT.md"
    
    with open(full_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Find Section 8 and replace the massive python code blocks with concise API signatures
    s8_idx = full_text.find("## 8. MÃ NGUỒN TỰ CHỨA ĐẦY ĐỦ ĐỂ TÁI LẬP ĐỘC LẬP")
    s9_idx = full_text.find("## 9. KẾT LUẬN & ĐỀ XUẤT ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT")

    prefix = full_text[:s8_idx]
    suffix = full_text[s9_idx:]

    compact_s8 = """## 8. CẤU TRÚC MÃ NGUỒN & HƯỚNG DẪN TÁI LẬP ĐỘC LẬP

Nhằm tối ưu hóa độ dài hiển thị trong các giao diện hội thoại (tránh tràn giới hạn token của trình duyệt và mô hình AI), toàn bộ mã nguồn đầy đủ được lưu trữ trong tệp đính kèm `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_11.md` và mã nguồn dự án. Dưới đây là tóm tắt chữ ký API của các thành phần cốt lõi:

### 8.1. Chữ ký API của Giải thuật Lõi (`CADMathCore` - Thuần SymPy, không phụ thuộc GUI):
```python
class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"

class CADMathCore:
    @staticmethod
    def real_status(r) -> bool | None:
        '''Xác định nghiệm r là thực (True), phức (False) hay chưa kết luận (None) dựa trên sp.N(r, 60).'''

    @staticmethod
    def check_sign_exact(expr_sub) -> str:
        '''Xác định dấu đại số chính xác: 'pos', 'neg', 'zero', 'nonreal', 'unknown'.'''

    def solve_radical_pedagogical(self, target_eq, x) -> tuple[list[str], list, list, list]:
        '''Giải sqrt(f(x)) = g(x) qua 4 bước: (steps, valid_sols, rejected_sols, indeterminate_sols).'''

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines) -> tuple[DiophantineCategory, list, int, list[str]]:
        '''Giải hệ Diophantine tuyến tính d=1: (category, int_sols, n_total, out_lines).'''
```

### 8.2. Chữ ký API của Bộ kiểm thử Benchmark (`run_batch_auto_test.py`):
```python
def get_test_cases(x, y, z):
    '''Trả về 19 ca kiểm thử: 7 ca Radical (RAD_01 đến RAD_07) + 12 ca Diophantine (DIO_01 đến DIO_12).'''

def execute_single_run(app, test_cases, is_warmup=False):
    '''Thực thi kiểm tra 4 bất biến: Invariant 1 (residue < 1e-7), Invariant 2 (vi phạm độc lập), 
    Bất biến phân hoạch (Partition), Kiểm tra đủ nghiệm (Curated Completeness).'''

def run_suite():
    '''Chạy 1 vòng warm-up + 5 vòng đo lường (Median & IQR), 
    chạy Oracle Hộp cố định N=3000 trên 100 hệ phân tầng (25/loại), 
    và chạy Kiểm thử đột biến thật trên Bytecode (Mutant 1, Mutant 2, Mutant 3).'''
```
*(Ghi chú: Toàn bộ mã nguồn triển khai chi tiết 100% có sẵn trong tệp `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_11.md` đính kèm).*

---

"""

    compact_doc = prefix + compact_s8 + suffix

    with open(compact_path, "w", encoding="utf-8") as f:
        f.write(compact_doc)

    print(f"Generated compact report: {compact_path} (Size: {len(compact_doc)} bytes)")

if __name__ == "__main__":
    generate_compact()
