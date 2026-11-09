# -*- coding: utf-8 -*-
"""
Gộp TRANSLATIONS (cad_math_v2) và LANG_DATA (geosolver_desktop) vào vi.json / en.json.

Chạy (trong thư mục stem_shared_core):
    python tools/migrate_i18n.py --cad "D:\\AI DATA\\STEM_APP\\cad_math_v2\\cad_math_v2.py" ^
                                 --geo "D:\\AI DATA\\STEM_APP\\geosolver_desktop\\geosolver_desktop.py"

Script đọc file nguồn bằng ast (KHÔNG chạy code của app), tìm biến gán ở mức module, rồi
literal_eval. Hỗ trợ 2 dạng cấu trúc:
    {"vi": {"key": "..."}, "en": {"key": "..."}}        (theo ngôn ngữ)
    {"key": {"vi": "...", "en": "..."}}                  (theo key)
Key được thêm tiền tố "cad." / "geo." để tránh trùng. Sau khi chạy sẽ có báo cáo key thiếu bản dịch.
Dùng --dry-run để xem trước, --keep để không ghi đè key đã có.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

LOCALES = Path(__file__).resolve().parent.parent / "i18n" / "locales"
ALIASES = {"vi": "vi", "vn": "vi", "vi_vn": "vi", "vi-vn": "vi",
           "en": "en", "en_us": "en", "en-us": "en", "eng": "en"}


def load_literal(py_file: Path, var_name: str) -> Optional[Any]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
    for node in tree.body:
        targets = []
        value = None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        for tg in targets:
            if isinstance(tg, ast.Name) and tg.id == var_name:
                try:
                    return ast.literal_eval(value)
                except ValueError as exc:
                    print(f"[!] {var_name} trong {py_file.name} có biểu thức không phải literal: {exc}")
                    return None
    print(f"[!] Không tìm thấy biến {var_name} trong {py_file}")
    return None


def flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    else:
        out[prefix] = obj
    return out


def split_by_language(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Trả về {"vi": {key: text}, "en": {key: text}} cho cả hai dạng cấu trúc."""
    result: Dict[str, Dict[str, Any]] = {"vi": {}, "en": {}}
    top_langs = {k for k in data if str(k).lower() in ALIASES}
    if top_langs and len(top_langs) == len(data):  # dạng theo ngôn ngữ
        for lang_key, sub in data.items():
            result[ALIASES[str(lang_key).lower()]].update(flatten(sub))
        return result
    for key, sub in flatten(data).items():          # dạng theo key: "<key>.<lang>"
        head, _, tail = key.rpartition(".")
        if tail.lower() in ALIASES and head:
            result[ALIASES[tail.lower()]][head] = sub
        else:
            print(f"[?] Bỏ qua key không nhận ra ngôn ngữ: {key}")
    return result


def merge_into(locale_file: Path, new_flat: Dict[str, Any], keep: bool) -> int:
    data = json.loads(locale_file.read_text(encoding="utf-8")) if locale_file.exists() else {}
    flat_existing = flatten({k: v for k, v in data.items() if not k.startswith("_")})
    added = 0
    for key, val in new_flat.items():
        if keep and key in flat_existing:
            continue
        flat_existing[key] = val
        added += 1
    out: Dict[str, Any] = {k: v for k, v in data.items() if k.startswith("_")}
    for key, val in sorted(flat_existing.items()):   # dựng lại JSON lồng nhau
        node = out
        parts = key.split(".")
        for p in parts[:-1]:
            nxt = node.get(p)
            if not isinstance(nxt, dict):          # key "a" vừa là chuỗi vừa là nhóm -> giữ dạng phẳng
                nxt = node[p] = {}
            node = nxt
        node[parts[-1]] = val
    return added, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cad", type=Path, help="file .py chứa TRANSLATIONS")
    ap.add_argument("--geo", type=Path, help="file .py chứa LANG_DATA")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep", action="store_true", help="không ghi đè key đã có")
    args = ap.parse_args()

    sources = []
    if args.cad:
        sources.append(("cad", args.cad, "TRANSLATIONS"))
    if args.geo:
        sources.append(("geo", args.geo, "LANG_DATA"))
    if not sources:
        ap.error("cần ít nhất --cad hoặc --geo")

    collected: Dict[str, Dict[str, Any]] = {"vi": {}, "en": {}}
    for prefix, path, var in sources:
        raw = load_literal(path, var)
        if not isinstance(raw, dict):
            continue
        parts = split_by_language(raw)
        for lang in ("vi", "en"):
            for k, v in parts[lang].items():
                collected[lang][f"{prefix}.{k}"] = v
        print(f"[{prefix}] vi={len(parts['vi'])} key, en={len(parts['en'])} key")

    only_vi = sorted(set(collected["vi"]) - set(collected["en"]))
    only_en = sorted(set(collected["en"]) - set(collected["vi"]))
    if only_vi:
        print(f"\n[!] {len(only_vi)} key có tiếng Việt nhưng THIẾU tiếng Anh (sẽ fallback), ví dụ: {only_vi[:8]}")
    if only_en:
        print(f"[!] {len(only_en)} key có tiếng Anh nhưng thiếu tiếng Việt, ví dụ: {only_en[:8]}")

    for lang in ("vi", "en"):
        added, merged = merge_into(LOCALES / f"{lang}.json", collected[lang], args.keep)
        if args.dry_run:
            print(f"[dry-run] {lang}.json: sẽ thêm/cập nhật {added} key")
        else:
            (LOCALES / f"{lang}.json").write_text(
                json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{lang}.json: thêm/cập nhật {added} key")
    print("\nLưu ý: chuỗi có dấu { } hoặc %s kiểu cũ cần đổi sang {tên_biến} nếu truyền kwargs vào t().")
    return 0


if __name__ == "__main__":
    sys.exit(main())
