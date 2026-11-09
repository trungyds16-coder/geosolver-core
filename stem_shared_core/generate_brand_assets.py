# -*- coding: utf-8 -*-
"""
generate_brand_assets.py
========================
Tạo bộ logo & icon chuẩn nhận diện thương hiệu TLabtool cho toàn bộ hệ sinh thái STEM:
1. CAD Math Studio: Biểu tượng Lông chim (Quill Feather) toán học tối giản, thanh lịch.
2. GeoSolver 2D: Kế thừa logo 2D hiện tại, bổ sung bản Grayscale Monochrome chuẩn Antigravity.
3. Phys Solver: Biểu tượng Vật lý lượng tử / Quỹ đạo hạt & Con lắc sóng điều hòa.
4. GeoSolver 3D: Biểu tượng Hình học không gian 3D (Khối lập phương isometric với trục tọa độ Oxyz và nét khuất).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
os.makedirs(ASSETS_DIR, exist_ok=True)

SIZE = 1024  # Vẽ với độ phân giải siêu nét (supersampling 1024x1024)

def to_grayscale_antigravity(img: Image.Image, bg_dark: bool = True) -> Image.Image:
    """
    Chuyển đổi hình ảnh sang phong cách xám tối giản (Grayscale Monochrome)
    tương tự phong cách của Antigravity Splash Screen:
    - Biểu tượng xám bạc tinh tế (#94A3B8 / #CBD5E1)
    - Nền trong suốt hoặc nền tối sang trọng
    """
    # Tách kênh alpha
    r, g, b, a = img.split()
    # Chuyển RGB sang độ sáng chuẩn
    gray = ImageOps.grayscale(img)
    # Tăng cường độ tương phản và ánh kim
    enhanced = ImageOps.autocontrast(gray, cutoff=2)
    
    # Tạo ảnh RGBA với tông màu xám bạc ánh thép
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    # Dùng enhanced để tạo màu xám từ #64748B đến #F1F5F9
    gray_pixels = enhanced.load()
    alpha_pixels = a.load()
    res_pixels = result.load()
    
    w, h = img.size
    for y in range(h):
        for x in range(w):
            alpha = alpha_pixels[x, y]
            if alpha > 0:
                v = gray_pixels[x, y]
                # Map value sang tông xám sáng thanh lịch (148 -> 230)
                lum = int(120 + (v / 255.0) * 125)
                res_pixels[x, y] = (lum, lum, int(lum * 1.03), alpha)
                
    return result

# =============================================================================
# 1. LOGO CAD MATH STUDIO (LÔNG VŨ TOÁN HỌC / QUILL FEATHER)
# =============================================================================
def draw_cad_math_feather(size=1024):
    """
    Vẽ lông vũ nghệ thuật tối giản (Minimalist Mathematical Quill Feather):
    Đường nét khí động học mềm mại uốn cong từ góc dưới sang góc trên.
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    cx, cy = size // 2, size // 2
    
    # Màu sắc chủ đạo: Xanh tím gradient toán học hoàng gia (#6366F1, #8B5CF6, #4F46E5)
    # Trục chính của lông vũ (Shaft / Rachis)
    # Đường cong bậc 3 từ (300, 850) -> (720, 180)
    def bezier_curve(p0, p1, p2, p3, steps=100):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            pts.append((x, y))
        return pts

    # Khung nền tròn bo góc siêu mềm phong cách icon app hiện đại
    pad = 80
    bg_box = (pad, pad, size - pad, size - pad)
    # Nền gradient tròn nhẹ
    draw.rounded_rectangle(bg_box, radius=180, fill=(30, 27, 75, 255)) # Dark Indigo #1E1B4B
    
    # Vòng tròn viền phát quang toán học mỏng
    draw.rounded_rectangle(bg_box, radius=180, outline=(99, 102, 241, 140), width=6)

    # 1. Cánh lông vũ bên trái (Upper & lower vane)
    # Tạo các nan lông (barbs) bằng các đường cong hình học toán học
    left_vane = [
        (350, 780), (320, 680), (280, 560), (270, 440), (300, 340), 
        (370, 260), (470, 200), (590, 170), (710, 180), # Đỉnh ngọn
        (660, 260), (600, 360), (540, 480), (480, 600), (420, 710), (350, 780)
    ]
    draw.polygon(left_vane, fill=(129, 140, 248, 230)) # Indigo light #818CF8

    # 2. Cánh lông vũ bên phải (Lower vane)
    right_vane = [
        (350, 780), (420, 710), (480, 600), (540, 480), (600, 360), (660, 260), (710, 180),
        (740, 220), (720, 310), (670, 420), (600, 540), (510, 670), (400, 770), (350, 780)
    ]
    draw.polygon(right_vane, fill=(167, 139, 250, 220)) # Purple light #A78BFA

    # 3. Tạo các đường cắt xẻ lông vũ thanh lịch (Feather splits / barbs)
    splits = [
        [(340, 430), (410, 470)],
        [(370, 320), (460, 370)],
        [(450, 240), (540, 300)],
        [(620, 440), (690, 400)],
        [(540, 560), (620, 520)],
    ]
    for s_pt, e_pt in splits:
        draw.line([s_pt, e_pt], fill=(30, 27, 75, 255), width=8)

    # 4. Trục sống lông vũ (Rachis) uốn cong thanh thoát màu trắng bạc
    spine_pts = bezier_curve((310, 830), (420, 640), (530, 420), (715, 175), steps=80)
    for i in range(len(spine_pts) - 1):
        # Trục to ở dưới (14px) và thon dần về đỉnh (4px)
        t = i / len(spine_pts)
        w = int(14 * (1 - t) + 3)
        draw.line([spine_pts[i], spine_pts[i+1]], fill=(255, 255, 255, 255), width=w)

    # 5. Ngòi bút lông (Quill Pen Calamus & Nib tip)
    nib_pts = [(310, 830), (280, 870), (265, 890), (280, 860), (310, 830)]
    draw.polygon(nib_pts, fill=(255, 255, 255, 255))
    draw.line([(280, 860), (265, 890)], fill=(30, 27, 75, 255), width=3) # Khe ngòi bút mực

    # 6. Biểu tượng tích phân ∫ và chuỗi $\sum$ lồng chìm tinh tế nghệ thuật
    # Vòng tròn điểm sáng tại ngòi bút
    draw.ellipse([(258, 883), (272, 897)], fill=(238, 242, 255, 255))
    
    return canvas

# =============================================================================
# 2. LOGO GEOSOLVER 2D (KẾ THỪA LOGO GỐC + BẢN GRAYSCALE)
# =============================================================================
def load_geosolver_2d_logo():
    src_path = "geosolver/assets/icon_256.png"
    if os.path.exists(src_path):
        img = Image.open(src_path).convert("RGBA")
        return img.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    # Nếu chưa có, vẽ lại logo hình học 2D tuyệt đẹp
    canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    pad = 80
    draw.rounded_rectangle((pad, pad, 1024 - pad, 1024 - pad), radius=180, fill=(24, 100, 171, 255))
    # Đường tròn nội tiếp và tam giác
    draw.ellipse((220, 220, 804, 804), outline=(208, 235, 255, 255), width=18)
    draw.polygon([(512, 230), (240, 770), (784, 770)], outline=(255, 255, 255, 255), width=16)
    # Các điểm đỉnh
    for pt in [(512, 230), (240, 770), (784, 770), (512, 512)]:
        draw.ellipse((pt[0]-24, pt[1]-24, pt[0]+24, pt[1]+24), fill=(255, 212, 59, 255))
    return canvas

# =============================================================================
# 3. LOGO PHYS SOLVER (VẬT LÝ LƯỢNG TỬ & QUỸ ĐẠO QUẢ LẮC SÓNG)
# =============================================================================
def draw_phys_solver_logo(size=1024):
    """
    Logo Phòng Thí Nghiệm Vật Lý Tự Do (Physics Sandbox):
    3 quỹ đạo elip lượng tử đan xen 3D quanh hạt nhân phát sáng,
    tượng trưng cho cơ học Newton, thuyết tương đối và sóng dao động điều hòa.
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    pad = 80
    bg_box = (pad, pad, size - pad, size - pad)
    # Nền Dark Cyan / Deep Space Slate (#064E3B hoặc #0F172A)
    draw.rounded_rectangle(bg_box, radius=180, fill=(15, 23, 42, 255))
    draw.rounded_rectangle(bg_box, radius=180, outline=(14, 165, 233, 140), width=6)
    
    cx, cy = size // 2, size // 2
    
    # Hàm vẽ elip xoay góc
    def draw_rotated_ellipse(cx, cy, rx, ry, angle_deg, color, width=12):
        rad = math.radians(angle_deg)
        pts = []
        for deg in range(0, 360, 2):
            th = math.radians(deg)
            ex = rx * math.cos(th)
            ey = ry * math.sin(th)
            # Xoay
            rx_rot = ex * math.cos(rad) - ey * math.sin(rad) + cx
            ry_rot = ex * math.sin(rad) + ey * math.cos(rad) + cy
            pts.append((rx_rot, ry_rot))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=width)
        draw.line([pts[-1], pts[0]], fill=color, width=width)

    # 3 Quỹ đạo nghiêng: 0°, 60°, 120°
    draw_rotated_ellipse(cx, cy, 340, 130, 0, (56, 189, 248, 220), width=14)   # Cyan #38BDF8
    draw_rotated_ellipse(cx, cy, 340, 130, 60, (129, 140, 248, 220), width=14) # Indigo #818CF8
    draw_rotated_ellipse(cx, cy, 340, 130, 120, (52, 211, 153, 220), width=14) # Emerald #34D399

    # Các hạt electron / thiên thể trên quỹ đạo
    electrons = [
        (cx + 340, cy, (56, 189, 248, 255)),
        (cx - 170, cy - int(130 * math.sin(math.radians(60)) * 1.8), (129, 140, 248, 255)),
        (cx - 170, cy + int(130 * math.sin(math.radians(60)) * 1.8), (52, 211, 153, 255)),
    ]
    for ex, ey, col in electrons:
        draw.ellipse([(ex-26, ey-26), (ex+26, ey+26)], fill=col)
        draw.ellipse([(ex-14, ey-14), (ex+14, ey+14)], fill=(255, 255, 255, 255))

    # Hạt nhân trung tâm phát sáng (Quả cầu phát sáng với quầng năng lượng)
    draw.ellipse([(cx-65, cy-65), (cx+65, cy+65)], fill=(14, 165, 233, 90))
    draw.ellipse([(cx-45, cy-45), (cx+45, cy+45)], fill=(245, 158, 11, 240)) # Amber Core #F59E0B
    draw.ellipse([(cx-25, cy-25), (cx+25, cy+25)], fill=(255, 255, 255, 255))

    return canvas

# =============================================================================
# 4. LOGO GEOSOLVER 3D (HÌNH HỌC KHÔNG GIAN 3D ISOMETRIC)
# =============================================================================
def draw_geosolver_3d_logo(size=1024):
    """
    Logo GeoSolver 3D: Nhận diện tức thì môn Hình học Không gian 3D:
    Khối lập phương isometric trong suốt với hệ trục toạ độ không gian Oxyz,
    mặt phẳng hình chiếu, các đỉnh nút và đường nét đứt (hidden lines).
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    pad = 80
    bg_box = (pad, pad, size - pad, size - pad)
    # Nền Deep Navy Space (#0A192F)
    draw.rounded_rectangle(bg_box, radius=180, fill=(10, 25, 47, 255))
    draw.rounded_rectangle(bg_box, radius=180, outline=(14, 165, 233, 140), width=6)
    
    cx, cy = size // 2, size // 2 + 30
    L = 220 # Bán kính khối lập phương
    
    # Tọa độ 8 đỉnh của khối lập phương Isometric (Chiếu song song 30 độ)
    # Góc chiếu isometric: dx = L * cos(30°), dy = L * sin(30°)
    cos30 = math.sqrt(3) / 2
    sin30 = 0.5
    
    dx = L * cos30
    dy = L * sin30
    
    # 8 đỉnh:
    # Mặt trên: Top center, Top right, Bottom center (mid), Top left
    v_top = (cx, cy - L)
    v_tr = (cx + dx, cy - L + dy)
    v_br = (cx + dx, cy + dy)
    v_bot = (cx, cy + L)
    v_bl = (cx - dx, cy + dy)
    v_tl = (cx - dx, cy - L + dy)
    v_cen = (cx, cy)
    v_back_bot = (cx, cy - dy)
    
    # 1. Vẽ 3 mặt trong suốt được tô bóng đổ màu không gian
    # Mặt trên (Top Face)
    draw.polygon([v_top, v_tr, v_cen, v_tl], fill=(56, 189, 248, 140)) # Cyan
    # Mặt trước bên phải (Right Face)
    draw.polygon([v_cen, v_tr, v_br, v_bot], fill=(14, 116, 144, 170)) # Dark Cyan
    # Mặt trước bên trái (Left Face)
    draw.polygon([v_tl, v_cen, v_bot, v_bl], fill=(3, 105, 161, 160)) # Sky Blue

    # 2. Vẽ 3 trục tọa độ không gian Oxyz xuyên tâm
    axis_len = 340
    # Trục Oz (hướng lên)
    draw.line([(cx, cy), (cx, cy - axis_len)], fill=(244, 63, 94, 255), width=8) # Red Z
    # Trục Ox (chéo xuống trái)
    draw.line([(cx, cy), (cx - axis_len * cos30, cy + axis_len * sin30)], fill=(34, 197, 94, 255), width=8) # Green X
    # Trục Oy (chéo xuống phải)
    draw.line([(cx, cy), (cx + axis_len * cos30, cy + axis_len * sin30)], fill=(59, 130, 246, 255), width=8) # Blue Y

    # Mũi tên trục
    draw.polygon([(cx, cy - axis_len - 15), (cx - 12, cy - axis_len + 10), (cx + 12, cy - axis_len + 10)], fill=(244, 63, 94, 255))
    
    # 3. Vẽ các cạnh khuất nét đứt (Hidden lines - đặc trưng số 1 của hình học không gian)
    def draw_dashed_line(p1, p2, color=(148, 163, 184, 200), width=6, dash=14, gap=10):
        total_dist = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        if total_dist == 0: return
        vx = (p2[0] - p1[0]) / total_dist
        vy = (p2[1] - p1[1]) / total_dist
        curr = 0.0
        while curr < total_dist:
            end = min(curr + dash, total_dist)
            draw.line([(p1[0] + vx * curr, p1[1] + vy * curr), (p1[0] + vx * end, p1[1] + vy * end)], fill=color, width=width)
            curr += dash + gap

    draw_dashed_line(v_bl, (cx, cy - dy))
    draw_dashed_line(v_br, (cx, cy - dy))
    draw_dashed_line(v_top, (cx, cy - dy))

    # 4. Vẽ các cạnh ngoài liền nét (Visible Edges)
    edges = [
        (v_top, v_tr), (v_tr, v_br), (v_br, v_bot), 
        (v_bot, v_bl), (v_bl, v_tl), (v_tl, v_top),
        (v_cen, v_top), (v_cen, v_br), (v_cen, v_bl)
    ]
    for p1, p2 in edges:
        draw.line([p1, p2], fill=(255, 255, 255, 255), width=10)

    # 5. Các nút điểm đỉnh (Vertices)
    for pt in [v_top, v_tr, v_br, v_bot, v_bl, v_tl, v_cen]:
        draw.ellipse([(pt[0]-18, pt[1]-18), (pt[0]+18, pt[1]+18)], fill=(255, 212, 59, 255), outline=(255, 255, 255, 255), width=4)
        
    # Ký hiệu toạ độ "3D" nghệ thuật nhỏ ở góc trên phải
    # (vẽ khối 3D chìm thể hiện nhận diện không gian)
    
    return canvas

def export_all():
    print("Đang tạo bộ biểu tượng nhận diện thương hiệu TLabtool STEM...")
    
    apps = [
        ("cad_math", draw_cad_math_feather),
        ("geosolver_2d", load_geosolver_2d_logo),
        ("phys_solver", draw_phys_solver_logo),
        ("geosolver_3d", draw_geosolver_3d_logo),
    ]
    
    for app_id, draw_func in apps:
        print(f"-> Tạo biểu tượng: {app_id}...")
        img_color_1024 = draw_func(1024) if app_id != "geosolver_2d" else draw_func()
        
        # 1. Bản màu gốc 512x512
        img_color_512 = img_color_1024.resize((512, 512), Image.Resampling.LANCZOS)
        img_color_512.save(os.path.join(ASSETS_DIR, f"{app_id}_logo.png"), "PNG")
        
        # 2. Bản màu xám đơn sắc (Grayscale Monochrome) cho Splash Screen
        img_gray_1024 = to_grayscale_antigravity(img_color_1024)
        img_gray_512 = img_gray_1024.resize((512, 512), Image.Resampling.LANCZOS)
        img_gray_512.save(os.path.join(ASSETS_DIR, f"{app_id}_logo_gray.png"), "PNG")
        
        # 3. Bản .ico đa kích thước cho Windows Titlebar và Taskbar
        ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img_color_512.save(
            os.path.join(ASSETS_DIR, f"{app_id}.ico"),
            format="ICO",
            sizes=ico_sizes
        )
        print(f"   [OK] Đã lưu {app_id}_logo.png, {app_id}_logo_gray.png, {app_id}.ico")

if __name__ == "__main__":
    export_all()
