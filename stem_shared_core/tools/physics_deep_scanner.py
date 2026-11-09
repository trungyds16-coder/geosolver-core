# -*- coding: utf-8 -*-
"""
physics_deep_scanner.py
=======================
Bộ quét sâu kho tài liệu VẬT LÍ (Lớp 10-12 & Vật lí Đại cương Đại học - PH1110/PH1111/Trần Ngọc Hợi)
tại D:\\AI DATA\\vật lí.

Đồng thời TÍCH HỢP & BỔ SUNG CÁC DẠNG TOÁN HSG / IPhO / VPhO KINH ĐIỂN:
1. Quang học hình học: Khúc xạ qua quả cầu thủy tinh, lưỡng chất cầu, quang sợi, tiêu cự phức hợp.
2. Mạch điện trở mạng lưới vô hạn (Infinite Grid Resistors), mạch lập phương 12 điện trở đối xứng (Cube Resistors), cầu Wheatstone mất cân bằng (Delta-Star).
3. Dao động & Cơ học phi tuyến: Con lắc vướng đinh, dao động trong điện trường, va chạm đàn hồi có ma sát.
4. Nhiệt động lực học & Khí thực: Chu trình Carnot, Van der Waals, biến thiên Entropy.
"""

from __future__ import annotations
import sys
import re
from pathlib import Path
import fitz

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SOURCE_DIR = Path(r"D:\AI DATA\vật lí")
OUTPUT_MD = Path(r"D:\AI DATA\STEM_APP\stem_shared_core\evaluation\TAP_DE_VAT_LY_THPT_DAI_CUONG_IPHO_GEMINI.md")

def clean_text(text: str) -> str:
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    return text.strip()

def scan_physics_vault():
    print(f"⚡ BẮT ĐẦU QUÉT KHO TÀI LIỆU VẬT LÍ: {SOURCE_DIR}")
    pdf_files = list(SOURCE_DIR.glob("*.pdf"))
    print(f"📚 Phát hiện {len(pdf_files)} tài liệu Vật lí (2044 trang giáo trình & bài tập)!\n")

    md_lines = [
        "# ĐẠI TUYỂN TẬP BÀI TOÁN VẬT LÍ THPT, ĐẠI CƯƠNG ĐẠI HỌC & OLYMPIC VPHO / IPHO",
        "Nguồn dữ liệu gốc: `D:\\AI DATA\\vật lí` (Sổ tay 10-12, Vật lí đại cương PH1110/PH1111, Trần Ngọc Hợi Tập 1, 2, 3).",
        "Tích hợp thêm: Các dạng bài toán HSG Quốc gia/Quốc tế: Khúc xạ quả cầu thủy tinh, Mạng điện trở đối xứng, Dao động vi mô.",
        "Dành cho: Chuyên gia Khảo thí Vật lí Gemini (Google AI Studio).",
        "\n" + "=" * 75 + "\n"
    ]

    # --- PHẦN 1: BỔ SUNG CÁC DẠNG TOÁN HSG ĐỈNH CAO THEO YÊU CẦU NGƯỜI DÙNG ---
    md_lines.append("## PHẦN ĐẶC BIỆT: CÁC DẠNG BÀI TOÁN HSG VẬT LÍ KINH ĐIỂN (QUẢ CẦU THỦY TINH & MẠNG ĐIỆN TRỞ CHẰNG CHỊT)\n")
    
    special_hard_cases = """
### [BÀI TOÁN HSG QUANG HÌNH - KHÚC XẠ QUA QUẢ CẦU THỦY TINH]
**Đề bài:** Một chùm tia sáng hẹp song song truyền trong không khí chiếu vuông góc tới một quả cầu thủy tinh đồng chất có bán kính R và chiết suất n = sqrt(3).
1. Hãy xác định góc tới i để tia sáng sau khi khúc xạ vào quả cầu, phản xạ toàn phần một lần ở mặt sau rồi ló ra ngoài song song với tia tới.
2. Tìm vị trí tiêu điểm chính của quả cầu thủy tinh khi chùm tia tới song song và gần trục chính (sử dụng công thức lưỡng chất cầu (n2 - n1)/R = n2/d' - n1/d).

### [BÀI TOÁN HSG ĐIỆN HỌC - MẠNG ĐIỆN TRỞ LẬP PHƯƠNG & LƯỚI VÔ HẠN]
**Đề bài:** 
1. Khung dây hình lập phương được tạo từ 12 điện trở bằng nhau, mỗi điện trở có giá trị R. Tính điện trở tương đương giữa hai đỉnh đối diện nhau qua đường chéo của khối lập phương (sử dụng phương pháp chập các nút có cùng điện thế do tính đối xứng).
2. Một lưới vô hạn các ô vuông phẳng vô tận, mỗi cạnh là một điện trở r. Tính điện trở tương đương giữa hai nút kề nhau trên lưới bằng phương pháp đặt nguồn dòng I và nguyên lý chồng chất điện thế.

### [BÀI TOÁN HSG DAO ĐỘNG & ĐIỆN TỪ - MẠCH RLC PHỨC HỢP & DAO ĐỘNG CƠ ĐIỆN]
**Đề bài:** Một con lắc đơn tích điện q treo trong điện trường đều E biến thiên điều hòa theo phương ngang. Khảo sát phương trình vi phân dao động cưỡng bức và tìm biên độ cộng hưởng khi có lực cản nhớt tỉ lệ với vận tốc.
"""
    md_lines.append(special_hard_cases)
    md_lines.append("\n" + "=" * 75 + "\n")

    # --- PHẦN 2: TRÍCH XUẤT CÁC TÀI LIỆU PDF TRONG THƯ MỤC ---
    total_pages_scanned = 0
    for pdf_path in pdf_files:
        try:
            doc = fitz.open(pdf_path)
            num_pages = len(doc)
            total_pages_scanned += num_pages
            print(f"📖 Đang quét: {pdf_path.name[:45]} ({num_pages} trang)...")

            md_lines.append(f"## TÀI LIỆU: {pdf_path.stem.upper()}")
            md_lines.append(f"- **Tên file:** `{pdf_path.name}` ({num_pages} trang)\n")

            # Lấy 10 trang bài tập tiêu biểu mỗi tài liệu
            scan_limit = min(15, num_pages)
            for p_no in range(scan_limit):
                text = doc[p_no].get_text()
                if len(text.strip()) > 80:
                    md_lines.append(f"### [Trang {p_no + 1}]\n{clean_text(text)}\n")

            md_lines.append("\n" + "-" * 60 + "\n")
            doc.close()

        except Exception as e:
            print(f"   ⚠️ Lỗi khi đọc {pdf_path.name}: {e}")

    # Ghi ra file
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("\n" + "=" * 75)
    print(f"🎉 HOÀN TẤT TỔNG HỢP VẬT LÍ! Tổng số trang duyệt qua: {total_pages_scanned} trang.")
    print(f"💾 File Markdown đã sẵn sàng để tải lên Gemini tại:\n   👉 {OUTPUT_MD}")
    print("=" * 75)

if __name__ == "__main__":
    scan_physics_vault()
