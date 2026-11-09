# -*- coding: utf-8 -*-
"""
render_premium_logos.py
=======================
Bộ tạo biểu tượng thương hiệu TLabtool chuẩn High-End Vector Supersampling (2048x2048):
1. CAD Math Studio: Lông vũ toán học Navy & Obsidian siêu sắc nét, tương phản cao, sang trọng đẳng cấp.
2. GeoSolver 2D: Tái tạo vector toán học siêu nét (Tam giác & Đường tròn nội tiếp Euclid), phóng to không bao giờ vỡ hạt.
3. Phys Solver: Con lắc va chạm Newton (Newton's Cradle) - biểu tượng kinh điển số 1 của Cơ học & Vật lý thực nghiệm.
4. GeoSolver 3D: Khối lập phương không gian Isometric Oxyz với nét đứt khuất SGK chuẩn xác.
"""

import os
import sys
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
os.makedirs(ASSETS_DIR, exist_ok=True)

# Độ phân giải vẽ siêu mịn (2048 x 2048)
HI_RES = 2048

# =============================================================================
# HÀM BỔ TRỢ HÌNH HỌC & ÁNH SÁNG METALLIC
# =============================================================================

def draw_sphere_3d(draw, cx, cy, radius, base_col, light_offset=(-0.35, -0.35)):
    """Vẽ quả cầu 3D metallic với tâm sáng phản quang siêu mịn."""
    # Vẽ các lớp vòng tròn gradient từ ngoài vào trong
    steps = int(radius * 1.5)
    r_base, g_base, b_base = base_col[:3]
    lx = cx + light_offset[0] * radius
    ly = cy + light_offset[1] * radius
    
    for i in range(steps, 0, -1):
        t = i / steps
        cur_r = radius * t
        # Tâm dời dần về phía nguồn sáng
        cur_cx = cx + (lx - cx) * (1 - t)
        cur_cy = cy + (ly - cy) * (1 - t)
        
        # Độ sáng tăng dần về tâm sáng
        lum = (1 - t) ** 1.4
        cr = min(255, int(r_base * (0.3 + 0.7 * t) + 255 * lum * 0.8))
        cg = min(255, int(g_base * (0.3 + 0.7 * t) + 255 * lum * 0.8))
        cb = min(255, int(b_base * (0.3 + 0.7 * t) + 255 * lum * 0.8))
        
        draw.ellipse([cur_cx - cur_r, cur_cy - cur_r, cur_cx + cur_r, cur_cy + cur_r], fill=(cr, cg, cb, 255))

def to_grayscale_antigravity(img: Image.Image) -> Image.Image:
    """
    Chuyển đổi hình ảnh sang phong cách xám titan/slate tối giản cho Splash Screen nền sáng:
    - Tone xám đậm Slate 700 (#334155 - #64748B) để tương phản sắc nét trên nền trắng/xám Cursor / Antigravity.
    """
    r, g, b, a = img.split()
    gray = ImageOps.grayscale(img)
    enhanced = ImageOps.autocontrast(gray, cutoff=2)
    
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gray_pixels = enhanced.load()
    alpha_pixels = a.load()
    res_pixels = result.load()
    
    w, h = img.size
    for y in range(h):
        for x in range(w):
            alpha = alpha_pixels[x, y]
            if alpha > 0:
                v = gray_pixels[x, y]
                # Tone xám titan Slate 700 - Slate 500 nổi bật trên nền sáng
                lum = int(55 + (v / 255.0) * 115)
                res_pixels[x, y] = (int(lum * 0.95), int(lum * 0.98), int(lum * 1.05), alpha)
                
    return result

# =============================================================================
# 1. LOGO CAD MATH STUDIO (CHIẾC LÔNG VŨ NAVY & OBSIDIAN ĐẲNG CẤP)
# =============================================================================

