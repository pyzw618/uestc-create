# scripts/

确定性作业的固化脚本（`ROADMAP` 原则 5 的例外：反复踩的坑与可复用机械流程收进来，
写作/分析类一律不脚本化）。每个脚本都编码了一个**真实踩过的坑**。

| 脚本 | 作用 | 编码的坑 | 被谁用 |
|---|---|---|---|
| `cjk.py` | 一次性设好 pptx 的 `a:ea` / docx 的 `w:eastAsia` 中文字体 | pptx 设 `w:eastAsia` 完全无效；中文走默认字体 | A / B / C 生成后 |
| `mpl_cjk.py` | matplotlib 中文字体注册 | 老版本无 `addfont`，字体名 fallback 成方块 | A 图表页 |
| `pptx_bg.py` | 克隆 `<p:bg>` 背景并重绑图片关系 | 直接复制 rId 在目标页解析不到，背景丢失 | A1 官方模板轨 |
| `pptx_qa.py` | 遍历查占位符/越界/溢出估算/文本重叠 | 每次现写遍历代码、口径不一 | A 验收 |
| `render_preview.py` | office → PDF → 逐页 PNG（**多后端探测**：PowerPoint/Word/WPS/LibreOffice） | 每次现写渲染命令；且误把 LibreOffice 当唯一渲染器 | A / B / C 视觉验收 |

## 运行环境

依赖：`python-pptx`、`python-docx`、`pymupdf`；渲染需要一个渲染器——**本机 PowerPoint/Word/WPS（Windows 经 `pywin32`）或 LibreOffice**，`render_preview.py` 会自动探测并选最忠实的一个。
本机开发环境：conda `py12`（Python 3.10）。CLAUDE.md 约定按需选/建环境。

## 说明

- 这些脚本是**机械辅助**，不替 agent 做判断；生成主流程仍按各 workflow 运行时内联写代码。
- 内容类检查（禁用词/占位符/个人信息）也收在 `evals/check_deliverable.py`，与工作流验收步对接。
- 修改脚本后请用真实产物回归（见各脚本 `--help` 与 `README` 用法）。
