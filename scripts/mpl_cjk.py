#!/usr/bin/env python3
"""matplotlib 中文字体设置。

固化坑：老版本 matplotlib 没有 `addfont`，直接用字体名会 fallback 成方框；
可靠做法是用 `FontProperties(fname=...msyh.ttc)` 注册真实字体文件。

用法：
    import mpl_cjk; mpl_cjk.setup()
    python mpl_cjk.py --self-test        # 找到字体并渲染一张测试图
"""
import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",     # 微软雅黑
    r"C:\Windows\Fonts\msyh.ttf",
    r"C:\Windows\Fonts\simhei.ttf",   # 黑体
    r"C:\Windows\Fonts\simsun.ttc",   # 宋体
    r"/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",     # 文泉驿（Debian/Ubuntu 常见）
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]


def find_font(font_file=None):
    if font_file and Path(font_file).exists():
        return font_file
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    return None


def setup(font_file=None, base=None):
    """返回实际使用的字体名。base=图片尺寸/字体名等可选覆盖。"""
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import font_manager, rcParams

    path = find_font(font_file)
    name = "sans-serif"
    if path:
        try:
            if hasattr(font_manager.fontManager, "addfont"):
                font_manager.fontManager.addfont(path)
            name = font_manager.FontProperties(fname=path).get_name()
        except Exception:
            fp = font_manager.FontProperties(fname=path)  # 兜底：直接给 FontProperties
            name = fp.get_name()
    else:
        # 不要静默降级：没字体时中文会变成方块，而这是最难自查的一类错
        print("⚠ mpl_cjk：未找到中文字体文件（已试 微软雅黑/黑体/宋体/PingFang/Noto CJK）。"
              "图表中的中文很可能渲染成方块（□）。请安装一款中文字体，"
              "或用 --font-file 指定 .ttf/.ttc 路径。", file=sys.stderr)
    rcParams["font.sans-serif"] = [name, "Microsoft YaHei", "SimHei",
                                   "PingFang SC", "Noto Sans CJK SC", "sans-serif"]
    rcParams["axes.unicode_minus"] = False             # 负号别用成方块
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--font-file", default=None)
    ap.add_argument("--out", default="mpl_cjk_test.png")
    a = ap.parse_args()
    if not a.self_test:
        print(__doc__)
        return 0
    name = setup(a.font_file)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_title("中文标题：分频器实测偏差 -4.6%")
    ax.plot([0, 1, 2], [0, 1, 0.5])
    ax.set_xlabel("时间 / ms")
    fig.tight_layout()
    fig.savefig(a.out, dpi=120)
    print(f"字体：{name}")
    print(f"测试图：{a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