def draw_cad_math_luxury_feather(size=HI_RES):
    """
    Biểu tượng Lông Vũ CAD Math Studio HD Siêu Sắc Nét (Khắc phục hoàn toàn lỗi nhòe & bố cục đầu lông):
    - Tái tạo trọn vẹn 100% dáng chiếc lông vũ organic được người dùng lựa chọn.
    - Cuống lông (calamus) được hoàn thiện thon mượt dứt khoát, kết thúc bằng đầu bo tròn sắc sảo, không còn bị cắt vụn hay nhòe mực.
    - Bố cục 2 nửa tương phản cao: Cánh phải Royal Navy (#0969DA) & Electric Azure rực rỡ; Cánh trái Midnight Obsidian (#0A192F) sâu thẳm.
    - Sống lông bạch kim Platinum Chrome sắc mảnh chia đôi hai vạt lông.
    - Độ nghiêng chuẩn 45 độ thanh thoát.
    """
    v2_path = os.path.join(ASSETS_DIR, "cad_math_logo_v2_300x300.png")
    if os.path.exists(v2_path):
        img_v2 = Image.open(v2_path).convert("RGBA")
        if img_v2.size != (size, size):
            img_v2 = img_v2.resize((size, size), Image.Resampling.LANCZOS)
            r, g, b, a = img_v2.split()
            rgb = Image.merge("RGB", (r, g, b)).filter(
                ImageFilter.UnsharpMask(radius=1.8, percent=140, threshold=1)
            )
            img_v2 = Image.merge("RGBA", (*rgb.split(), a))
        return img_v2

    hd_path = os.path.join(ASSETS_DIR, "cad_math_feather_90pct_navy_45deg.png")
    if os.path.exists(hd_path):
        img_hd = Image.open(hd_path)
        if img_hd.size != (size, size):
            img_hd = img_hd.resize((size, size), Image.Resampling.LANCZOS)
        return img_hd

    ref_path = os.path.join(ASSETS_DIR, "ref_feather.jpg")
    if os.path.exists(ref_path):
        try:
            from scipy.ndimage import label, binary_fill_holes, distance_transform_edt, gaussian_filter1d
            from scipy.spatial import cKDTree
            img_ref = Image.open(ref_path).convert("RGB")
            arr = np.array(img_ref).astype(np.float32)

            bg_col = np.array([238.0, 239.0, 241.0])
            dist_to_bg = np.linalg.norm(arr - bg_col, axis=2)

            mask = dist_to_bg > 35.0
            mask[915:985, 300:670] = False # Loại bỏ chữ 300x300 px
            mask[:20, :] = False
            mask[1000:, :] = False
            mask[:, :20] = False
            mask[:, 1000:] = False

            lbl, n_lbl = label(mask)
            sizes = np.bincount(lbl.ravel())
            sizes[0] = 0
            feather_lbl = sizes.argmax()
            feather_mask = (lbl == feather_lbl)

            wisp_mask = (lbl > 0) & (arr.mean(axis=2) < 210) & (~feather_mask)
            dt = distance_transform_edt(~feather_mask)
            feather_mask = feather_mask | (wisp_mask & (dt < 25))
            feather_mask = binary_fill_holes(feather_mask)

            # Khớp sống lông (spine) chính xác
            pts = np.array([
                [75, 960], [105, 915], [155, 835], [225, 735],
                [320, 600], [450, 440], [600, 280], [740, 150], [880, 50]
            ], dtype=np.float32)
            t_pts = np.linspace(0, 1, len(pts))
            poly_x = np.polyfit(t_pts, pts[:, 0], deg=3)
            poly_y = np.polyfit(t_pts, pts[:, 1], deg=3)

            ts = np.linspace(0, 1, 1000)
            sx = np.polyval(poly_x, ts)
            sy = np.polyval(poly_y, ts)
            spine_coords = np.column_stack([sx, sy])
            tree = cKDTree(spine_coords)

            dx = np.polyval(np.polyder(poly_x), ts)
            dy = np.polyval(np.polyder(poly_y), ts)
            lens = np.hypot(dx, dy)
            tx = dx / lens
            ty = dy / lens

            y_idx, x_idx = np.where(feather_mask)
            query_pts = np.column_stack([x_idx, y_idx])
            dists, nearest_idx = tree.query(query_pts)

            t_n = ts[nearest_idx]
            s_xn = sx[nearest_idx]
            s_yn = sy[nearest_idx]
            t_xn = tx[nearest_idx]
            t_yn = ty[nearest_idx]

            cross = (x_idx - s_xn) * t_yn - (y_idx - s_yn) * t_xn
            d_perp = np.abs(cross)

            # Ước tính độ rộng cánh phải và loại bỏ hoàn toàn vết loang (Zero Splotches)
            t_bins = np.linspace(0, 1, 51)
            w_right_max = np.zeros(len(ts))
            right_mask = cross > 0
            for i in range(50):
                in_bin = right_mask & (t_n >= t_bins[i]) & (t_n < t_bins[i+1])
                if np.any(in_bin):
                    max_d = np.percentile(d_perp[in_bin], 98)
                else:
                    max_d = 50.0
                w_right_max[int(i*20):int((i+1)*20)] = max(max_d, 20.0)

            w_right_max = gaussian_filter1d(w_right_max, sigma=15)
            w_r_pixel = w_right_max[nearest_idx]
            u_right = np.clip(d_perp / (w_r_pixel + 1e-5), 0.0, 1.0)

            # Tái tạo các nan lông song song chân thực ôm theo sống lông
            theta_r = np.radians(34)
            b_coord_r = (x_idx - s_xn) * np.sin(theta_r) + (y_idx - s_yn) * np.cos(theta_r) + t_n * 600.0
            striation_r = 0.5 + 0.5 * np.cos(2 * np.pi * b_coord_r / 10.0)

            light_right = 0.15 + 0.55 * np.sin(u_right * np.pi * 0.85) + 0.18 * striation_r * (1.0 - np.exp(-d_perp / 10.0))
            rim_r = np.exp(-((1.0 - u_right) ** 2) / 0.04)
            light_right = np.clip(light_right + 0.22 * rim_r, 0.0, 1.0)

            # Cánh trái
            orig_gray = 0.299 * arr[y_idx, x_idx, 0] + 0.587 * arr[y_idx, x_idx, 1] + 0.114 * arr[y_idx, x_idx, 2]
            p_min, p_max = np.percentile(orig_gray, 2), np.percentile(orig_gray, 98)
            norm_orig = np.clip((orig_gray - p_min) / (p_max - p_min + 1e-5), 0.0, 1.0)

            final_light = np.where(cross > 0, light_right, norm_orig * 0.9 + 0.1)

            # Sống lông có lõi bạch kim
            platinum_core = np.exp(-(d_perp ** 2) / 3.0) * (t_n ** 0.5)

            # Phối màu tương phản cao sang trọng
            c_obs = np.array([3.0, 10.0, 28.0])        # Midnight Obsidian
            c_navy = np.array([9.0, 52.0, 135.0])       # Deep Navy
            c_royal = np.array([14.0, 105.0, 218.0])    # Royal Navy Antigravity (#0969DA)
            c_azure = np.array([80.0, 185.0, 255.0])    # Electric Azure Highlight
            c_plat = np.array([245.0, 248.0, 255.0])    # Platinum Core

            t_col = final_light[:, None]
            out_rgb = np.zeros((len(x_idx), 3), dtype=np.float32)

            m0 = (t_col < 0.35)
            t0 = np.clip(t_col / 0.35, 0.0, 1.0)
            out_rgb += m0 * (c_obs * (1.0 - t0) + c_navy * t0)

            m1 = (t_col >= 0.35) & (t_col < 0.70)
            t1 = np.clip((t_col - 0.35) / 0.35, 0.0, 1.0)
            out_rgb += m1 * (c_navy * (1.0 - t1) + c_royal * t1)

            m2 = (t_col >= 0.70)
            t2 = np.clip((t_col - 0.70) / 0.30, 0.0, 1.0)
            out_rgb += m2 * (c_royal * (1.0 - t2) + c_azure * t2)

            plat_amt = (platinum_core[:, None] * 0.75) * (t_n[:, None] > 0.05)
            out_rgb = out_rgb * (1.0 - plat_amt) + c_plat * plat_amt

            alpha = (feather_mask.astype(np.float32) * 255.0)
            alpha_img = Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
            alpha_smooth = np.array(alpha_img)

            out_rgba = np.zeros((1024, 1024, 4), dtype=np.uint8)
            out_rgba[y_idx, x_idx, :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)
            out_rgba[y_idx, x_idx, 3] = alpha_smooth[y_idx, x_idx]

            feather_img = Image.fromarray(out_rgba, "RGBA")
            if size != 1024:
                feather_img = feather_img.resize((size, size), Image.Resampling.LANCZOS)
            return feather_img
        except Exception as ex:
            print(f"Fallback to procedural feather: {ex}")

    # Thuật toán dự phòng (Procedural Vector Feather)
    scale = size / 1024.0
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # 1. Nền squircle tối giản sang trọng (Dark Obsidian Slate #090D16)
    pad = int(80 * scale)
    radius = int(190 * scale)
    bg_box = (pad, pad, size - pad, size - pad)
    
    draw.rounded_rectangle(bg_box, radius=radius, fill=(9, 13, 22, 255)) # Dark Obsidian
    # Đường viền hairline siêu mảnh ánh xanh Navy tinh tế
    draw.rounded_rectangle(bg_box, radius=radius, outline=(14, 165, 233, 110), width=int(5 * scale))

    # Định nghĩa các điểm điều khiển của sống lông (Rachis curve)
    # Đường cong nhẹ nhàng từ (260, 860) qua (480, 560), (660, 340) tới đỉnh (850, 140)
    spine_control_pts = [
        (230 * scale, 870 * scale),
        (380 * scale, 680 * scale),
        (540 * scale, 480 * scale),
        (690 * scale, 300 * scale),
        (840 * scale, 145 * scale)
    ]
    
    def get_spine_point(t):
        # Đường cong Bezier bậc 4
        n = len(spine_control_pts) - 1
        x, y = 0.0, 0.0
        for i, (px, py) in enumerate(spine_control_pts):
            coeff = math.comb(n, i) * ((1 - t) ** (n - i)) * (t ** i)
            x += coeff * px
            y += coeff * py
        return x, y

    def get_spine_tangent(t):
        dt = 0.001
        t0 = max(0.0, t - dt)
        t1 = min(1.0, t + dt)
        x0, y0 = get_spine_point(t0)
        x1, y1 = get_spine_point(t1)
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length == 0: return (1.0, 0.0), (0.0, 1.0)
        tx, ty = dx / length, dy / length
        nx, ny = -ty, tx # Pháp tuyến hướng sang cánh trái (upper vane)
        return (tx, ty), (nx, ny)

    # 2. Xây dựng các phân đoạn lông vũ (Vane Lobes) chính xác theo ảnh mẫu của người dùng:
    # Cánh trên (Left / Upper Vane): 3 khía xẻ lớn đặc trưng
    # Cánh dưới (Right / Lower Vane): Khía xẻ mượt mà ôm sát sống lông
    
    # Tạo các lớp nan lông (Feather Barbs) với gradient Navy Antigravity
    num_barbs = 400
    for i in range(num_barbs):
        t = i / num_barbs
        sx, sy = get_spine_point(t)
        (tx, ty), (nx, ny) = get_spine_tangent(t)
        
        # Góc xiên của sợi lông so với sống: ~35 độ
        angle_rad = math.radians(35)
        # Vector sợi lông bên trái
        bx_left = tx * math.cos(angle_rad) + nx * math.sin(angle_rad)
        by_left = ty * math.cos(angle_rad) + ny * math.sin(angle_rad)
        # Vector sợi lông bên phải
        bx_right = tx * math.cos(angle_rad) - nx * math.sin(angle_rad)
        by_right = ty * math.cos(angle_rad) - ny * math.sin(angle_rad)
        
        # Chiều rộng cánh lông vũ tại t theo đúng dáng chiếc lông mẫu
        # Đường bao cánh trái có 3 vết lõm sâu (feather splits)
        # Lobe 1: t in [0.15, 0.45], Lobe 2: t in [0.48, 0.75], Lobe 3: t in [0.77, 0.98]
        if t < 0.12:
            w_left = t / 0.12 * 70 * scale
        elif t < 0.42:
            w_left = (120 + 80 * math.sin((t - 0.12) / 0.30 * math.pi)) * scale
        elif t < 0.45:
            w_left = 60 * scale # Vết xẻ 1
        elif t < 0.72:
            w_left = (150 + 90 * math.sin((t - 0.45) / 0.27 * math.pi)) * scale
        elif t < 0.75:
            w_left = 70 * scale # Vết xẻ 2
        else:
            w_left = (160 * math.sin((t - 0.75) / 0.25 * math.pi)) * scale

        # Chiều rộng cánh phải (Lower vane)
        if t < 0.15:
            w_right = t / 0.15 * 50 * scale
        elif t < 0.60:
            w_right = (100 + 70 * math.sin((t - 0.15) / 0.45 * math.pi)) * scale
        elif t < 0.63:
            w_right = 50 * scale # Vết xẻ nhỏ
        elif t < 0.88:
            w_right = (90 + 50 * math.sin((t - 0.63) / 0.25 * math.pi)) * scale
        elif t < 0.90:
            w_right = 35 * scale
        else:
            w_right = (80 * math.sin((t - 0.90) / 0.10 * math.pi)) * scale
            
        # Vẽ sợi lông bên trái
        if w_left > 1:
            ex = sx + bx_left * w_left
            ey = sy + by_left * w_left
            # Phối màu tương phản cao: Xanh Navy Antigravity (#0969DA, #1E40AF)
            # Gần sống lông đậm (Dark Navy #0A192F), ngọn sợi sáng (Vibrant Royal Blue #2563EB / Cyan Highlight #38BDF8)
            col_dark = (10, 25, 55, 255)
            col_bright = (37, 99, 235, 255)
            # Vẽ đường nét sắc mịn
            draw.line([(sx, sy), (ex, ey)], fill=col_bright, width=int(5 * scale))
            draw.line([(sx, sy), (sx + bx_left * (w_left * 0.45), sy + by_left * (w_left * 0.45))], fill=col_dark, width=int(6 * scale))
            # Điểm nhấn ánh sáng ở viền mép ngoài
            draw.line([(ex - bx_left * 6, ey - by_left * 6), (ex, ey)], fill=(96, 165, 250, 255), width=int(3 * scale))

        # Vẽ sợi lông bên phải
        if w_right > 1:
            ex_r = sx + bx_right * w_right
            ey_r = sy + by_right * w_right
            col_dark_r = (8, 20, 45, 255)
            col_bright_r = (29, 78, 216, 255) # Deep Royal Navy #1D4ED8
            draw.line([(sx, sy), (ex_r, ey_r)], fill=col_bright_r, width=int(5 * scale))
            draw.line([(sx, sy), (sx + bx_right * (w_right * 0.4), sy + by_right * (w_right * 0.4))], fill=col_dark_r, width=int(6 * scale))

    # 3. Phủ màng đổ bóng gradient và gân bóng mượt (Silky Feather Sheen)
    # Tạo các mảng sáng mềm mại uốn lượn trên thân lông vũ
    sheen_pts = [
        get_spine_point(0.2), get_spine_point(0.4), get_spine_point(0.65), get_spine_point(0.85)
    ]
    for pt in sheen_pts:
        draw.ellipse([pt[0]-40*scale, pt[1]-40*scale, pt[0]+40*scale, pt[1]+40*scale], fill=(30, 58, 138, 40))

    # 4. Vẽ Sống Lông Vũ (Rachis) Bạch Kim mạ Chrome sáng bóng cực kỳ sang trọng
    # Sống lông tương phản rực rỡ với màu xanh navy
    steps_spine = 200
    for i in range(steps_spine):
        t0 = i / steps_spine
        t1 = (i + 1) / steps_spine
        p0 = get_spine_point(t0)
        p1 = get_spine_point(t1)
        # Chiều rộng sống lông vuốt thon từ 18px ở gốc xuống 3px ở đỉnh
        w = int((16 * (1 - t0) + 3.5) * scale)
        # Lớp bóng đổ đậm dưới sống lông
        draw.line([(p0[0] + 3*scale, p0[1] + 3*scale), (p1[0] + 3*scale, p1[1] + 3*scale)], fill=(3, 7, 18, 200), width=w+int(4*scale))
        # Thân sống lông màu xanh dương sẫm
        draw.line([p0, p1], fill=(15, 23, 42, 255), width=w+int(2*scale))
        # Đường phản quang bạch kim sáng chói ở trung tâm sống lông (Crisp Platinum Core)
        draw.line([p0, p1], fill=(248, 250, 252, 255), width=max(1, int(w * 0.45)))
        # Ánh xanh Cyan Antigravity
        draw.line([(p0[0] - 1*scale, p0[1] - 1*scale), (p1[0] - 1*scale, p1[1] - 1*scale)], fill=(56, 189, 248, 220), width=max(1, int(w * 0.25)))

    # 5. Ngòi Bút Lông Vũ (Quill Calamus / Nib Tip):
    # Phần gốc biến hóa thành ngòi bút máy kim loại tinh xảo
    p_base = get_spine_point(0.0)
    p_next = get_spine_point(0.05)
    dx_tip = p_base[0] - p_next[0]
    dy_tip = p_base[1] - p_next[1]
    dist_tip = math.hypot(dx_tip, dy_tip)
    vx, vy = dx_tip / dist_tip, dy_tip / dist_tip
    
    nib_len = 55 * scale
    tip_pt = (p_base[0] + vx * nib_len, p_base[1] + vy * nib_len)
    
    # Vẽ ngòi bút mạ bạch kim vuốt nhọn
    draw.line([p_base, tip_pt], fill=(241, 245, 249, 255), width=int(12 * scale))
    draw.line([p_base, tip_pt], fill=(14, 165, 233, 255), width=int(4 * scale))
    # Khe mực ngòi bút (Breather slot)
    draw.ellipse([tip_pt[0]-4*scale, tip_pt[1]-4*scale, tip_pt[0]+4*scale, tip_pt[1]+4*scale], fill=(9, 13, 22, 255))
    
    return canvas

