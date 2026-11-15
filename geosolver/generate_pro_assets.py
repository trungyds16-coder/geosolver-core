# -*- coding: utf-8 -*-
"""
GeoSolver 2D CAD Pro - Bộ Tạo Icon & Tài Nguyên Thương Hiệu Bản Pro
Tạo icon có huy hiệu 'PRO' bo góc nhỏ gọn ở góc trên bên phải của icon gốc.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def generate_pro_icons():
    src_logo = os.path.join(ASSETS_DIR, "geosolver_2d_logo.png")
    if not os.path.exists(src_logo):
        src_logo = os.path.join(ASSETS_DIR, "icon_256.png")
    
    base = Image.open(src_logo).convert("RGBA")
    W, H = 512, 512
    base = base.resize((W, H), Image.Resampling.LANCZOS)
    
    # 2x supersampling for high fidelity
    scale = 2
    canvas = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    canvas.paste(base.resize((W * scale, H * scale), Image.Resampling.LANCZOS), (0, 0))
    
    # Compact rounded badge in top-right corner
    bw = int(144 * scale)
    bh = int(66 * scale)
    bx2 = int(486 * scale)
    bx1 = bx2 - bw
    by1 = int(24 * scale)
    by2 = by1 + bh
    radius = int(22 * scale)
    
    badge_layer = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge_layer)
    
    # Drop shadow
    shadow_offset = int(4 * scale)
    draw.rounded_rectangle(
        [bx1, by1 + shadow_offset, bx2, by2 + shadow_offset],
        radius=radius,
        fill=(0, 0, 0, 95)
    )
    
    # Gold Gradient Fill
    badge_img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge_img)
    for i in range(bh):
        t = i / float(bh)
        r = int(251 * (1 - t) + 217 * t)  # #FBBF24 to #D97706
        g = int(191 * (1 - t) + 119 * t)
        b = int(36 * (1 - t) + 6 * t)
        b_draw.line([(0, i), (bw, i)], fill=(r, g, b, 255))
        
    mask = Image.new("L", (bw, bh), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=radius, fill=255)
    badge_layer.paste(badge_img, (bx1, by1), mask=mask)
    
    # Outline Border
    draw.rounded_rectangle(
        [bx1, by1, bx2 - 1, by2 - 1],
        radius=radius,
        outline=(255, 255, 255, 230),
        width=int(2.5 * scale)
    )
    
    # 'PRO' Text
    try:
        font = ImageFont.truetype("segoeuib.ttf", int(37 * scale))
    except Exception:
        try:
            font = ImageFont.truetype("arialbd.ttf", int(37 * scale))
        except Exception:
            font = ImageFont.load_default()
            
    bbox = font.getbbox("PRO")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = bx1 + (bw - tw) // 2 - bbox[0]
    ty = by1 + (bh - th) // 2 - bbox[1]
    
    # Text shadow
    draw.text((tx + int(1.5 * scale), ty + int(1.5 * scale)), "PRO", fill=(146, 64, 14, 210), font=font)
    # Text main crisp white
    draw.text((tx, ty), "PRO", fill=(255, 255, 255, 255), font=font)
    
    # Merge layers
    final_2x = Image.alpha_composite(canvas, badge_layer)
    logo_pro_512 = final_2x.resize((W, H), Image.Resampling.LANCZOS)
    
    # 1. Save 512x512 logo
    out_logo_png = os.path.join(ASSETS_DIR, "geosolver_2d_logo_pro.png")
    logo_pro_512.save(out_logo_png, "PNG")
    print(f"✓ Đã tạo logo Pro: {out_logo_png}")
    
    # 2. Save .ico files (multi-size)
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    out_ico_2d = os.path.join(ASSETS_DIR, "geosolver_2d_pro.ico")
    logo_pro_512.save(out_ico_2d, format="ICO", sizes=ico_sizes)
    print(f"✓ Đã tạo icon Pro: {out_ico_2d}")
    
    out_ico_app = os.path.join(ASSETS_DIR, "app_pro.ico")
    logo_pro_512.save(out_ico_app, format="ICO", sizes=ico_sizes)
    print(f"✓ Đã tạo icon App Pro: {out_ico_app}")
    
    # 3. Save Store Logo Variants for Pro
    logo_pro_512.resize((150, 150), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "Square150x150Logo_pro.png"), "PNG")
    logo_pro_512.resize((44, 44), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "Square44x44Logo_pro.png"), "PNG")
    logo_pro_512.resize((50, 50), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "StoreLogo_pro.png"), "PNG")
    logo_pro_512.resize((300, 300), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "StoreLogo_300x300_pro.png"), "PNG")
    print("✓ Đã hoàn tất tạo toàn bộ bộ tài nguyên Store & Desktop Icon Pro!")

if __name__ == "__main__":
    generate_pro_icons()
