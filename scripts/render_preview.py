#!/usr/bin/env python3
"""交付物渲染预览：office 文档 → PDF → 逐页 PNG。

供三路线视觉验收复用（省去每次现写 soffice / 渲染命令）。
生成的页图交给 `engines/visual-judge.md` 或人工自查。

用法：
    python render_preview.py <file.pptx|docx|pdf> [--outdir DIR] [--dpi 150]

stdout 每行输出一个 PNG 绝对路径（按页序）。
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def _soffice():
    return shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"


def to_pdf(src, outdir):
    if src.suffix.lower() == ".pdf":
        return src
    profile = tempfile.mkdtemp(prefix="soffice_").replace("\\", "/")
    cmd = [_soffice(), "--headless", "--norestore",
           f"-env:UserInstallation=file:///{profile}",
           "--convert-to", "pdf", "--outdir", str(outdir), str(src)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = outdir / (src.stem + ".pdf")
    if not pdf.exists():
        sys.exit(f"soffice 未能生成 PDF：{pdf}")
    return pdf


def pdf_to_pngs(pdf, outdir, dpi):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(str(pdf))
    paths = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=dpi)
        p = outdir / f"{pdf.stem}_p{i:02d}.png"
        pix.save(str(p))
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args()

    src = Path(a.path)
    if not src.exists():
        sys.exit(f"文件不存在：{src}")
    outdir = Path(a.outdir) if a.outdir else src.parent / f"preview_{src.stem}"
    outdir.mkdir(parents=True, exist_ok=True)

    pdf = to_pdf(src, outdir)
    pngs = pdf_to_pngs(pdf, outdir, a.dpi)
    print(f"# {len(pngs)} 页 → {outdir}")
    for p in pngs:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