# =============================================================================
# 2. LOGO GEOSOLVER 2D (TÁI TẠO HOÀN TOÀN TỪ VECTOR TOÁN HỌC SIÊU NÉT)
# =============================================================================

def draw_geosolver_2d_highres(size=HI_RES):
    """
    Tái tạo trung thực 100% Logo GeoSolver 2D nguyên bản chuẩn hình học kỹ thuật siêu nét:
    - Bảo toàn nguyên vẹn cấu trúc mộc mạc và chuẩn xác mà người dùng yêu thích:
      1. Nền Squircle bo góc mềm mại màu Xanh Kỹ Thuật Royal CAD Blue (#1864AB).
      2. Viền hairline màu xanh sáng Light Cyan (#E0FDFF).
      3. Tam giác cân toán học viền trắng tinh khiết (#FFFFFF).
      4. Đường tròn màu vàng kim (#FFD936) tiếp xúc đáy tam giác.
      5. Tâm điểm tròn đỏ kỹ thuật (#E03131) tại chính tâm đường tròn.
    - Vẽ bằng toán vector độ phân giải cao 2048x2048: Tuyệt đối không bao giờ vỡ hạt hay mờ răng cưa.
    """
    scale = size / 150.0
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # 1. Nền Squircle Royal CAD Blue (#1864AB)
    pad = 5.0 * scale
    radius = 21.0 * scale
    border_w = int(round(3.5 * scale))
    box = [pad, pad, size - pad, size - pad]
    
    draw.rounded_rectangle(box, radius=radius, fill=(24, 100, 171, 255))
    draw.rounded_rectangle(box, radius=radius, outline=(224, 253, 255, 255), width=border_w)
    
    # 2. Tam giác toán học viền trắng tinh khiết
    Ax, Ay = 75.0 * scale, 27.0 * scale
    Bx, By = 27.0 * scale, 119.0 * scale
    Cx, Cy = 123.0 * scale, 119.0 * scale
    tri_w = int(round(3.8 * scale))
    
    draw.polygon([(Ax, Ay), (Bx, By), (Cx, Cy)], outline=(255, 255, 255, 255), width=tri_w)
    
    # 3. Đường tròn màu vàng kim (#FFD936) tiếp xúc đáy
    Ix, Iy = 75.0 * scale, 96.5 * scale
    r_in = 23.0 * scale
    circ_w = int(round(3.8 * scale))
    draw.ellipse([Ix - r_in, Iy - r_in, Ix + r_in, Iy + r_in], outline=(255, 217, 54, 255), width=circ_w)
    
    # 4. Tâm tròn đỏ kỹ thuật (#E03131)
    r_red = 3.2 * scale
    draw.ellipse([Ix - r_red, Iy - r_red, Ix + r_red, Iy + r_red], fill=(224, 49, 49, 255))
    
    return canvas

