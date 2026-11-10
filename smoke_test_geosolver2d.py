import os
import sys
import json
import hashlib
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

def run_smoke():
    results = {}
    print("=== GEOSOLVER 2D v3.1 RC5 SMOKE TEST ===")

    # 1. Geometry 2D Kernel
    try:
        from geosolver.geosolver_desktop import classify_triangle
        res1 = classify_triangle({"name": "A", "x": 0, "y": 0, "source": "typed", "exact": True},
                                 {"name": "B", "x": 4, "y": 0, "source": "typed", "exact": True},
                                 {"name": "C", "x": 0, "y": 3, "source": "typed", "exact": True})
        assert res1["type"] == "right" and res1["vertex"] == "A"
        results["geometry2d_kernel"] = True
        print("[OK] geometry2d_kernel")
    except Exception as e:
        results["geometry2d_kernel"] = False
        print(f"[FAIL] geometry2d_kernel: {e}")

    # 2. Taint Tracking Propagation
    try:
        from geosolver.geosolver_desktop import _point_flag
        pFree = {"name": "P", "x": 1.23, "y": 4.56, "source": "dragged", "exact": False}
        pTyped = {"name": "Q", "x": 0.0, "y": 0.0, "source": "typed", "exact": True}
        pMid = {"name": "M", "x": 0.615, "y": 2.28, "source": "midpoint", "parents": [pFree, pTyped]}
        assert _point_flag(pMid) is False
        results["taint_tracking"] = True
        print("[OK] taint_tracking")
    except Exception as e:
        results["taint_tracking"] = False
        print(f"[FAIL] taint_tracking: {e}")

    # 3. SymPy Engine
    try:
        import sympy as sp
        x = sp.Symbol('x')
        sol = sp.solve(x**2 - 4, x)
        assert len(sol) == 2
        results["sympy"] = True
        print("[OK] sympy")
    except Exception as e:
        results["sympy"] = False
        print(f"[FAIL] sympy: {e}")

    # 4. Tkinter GUI Runtime
    try:
        from geosolver.geosolver_desktop import GeoSolverApp
        app = GeoSolverApp(with_splash=False)
        app.update()
        app.destroy()
        results["tkinter_runtime"] = True
        print("[OK] tkinter_runtime")
    except Exception as e:
        results["tkinter_runtime"] = False
        print(f"[FAIL] tkinter_runtime: {e}")

    # 5. DPAPI KeyStore (Windows only)
    try:
        from stem_shared_core.ai_local_manager import GeminiKeyStore
        tmp_key = Path(os.environ.get("LOCALAPPDATA", ".")) / "GeoSolver" / "test_smoke_key.txt"
        store = GeminiKeyStore(tmp_key)
        store.save("AIzaSySmokeTestSecretKey123")
        read_val = store.read()
        assert read_val == "AIzaSySmokeTestSecretKey123"
        if tmp_key.is_file():
            tmp_key.unlink()
        results["dpapi_keystore"] = True
        print("[OK] dpapi_keystore")
    except Exception as e:
        results["dpapi_keystore"] = False
        print(f"[FAIL] dpapi_keystore: {e}")

    # 6. SSL / Certifi Validation
    try:
        import certifi
        cafile = certifi.where()
        assert os.path.exists(cafile)
        ctx = ssl.create_default_context(cafile=cafile)
        req = urllib.request.Request("https://generativelanguage.googleapis.com", headers={"User-Agent": "GeoSolver2D-SmokeTest"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                pass
        except urllib.error.HTTPError as he:
            # 404/403 means SSL handshake was 100% successful
            pass
        results["ssl_certifi"] = True
        print("[OK] ssl_certifi")
    except Exception as e:
        results["ssl_certifi"] = False
        print(f"[FAIL] ssl_certifi: {e}")

    # Hash executable
    exe_path = sys.executable
    with open(exe_path, "rb") as f:
        exe_hash = hashlib.sha256(f.read()).hexdigest().upper()

    all_pass = all(results.values())
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "frozen": getattr(sys, "frozen", False),
        "python_version": sys.version,
        "executable": exe_path,
        "executable_sha256": exe_hash,
        "checks": results,
        "status": "PASS" if all_pass else "FAIL",
        "exit_code": 0 if all_pass else 1
    }

    with open("smoke_test_result_geosolver2d.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nFinal Smoke Test Status: {summary['status']} (Exit Code {summary['exit_code']})")
    sys.exit(summary["exit_code"])

if __name__ == "__main__":
    run_smoke()
