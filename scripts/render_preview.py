#!/usr/bin/env python3
"""交付物渲染预览：office 文档 → PDF → 逐页 PNG（多后端，探测优先）。

视觉验收必须"真渲染"才能发现溢出/错位。但**渲染器不必是 LibreOffice**：
本机已有的 PowerPoint / Word / WPS 同样能导出真实效果，且对自家格式往往更忠实
（pptx 引擎自己也指出：LibreOffice 会替换缺失字体，其"溢出与否"的判断可能与
真实 PowerPoint 不一致）。

因此本脚本**先探测本机已有渲染器**，按格式选最忠实的那个；**都没有**才提示安装
LibreOffice。不要为了"必须用 LibreOffice"而让用户白下几百 MB。

后端优先级（auto）：
  .pptx ： PowerPoint → WPS 演示(KWPP) → LibreOffice(soffice)
  .docx ： Word → WPS 文字(KWPS) → LibreOffice(soffice)
  .pdf  ： 无需转换
所有后端统一先产 PDF，再用 pymupdf 逐页栅格化（免装 poppler）。

用法：
    python render_preview.py <file.pptx|docx|pdf> [--outdir DIR] [--dpi 150]
    python render_preview.py --list                 # 只探测并列出可用后端
    python render_preview.py <file> --backend powerpoint
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

SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice", "/usr/local/bin/soffice",
]

# COM ProgID → 说明；pptx 与 docx 各自的首选与备选
COM_BACKENDS = {
    "powerpoint": "PowerPoint.Application",
    "word": "Word.Application",
    "wps-presentation": "KWPP.Application",
    "wps-writer": "KWPS.Application",
}

# 各格式的后端优先级：本机原生渲染器优先，LibreOffice 兜底
ORDER = {
    ".pptx": ["powerpoint", "wps-presentation", "soffice"],
    ".docx": ["word", "wps-writer", "soffice"],
    ".pdf": [],
}

_com = None
_avail_cache = {}


def _win32com():
    global _com
    if _com is None:
        try:
            import win32com.client  # noqa
            _com = win32com.client
        except Exception:
            _com = False
    return _com or None


def soffice_path():
    p = shutil.which("soffice")
    if p:
        return p
    for c in SOFFICE_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def available(backend):
    if backend in _avail_cache:
        return _avail_cache[backend]
    if backend == "soffice":
        ok = soffice_path() is not None
    else:
        com = _win32com()
        ok = False
        if com:
            try:
                com.Dispatch(COM_BACKENDS[backend])
                ok = True
            except Exception:
                ok = False
    _avail_cache[backend] = ok
    return ok


def pick_backend(src, forced=None):
    if forced and forced != "auto":
        if not available(forced):
            sys.exit(f"指定的后端 {forced} 不可用。用 --list 查看可用项。")
        return forced
    for b in ORDER.get(src.suffix.lower(), []):
        if available(b):
            return b
    return None


# ── 各后端 → PDF ────────────────────────────────────────────────────────
def _com_to_pdf(progid, src, pdf, saveas_fmt):
    com = _win32com()
    app = com.Dispatch(progid)
    try:
        if progid == "PowerPoint.Application":
            doc = app.Presentations.Open(str(src.resolve()), ReadOnly=True, WithWindow=False)
            try:
                doc.SaveAs(str(pdf.resolve()), saveas_fmt)
            finally:
                doc.Close()
        else:                                   # Word / WPS 文字
            try:
                app.Visible = False
            except Exception:
                pass
            doc = app.Documents.Open(str(src.resolve()), ReadOnly=True)
            try:
                doc.SaveAs(str(pdf.resolve()), saveas_fmt)
            finally:
                doc.Close(False)
    finally:
        try:
            app.Quit()
        except Exception:
            pass


def to_pdf(src, outdir, backend):
    if src.suffix.lower() == ".pdf":
        return src
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = outdir / (src.stem + ".pdf")
    if backend == "soffice":
        profile = tempfile.mkdtemp(prefix="soffice_").replace("\\", "/")
        cmd = [soffice_path(), "--headless", "--norestore",
               f"-env:UserInstallation=file:///{profile}",
               "--convert-to", "pdf", "--outdir", str(outdir), str(src)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif backend == "powerpoint":
        _com_to_pdf("PowerPoint.Application", src, pdf, 32)   # ppSaveAsPDF
    elif backend == "wps-presentation":
        _com_to_pdf("KWPP.Application", src, pdf, 32)
    elif backend == "word":
        _com_to_pdf("Word.Application", src, pdf, 17)         # wdFormatPDF
    elif backend == "wps-writer":
        _com_to_pdf("KWPS.Application", src, pdf, 17)
    else:
        sys.exit(f"未知后端：{backend}")
    if not pdf.exists():
        sys.exit(f"后端 {backend} 未能生成 PDF：{pdf}")
    return pdf


def pdf_to_pngs(pdf, outdir, dpi):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(str(pdf))
    paths = []
    for i, page in enumerate(doc, 1):
        p = outdir / f"{pdf.stem}_p{i:02d}.png"
        page.get_pixmap(dpi=dpi).save(str(p))
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", help="待渲染文件")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--backend", default="auto",
                    help="auto | powerpoint | word | wps-presentation | wps-writer | soffice")
    ap.add_argument("--list", action="store_true", help="只探测可用后端")
    a = ap.parse_args()

    if a.list or not a.path:
        print("可用渲染后端：")
        for b in ("powerpoint", "word", "wps-presentation", "wps-writer", "soffice"):
            print(f"  {'✓' if available(b) else '✗'} {b}")
        return 0 if a.list else 2

    src = Path(a.path)
    if not src.exists():
        sys.exit(f"文件不存在：{src}")

    backend = pick_backend(src, a.backend)
    if backend is None:
        sys.exit(
            "本机未找到可用渲染器（PowerPoint / WPS / LibreOffice 都没有）。\n"
            "视觉验收需要真渲染，请任选其一安装：\n"
            "  - 已装 Office 或 WPS → 直接可用（无需额外安装）\n"
            "  - 都没有 → 安装 LibreOffice："
            "https://mirrors.tuna.tsinghua.edu.cn/libreoffice/libreoffice/stable/")

    outdir = Path(a.outdir) if a.outdir else src.parent / f"preview_{src.stem}"
    outdir.mkdir(parents=True, exist_ok=True)

    pdf = to_pdf(src, outdir, backend)
    pngs = pdf_to_pngs(pdf, outdir, a.dpi)
    print(f"# 后端={backend}  {len(pngs)} 页 → {outdir}")
    for p in pngs:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
