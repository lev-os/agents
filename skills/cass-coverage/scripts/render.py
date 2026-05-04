#!/usr/bin/env python3
"""Render: copy viewer/dashboard.html into output dir + place coverage.json next to it.

Usage:
    python3 render.py --coverage <coverage.json> --output-dir <dir>

The output dir gets:
    dashboard.html  (copy of viewer/dashboard.html)
    coverage.json   (copy of input — viewer fetches this)
"""
import argparse, shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage", required=True, help="path to coverage.json")
    ap.add_argument("--output-dir", required=True, help="output directory (will be created)")
    ap.add_argument("--viewer", default=None, help="override viewer path (default: ../viewer/dashboard.html relative to script)")
    args = ap.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    viewer = Path(args.viewer) if args.viewer else Path(__file__).resolve().parent.parent / "viewer" / "dashboard.html"
    if not viewer.exists():
        raise SystemExit(f"viewer not found at {viewer}")

    shutil.copy2(viewer, out / "dashboard.html")
    cov_dst = out / "coverage.json"
    cov_src = Path(args.coverage).resolve()
    if cov_src != cov_dst.resolve():
        shutil.copy2(args.coverage, cov_dst)

    # Also emit coverage.js for file:// loading (browsers block fetch() on file://)
    cov_text = (out / "coverage.json").read_text()
    (out / "coverage.js").write_text(f"window.__COVERAGE = {cov_text};\n")

    dash_size = (out / "dashboard.html").stat().st_size
    cov_size = (out / "coverage.json").stat().st_size
    js_size = (out / "coverage.js").stat().st_size
    print(f"rendered → {out}/")
    print(f"  dashboard.html  {dash_size//1024} KB")
    print(f"  coverage.json   {cov_size//1024} KB  (canonical artifact)")
    print(f"  coverage.js     {js_size//1024} KB  (file:// loader)")
    print(f"open: file://{out.resolve()}/dashboard.html")


if __name__ == "__main__":
    main()