# =============================================================================
# 3. LOGO PHYS SOLVER (CON LẮC VA CHẠM NEWTON - BIỂU TƯỢNG VẬT LÝ KINH ĐIỂN)
# =============================================================================

def draw_physics_newton_cradle(size=HI_RES):
    """
    Logo Phòng Thí Nghiệm Vật Lý (Physics Sandbox Studio):
    Con lắc va chạm Newton (Newton's Cradle) - Biểu tượng số 1 của Vật lý học:
    - Khung treo kim loại Titanium cao cấp.
    - 5 quả cầu kim loại mạ Chrome sáng bóng phản chiếu ánh sáng 3D.
    - Quả cầu thứ 1 vung lên góc theta với vệt quỹ đạo động lượng (Momentum Arc),
      sẵn sàng va chạm đàn hồi truyền động lượng và bảo toàn năng lượng.
    - Nhận diện tức thì môn Vật lý cơ học & động lực học!
    """
    scale = size / 1024.0
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # 1. Nền Slate Deep Navy (#0B132B)
    pad = int(80 * scale)
    radius = int(190 * scale)
    bg_box = (pad, pad, size - pad, size - pad)
    
    draw.rounded_rectangle(bg_box, radius=radius, fill=(11, 19, 43, 255)) # Deep Physics Navy
    draw.rounded_rectangle(bg_box, radius=radius, outline=(56, 189, 248, 120), width=int(5 * scale))

    cx, cy = size // 2, size // 2
    
    # 2. Thanh treo ngang kim loại mạ Chrome (Suspension Bar)
    bar_y = 280 * scale
    bar_x1 = 260 * scale
    bar_x2 = 764 * scale
    
    # Đổ bóng thanh treo
    draw.rounded_rectangle([bar_x1, bar_y - 12*scale, bar_x2, bar_y + 12*scale], radius=int(6*scale), fill=(203, 213, 225, 255))
    draw.line([bar_x1, bar_y, bar_x2, bar_y], fill=(255, 255, 255, 255), width=int(4 * scale))
    
    # 3. Thông số 5 quả cầu kim loại
    ball_radius = 42 * scale
    string_len = 340 * scale
    
    # Vị trí cân bằng của 5 quả cầu (Quả 2, 3, 4, 5 đứng yên, quả 1 vung lên)
    # 4 quả tĩnh: Quả 2, 3, 4, 5 nằm ở x = cx - ball_radius, cx + ball_radius, ...
    center_spacing = ball_radius * 2.05
    
    # Quả 3 ở giữa cx
    x3 = cx
    x2 = cx - center_spacing
    x4 = cx + center_spacing
    x5 = cx + center_spacing * 2
    
    pivot_y = bar_y
    rest_y = bar_y + string_len
    
    # Quả 1: Vung sang trái với góc 40 độ
    theta = math.radians(42)
    pivot1_x = cx - center_spacing * 2
    ball1_x = pivot1_x - string_len * math.sin(theta)
    ball1_y = pivot_y + string_len * math.cos(theta)
    
    # 4. Vẽ Vệt quỹ đạo chuyển động động lượng (Motion Arc Trail) của Quả 1
    arc_pts = []
    for deg in range(0, 45, 2):
        rad = math.radians(deg)
        ax = pivot1_x - string_len * math.sin(rad)
        ay = pivot_y + string_len * math.cos(rad)
        arc_pts.append((ax, ay))
    for j in range(len(arc_pts) - 1):
        alpha_arc = int(220 * (j / len(arc_pts)))
        draw.line([arc_pts[j], arc_pts[j+1]], fill=(56, 189, 248, alpha_arc), width=int(6 * scale))

    # Vector vận tốc $\vec{v}$ tại quả 1
    v_start = (ball1_x, ball1_y)
    v_len = 70 * scale
    # Hướng tiếp tuyến
    v_end = (ball1_x + math.cos(theta) * v_len, ball1_y + math.sin(theta) * v_len)
    draw.line([v_start, v_end], fill=(234, 179, 8, 240), width=int(6 * scale)) # Vector màu vàng
    # Đầu mũi tên vector
    draw.polygon([v_end, (v_end[0]-14*scale, v_end[1]-6*scale), (v_end[0]-6*scale, v_end[1]-14*scale)], fill=(234, 179, 8, 255))

    # 5. Vẽ Các sợi dây treo (Suspension Strings - Dây đôi cho mỗi quả cầu)
    pivots = [pivot1_x, x2, x3, x4, x5]
    balls = [(ball1_x, ball1_y), (x2, rest_y), (x3, rest_y), (x4, rest_y), (x5, rest_y)]
    
    for (px, py), (bx, by) in zip([(pivot1_x, pivot_y), (x2, pivot_y), (x3, pivot_y), (x4, pivot_y), (x5, pivot_y)], balls):
        # Dây treo đôi tạo hình tam giác V mỏng
        draw.line([(px - 8*scale, py), (bx, by - ball_radius + 4*scale)], fill=(148, 163, 184, 210), width=int(3 * scale))
        draw.line([(px + 8*scale, py), (bx, by - ball_radius + 4*scale)], fill=(148, 163, 184, 210), width=int(3 * scale))

    # 6. Vẽ 5 Quả cầu Kim loại Chrome 3D siêu thực
    for idx, (bx, by) in enumerate(balls):
        # Đổ bóng dưới đất cho các quả tĩnh
        if idx > 0:
            draw.ellipse([bx - ball_radius*0.8, rest_y + ball_radius*1.3, bx + ball_radius*0.8, rest_y + ball_radius*1.55], fill=(5, 10, 20, 160))
        # Vẽ quả cầu kim loại 3D phản quang
        draw_sphere_3d(draw, bx, by, ball_radius, (180, 200, 225))
        # Vòng viền phản xạ ánh sáng kim loại
        draw.ellipse([bx - ball_radius, by - ball_radius, bx + ball_radius, by + ball_radius], outline=(255, 255, 255, 140), width=int(2 * scale))

    # Tia sáng năng lượng va chạm tại điểm tiếp xúc quả 4 & 5
    spark_x = (x4 + x5) / 2
    spark_y = rest_y
    draw.ellipse([spark_x - 12*scale, spark_y - 12*scale, spark_x + 12*scale, spark_y + 12*scale], fill=(255, 255, 255, 240))
    draw.ellipse([spark_x - 6*scale, spark_y - 6*scale, spark_x + 6*scale, spark_y + 6*scale], fill=(56, 189, 248, 255))

    return canvas

