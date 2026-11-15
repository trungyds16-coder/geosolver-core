import re

with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace version and titles
code = code.replace('CAD Math Studio v2.3', 'CAD Math Studio Pro v2.4')
code = code.replace('CAD MATH STUDIO v2.3', 'CAD MATH STUDIO PRO v2.4')
code = code.replace('Version: 2.3 (Enterprise Release)', 'Version: 2.4 (Pro Edition)')
code = code.replace('Phiên bản: 2.1', 'Phiên bản: 2.4 (Bản Pro)')

# Update toolbar buttons
code = code.replace('text=self._s("Xuất báo cáo", "Export Report"),', 'text=self._s("🖨️ In ấn / Báo cáo (Ctrl+P)", "🖨️ Print / Report (Ctrl+P)"),')
code = code.replace('text=self._s("Cấu hình", "Settings"),', 'text=self._s("⚙️ Kết nối AI", "⚙️ AI Connect"),')
code = code.replace('text=self._s("AI giải toán (F5)", "AI Solve (F5)"),', 'text=self._s("⚡ AI giải toán (F5)", "⚡ AI Solve (F5)"),')

# Update menu labels
code = code.replace('"Export HTML / Print Report... (Ctrl+P)" if is_en else "Xuất báo cáo HTML / In ấn... (Ctrl+P)"', '"Print Solution / Export HTML... (Ctrl+P)" if is_en else "In ấn bài giải / Xuất báo cáo... (Ctrl+P)"')
code = code.replace('"AI Settings" if is_en else "Cấu hình AI"', '"AI Connection Settings..." if is_en else "Cài đặt kết nối AI..."')

with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Update completed successfully!")
