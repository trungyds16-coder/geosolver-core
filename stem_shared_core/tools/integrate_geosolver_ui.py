# -*- coding: utf-8 -*-
"""
Công cụ tích hợp GeoSolver2DCore vào GeoSolver CAD Desktop
"""
import os

filepath = os.path.join(os.path.dirname(__file__), "..", "..", "geosolver", "geosolver_desktop.py")
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

import_target = "_AI_HUB_AVAILABLE = False"
import_repl = """_AI_HUB_AVAILABLE = False

# Import Lõi Hình học Phẳng độc lập (GeoSolver2DCore) đã qua thẩm định khoa học
try:
    from stem_shared_core.geosolver_core import (
        GeoSolver2DCore,
        MissingGeometricNodeError,
        DegenerateGeometryError,
        OutOfBoundsError
    )
    _GEOSOLVER_CORE_AVAILABLE = True
except Exception:
    _GEOSOLVER_CORE_AVAILABLE = False
    GeoSolver2DCore = None"""

if import_target in content and "_GEOSOLVER_CORE_AVAILABLE" not in content:
    content = content.replace(import_target, import_repl, 1)
    print("1. Đã chèn import GeoSolver2DCore.")

init_target = 'self.title("GeoSolver 2D CAD Studio")'
init_repl = """self.title("GeoSolver 2D CAD Studio")

        # Tích hợp lõi hình học độc lập đã qua thẩm định khoa học
        self.geo_engine = GeoSolver2DCore() if _GEOSOLVER_CORE_AVAILABLE and GeoSolver2DCore is not None else None"""

if init_target in content and "self.geo_engine =" not in content:
    content = content.replace(init_target, init_repl, 1)
    print("2. Đã khởi tạo self.geo_engine trong GeoSolverApp.__init__.")

screen_target = """    def to_screen(self, x, y):

        return self.origin_x + x * self.scale, self.origin_y - y * self.scale



    def to_world(self, px, py):

        return (px - self.origin_x) / self.scale, (self.origin_y - py) / self.scale"""

screen_repl = """    def to_screen(self, x, y):

        if getattr(self, 'geo_engine', None) is not None:
            return self.geo_engine.cartesian_to_canvas((x, y), (self.origin_x, self.origin_y), self.scale, flip_y=True)
        return self.origin_x + x * self.scale, self.origin_y - y * self.scale



    def to_world(self, px, py):

        if getattr(self, 'geo_engine', None) is not None:
            return self.geo_engine.canvas_to_cartesian((px, py), (self.origin_x, self.origin_y), self.scale, flip_y=True)
        return (px - self.origin_x) / self.scale, (self.origin_y - py) / self.scale"""

if screen_target in content:
    content = content.replace(screen_target, screen_repl, 1)
    print("3. Đã ủy quyền to_screen / to_world cho GeoSolver2DCore.")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Tích hợp hoàn tất thành công!")