# =============================================================================
# 4. LOGO GEOSOLVER 3D (HÌNH HỌC KHÔNG GIAN 3D ISOMETRIC CHUẨN MỰC)
# =============================================================================

def draw_geosolver_3d_highres(size=HI_RES):
    """
    Tái tạo logo GeoSolver 3D ở độ phân giải 2048x2048 siêu nét:
    Khối lập phương isometric trong suốt với hệ trục tọa độ không gian Oxyz và nét đứt khuất SGK.
    """
    scale = size / 1024.0
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    pad = int(80 * scale)
    radius = int(190 * scale)
    bg_box = (pad, pad, size - pad, size - pad)
    
    draw.rounded_rectangle(bg_box, radius=radius, fill=(10, 25, 47, 255))
    draw.rounded_rectangle(bg_box, radius=radius, outline=(14, 165, 233, 140), width=int(5 * scale))
    
    cx, cy = size // 2, size // 2 + int(40 * scale)
    L = 230 * scale
    
    cos30 = math.sqrt(3) / 2
    sin30 = 0.5
    dx = L * cos30
    dy = L * sin30
    
    v_top = (cx, cy - L)
    v_tr = (cx + dx, cy - L + dy)
    v_br = (cx + dx, cy + dy)
    v_bot = (cx, cy + L)
    v_bl = (cx - dx, cy + dy)
    v_tl = (cx - dx, cy - L + dy)
    v_cen = (cx, cy)
    v_back_bot = (cx, cy - dy)
    
    # Mặt trong suốt có bóng đổ
    draw.polygon([v_top, v_tr, v_cen, v_tl], fill=(56, 189, 248, 130)) # Mặt trên Cyan
    draw.polygon([v_cen, v_tr, v_br, v_bot], fill=(14, 116, 144, 160)) # Mặt phải Dark Cyan
    draw.polygon([v_tl, v_cen, v_bot, v_bl], fill=(3, 105, 161, 150))  # Mặt trái Sky Blue

    # 3 Trục toạ độ Oxyz
    axis_len = 360 * scale
    draw.line([(cx, cy), (cx, cy - axis_len)], fill=(244, 63, 94, 255), width=int(10 * scale)) # Oz Đỏ
    draw.line([(cx, cy), (cx - axis_len * cos30, cy + axis_len * sin30)], fill=(34, 197, 94, 255), width=int(10 * scale)) # Ox Xanh lá
    draw.line([(cx, cy), (cx + axis_len * cos30, cy + axis_len * sin30)], fill=(59, 130, 246, 255), width=int(10 * scale)) # Oy Xanh dương

    # Nét đứt khuất SGK
    def draw_dashed(p1, p2, width=int(8*scale), dash=int(18*scale), gap=int(14*scale)):
        dist = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        if dist == 0: return
        vx, vy = (p2[0]-p1[0])/dist, (p2[1]-p1[1])/dist
        curr = 0.0
        while curr < dist:
            end = min(curr + dash, dist)
            draw.line([(p1[0]+vx*curr, p1[1]+vy*curr), (p1[0]+vx*end, p1[1]+vy*end)], fill=(148, 163, 184, 220), width=width)
            curr += dash + gap

    draw_dashed(v_bl, v_back_bot)
    draw_dashed(v_br, v_back_bot)
    draw_dashed(v_top, v_back_bot)

    # Nét liền thấy
    edges = [
        (v_top, v_tr), (v_tr, v_br), (v_br, v_bot), 
        (v_bot, v_bl), (v_bl, v_tl), (v_tl, v_top),
        (v_cen, v_top), (v_cen, v_br), (v_cen, v_bl)
    ]
    for p1, p2 in edges:
        draw.line([p1, p2], fill=(255, 255, 255, 255), width=int(14 * scale))

    # Đỉnh vàng 3D
    for pt in [v_top, v_tr, v_br, v_bot, v_bl, v_tl, v_cen]:
        draw_sphere_3d(draw, pt[0], pt[1], 20 * scale, (255, 212, 59))
        draw.ellipse([pt[0] - 20*scale, pt[1] - 20*scale, pt[0] + 20*scale, pt[1] + 20*scale], outline=(255, 255, 255, 255), width=int(3 * scale))

    return canvas

