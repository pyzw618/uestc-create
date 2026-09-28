#!/usr/bin/env python3
"""uestc-create 交付物机检（纯标准库，无需第三方依赖）。

对 .docx / .pptx 抽取文本，跑客观断言：占位符残留、禁用词、模糊数字词、
个人信息、emoji、单页密度。把"自评 checklist"里可机验的部分自动化。

用法：
    python check_deliverable.py <file.docx|file.pptx> [--json] [--max-chars N]

退出码：0 = 无 hard fail；1 = 有 hard fail。
只做客观判定；视觉效果、叙事质量等主观项仍走 checklist 与 visual-judge。
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

# Windows 默认 GBK 无法输出 ✓/✗ 等字符，强制 stdout/stderr 走 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 断言表（来源：references/writing-style.md §1.4 与各路线 checklist）──

# 占位符残留：出现即 fail
PLACEHOLDERS = [
    (r"队名\s*[:：]\s*(?:$|\s)", "队名占位未填"),
    (r"队员\s*[:：]\s*(?:$|\s)", "队员占位未填"),
    (r"\b[xX]{3,}\b", "xxx 占位"),
    (r"\bTODO\b", "TODO 残留"),
    (r"待补(?:充|写)?", "待补残留"),
    (r"待填写", "待填写残留"),
    (r"Click to add", "PPT 模板占位符未填"),
    (r"^\s*[<＜]\s*[>＞]\s*$", "空占位尖括号"),
]

# 禁用词：cap = 全文允许次数；超过即 fail
BANNED_CAPPED = [
    (r"综上所述", 1, "综上所述（结论处 ≤1 次）"),
    (r"总而言之", 1, "总而言之（≤1 次）"),
    (r"不难发现", 0, "不难发现"),
    (r"由此可见", 0, "由此可见"),
    (r"具有重要意义", 0, "具有重要意义"),
    (r"有力支撑", 0, "为……提供了有力支撑"),
    (r"随着.{0,12}不断发展", 0, "随着……的不断发展"),
    (r"迈上了?新台阶", 0, "迈上新台阶"),
    (r"赋能", 0, "赋能（报告文学腔）"),
    (r"抓手", 0, "抓手（报告文学腔）"),
    (r"深度融合", 0, "深度融合（报告文学腔）"),
    (r"全方位", 0, "全方位"),
    (r"层次化|体系化", 0, "层次化/体系化（除非确有所指）"),
]

# 闭环：工程语境合法，只在非"闭环控制/闭环反馈/闭环回路"时计
CLOSED_LOOP = (r"闭环", r"闭环(?:控制|反馈|回路|调节)", "闭环（非工程语境）")

# 模糊数字词：出现即 fail（必须落到具体数字）
VAGUE = [
    (r"明显(?:提升|提高|改善|增强)", "“明显提升”类模糊表述"),
    (r"显著(?:提升|提高|改善|增强|优于)", "“显著改善”类模糊表述"),
    (r"效果(?:很好|不错|理想)", "“效果很好”类主观表述"),
]

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)
STUDENT_ID = re.compile(r"\b20\d{9,12}\b")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CJK = re.compile(r"[一-鿿]")


def _docx_blocks(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    # 以段落切分，去标签
    paras = re.split(r"</w:p>", xml)
    out = []
    for p in paras:
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        text = re.sub(r"<[^>]+>", "", text)
        if text.strip():
            out.append(text)
    return out or [re.sub(r"<[^>]+>", "", xml)]


def _pptx_blocks(path):
    with zipfile.ZipFile(path) as z:
        names = sorted(
            (n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        out = []
        for n in names:
            xml = z.read(n).decode("utf-8", errors="replace")
            text = "".join(re.findall(r"<a:t>(.*?)</a:t>", xml, re.S))
            out.append(re.sub(r"<[^>]+>", "", text))
    return out


def extract(path):
    suffix = path.suffix.lower()
    if suffix == ".docx":
        blocks = _docx_blocks(path)
    elif suffix == ".pptx":
        blocks = _pptx_blocks(path)
    else:
        raise SystemExit(f"仅支持 .docx / .pptx，收到：{suffix}")
    return "\n".join(blocks), blocks


def check(path: Path, max_chars: int) -> dict:
    full, blocks = extract(path)
    hard, warn = [], []

    for pat, msg in PLACEHOLDERS:
        hits = re.findall(pat, full, re.M)
        if hits:
            hard.append({"check": "占位符", "issue": msg, "count": len(hits)})

    for pat, cap, msg in BANNED_CAPPED:
        n = len(re.findall(pat, full))
        if n > cap:
            hard.append({"check": "禁用词", "issue": msg, "count": n, "cap": cap})

    pat, allow, msg = CLOSED_LOOP
    n_bad = len(re.findall(pat, full)) - len(re.findall(allow, full))
    if n_bad > 0:
        hard.append({"check": "禁用词", "issue": msg, "count": n_bad, "cap": 0})

    for pat, msg in VAGUE:
        n = len(re.findall(pat, full))
        if n:
            hard.append({"check": "模糊数字", "issue": msg, "count": n})

    ids = STUDENT_ID.findall(full)
    if ids:
        hard.append({"check": "个人信息", "issue": "疑似学号", "samples": ids[:3]})
    emails = [e for e in EMAIL.findall(full) if "std.uestc" in e or "qq.com" in e]
    if emails:
        warn.append({"check": "个人信息", "issue": "疑似邮箱（确认非示例）", "samples": emails[:3]})

    emo = EMOJI.findall(full)
    if emo:
        warn.append({"check": "形态", "issue": "正文出现 emoji", "count": len(emo)})

    over = []
    for i, b in enumerate(blocks, 1):
        n = len(CJK.findall(b))
        if n > max_chars:
            over.append({"block": i, "chars": n})
    if over:
        warn.append({
            "check": "密度", "issue": f"单块汉字数 > {max_chars}（为宜非硬限，需讲稿支撑）",
            "blocks": over[:5],
        })

    return {
        "file": str(path),
        "blocks": len(blocks),
        "cjk_total": len(CJK.findall(full)),
        "hard_fail": hard,
        "warn": warn,
        "pass": not hard,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="uestc-create 交付物机检")
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--max-chars", type=int, default=330,
                    help="单页/单段汉字数上限（PPT 正文默认 330，论文可调大）")
    a = ap.parse_args()

    p = Path(a.path)
    if not p.exists():
        print(f"文件不存在：{p}", file=sys.stderr)
        return 2

    r = check(p, a.max_chars)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"文件：{r['file']}  块数：{r['blocks']}  汉字：{r['cjk_total']}")
        if r["hard_fail"]:
            print(f"✗ hard fail（{len(r['hard_fail'])}）：")
            for h in r["hard_fail"]:
                print(f"  - [{h['check']}] {h['issue']} ×{h.get('count', 1)}")
        else:
            print("✓ 无 hard fail")
        for w in r["warn"]:
            print(f"  ! [{w['check']}] {w['issue']} ×{w.get('count', 1)}")
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