# =============================================================================
# QUẢN LÝ XUẤT TẬP TIN & ĐỒNG BỘ TOÀN HỆ THỐNG
# =============================================================================

def export_all_premium():
    print("======================================================================")
    print("  RENDER BỘ BIỂU TƯỢNG ĐẲNG CẤP TLABTOOL STEM (2048x2048 SUPERSAMPLING)")
    print("======================================================================")
    
    generators = [
        ("cad_math", draw_cad_math_luxury_feather, "CAD Math Studio (Lông vũ Navy & Obsidian)"),
        ("geosolver_2d", draw_geosolver_2d_highres, "GeoSolver 2D (Hình học phẳng Vector siêu nét)"),
        ("phys_solver", draw_physics_newton_cradle, "Phys Solver (Con lắc va chạm Newton 3D)"),
        ("geosolver_3d", draw_geosolver_3d_highres, "GeoSolver 3D (Đa diện không gian Isometric Oxyz)"),
    ]
    
    dest_folders = [
        ASSETS_DIR,
        os.path.abspath("cad_math_v2/assets"),
        os.path.abspath("geosolver/assets"),
        os.path.abspath("phys_solver/assets"),
        os.path.abspath("geosolver_3d/assets"),
    ]
    for d in dest_folders:
        os.makedirs(d, exist_ok=True)
        
    for app_id, draw_func, desc in generators:
        print(f"\n[RENDER] Đang vẽ {desc}...")
        img_2048 = draw_func(HI_RES)
        
        # 1. Downsample chất lượng cao bằng LANCZOS xuống 1024x1024 và 512x512
        img_1024 = img_2048.resize((1024, 1024), Image.Resampling.LANCZOS)
        img_512 = img_2048.resize((512, 512), Image.Resampling.LANCZOS)
        
        # 2. Tạo bản Grayscale Monochrome cho Splash Screen
        custom_gray_path = os.path.join(ASSETS_DIR, f"{app_id}_logo_gray_v2_300x300.png")
        if os.path.exists(custom_gray_path):
            g_raw = Image.open(custom_gray_path).convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
            gr, gg, gb, ga = g_raw.split()
            grgb_sharp = Image.merge("RGB", (gr, gg, gb)).filter(
                ImageFilter.UnsharpMask(radius=1.6, percent=130, threshold=1)
            )
            grgb_sharp = ImageEnhance.Contrast(grgb_sharp).enhance(1.12)
            img_gray_512 = Image.merge("RGBA", (*grgb_sharp.split(), ga))
        else:
            img_gray_512 = to_grayscale_antigravity(img_512)
        
        # 3. Tạo file Windows Icon .ICO đa kích thước
        ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Lưu vào ASSETS_DIR chung
        png_path = os.path.join(ASSETS_DIR, f"{app_id}_logo.png")
        gray_path = os.path.join(ASSETS_DIR, f"{app_id}_logo_gray.png")
        ico_path = os.path.join(ASSETS_DIR, f"{app_id}.ico")
        
        img_512.save(png_path, "PNG")
        img_gray_512.save(gray_path, "PNG")
        img_512.save(ico_path, format="ICO", sizes=ico_sizes)
        
        print(f"  -> Đã tạo: {app_id}_logo.png (512x512)")
        print(f"  -> Đã tạo: {app_id}_logo_gray.png (Grayscale Splash)")
        print(f"  -> Đã tạo: {app_id}.ico (Đa kích thước 16-256px)")
        
        # Sao chép vào thư mục của từng app
        for dest in dest_folders:
            if app_id in dest or (app_id == "geosolver_2d" and "geosolver" in dest and "3d" not in dest):
                img_512.save(os.path.join(dest, f"{app_id}_logo.png"), "PNG")
                img_gray_512.save(os.path.join(dest, f"{app_id}_logo_gray.png"), "PNG")
                img_512.save(os.path.join(dest, f"{app_id}.ico"), format="ICO", sizes=ico_sizes)
                if app_id == "geosolver_2d":
                    # Cập nhật luôn các icon MSIX & Windows app cũ của geosolver
                    img_512.resize((256, 256), Image.Resampling.LANCZOS).save(os.path.join(dest, "icon_256.png"))
                    img_512.resize((300, 300), Image.Resampling.LANCZOS).save(os.path.join(dest, "StoreLogo_300x300.png"))
                    img_512.resize((150, 150), Image.Resampling.LANCZOS).save(os.path.join(dest, "Square150x150Logo.png"))
                    img_512.save(os.path.join(dest, "app.ico"), format="ICO", sizes=ico_sizes)
                print(f"  -> Đồng bộ vào {dest}/")

    print("\n[HOÀN TẤT] Tất cả các biểu tượng đã được tái tạo ở độ phân giải 2048x2048 siêu sắc nét!")

if __name__ == "__main__":
    export_all_premium()
