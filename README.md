# uestc-create

电子科技大学（成电）课程交付物技能包：**汇报 PPT / 实验报告 / 课程论文与课程设计报告 / 开题-中期-结题规划**。

面向"最后一公里"：实验怎么做、数据怎么分析、代码怎么写不归它管；它把已有成果变成合格的交付物。

## 安装

1. 把整个 `uestc-create/` 文件夹拷入所用 agent 的技能目录（如 `~/.agents/skills/` 或对应配置的 skills 路径），或按所用工具的方式注册该文件夹为技能。
2. 填写 `config/user.yaml`（姓名/学号/学院/专业）——首次使用可从 `config/user.yaml.example` 复制一份再填；留空则首次生成封面时会引导你填。该文件只在本机，已在 `.gitignore` 中忽略，随包分发时不会被带走。
3. 依赖（按需，缺什么装什么）：
   - Python 3 + `python-pptx`、`python-docx`、`Pillow`、`pypdf`、`matplotlib`、`pymupdf`（后两者供 `scripts/` 的图表与渲染）
   - 渲染器（.doc→.docx、文档→PDF、渲染预览）：**用本机已有的任一即可，无需额外安装**——Windows：PowerPoint / Word / WPS（原生渲染对自家格式更忠实）；Linux / macOS：LibreOffice。**一个都没有时**再装 [LibreOffice](https://mirrors.tuna.tsinghua.edu.cn/libreoffice/libreoffice/stable/)（清华镜像快）
   - TeX Live（XeLaTeX + latexmk，仅 LaTeX 论文需要；`assets/course-papers/latex/` 编译验证过）
   - Node.js + `pptxgenjs`（pptx 引擎的 JS 生成轨，可选；python-pptx 轨不需要）

## 使用示例

- 「把这篇论文做成 12 页中期答辩 PPT，用官方蓝模板」
- 「数电实验三的数据在 lab3.xlsx，按标准实验报告格式写报告」
- 「党史课期末论文，题目自选，3000 字」
- 「我下个月开题，帮我理一理要做哪些事」（只给规划，不产出文件）

## 目录结构

```
SKILL.md                总路由（先读这个）
config/user.yaml        你的信息（只存在本机）
workflows/              四条路线的工作流
references/             写作纪律(writing-style.md) + 各路线规范
scripts/                固化脚本（cjk / mpl_cjk / pptx_bg / pptx_qa / render_preview）
evals/                  机检与评测（check_deliverable / run_trigger_eval / grader）
assets/
  slides/templates/     8 套官方 PPT 模板
  slides/masters/       红/蓝/白风景/DIY 四套母版几何 JSON（其余 4 套无，走自由填充）
  slides/brand/         校徽/校标/院徽/线稿/银杏 等官方素材
  icons-charts/         图表 SVG 模板 ×33 + 精选图标 ×570
  course-papers/        论文/课设模板 + LaTeX 模板
  lab-report/           标准实验报告模板与版式参数
engines/
  docx/ pdf/ pptx/      三引擎（官方技能完整内容随包，轻量适配任意 agent）
  visual-judge.md       视觉验收提示词（子 agent 可派发；无子 agent 能力按其自查）
```

## 兼容性与平台

**Agent 兼容性**：内容与 agent 无关——不依赖任何宿主专属工具（无 Task/Skill/artifacts 之类调用）。子 agent 全程**可选**：视觉验收与独立打分处都写了"无子 agent 能力时按同一标准自查"的降级路径（`engines/visual-judge.md`、`evals/grader.md`）。
唯一前提：「技能被自动发现」依赖宿主具备 skill 机制（如 SKILL.md 约定）；在不具备该机制的框架或裸 API 下，内容同样可用，但需把 `SKILL.md` 显式交给模型。

**平台兼容性**：

| 项 | Windows | Linux / macOS |
|---|---|---|
| python 脚本（`scripts/`、`evals/`） | ✅ 已实测 | 静态审计通过，**未实机验证** |
| 渲染器 | PowerPoint / Word / WPS（经 `pywin32` COM） | LibreOffice（`soffice`） |
| 中文字体默认 | 微软雅黑 | Linux: Noto Sans CJK SC · macOS: PingFang SC |
| shell 脚本（`engines/*/env_check.sh`、`setup.sh`） | 需 Git Bash 或 WSL | ✅ 原生 bash |

渲染器是**探测式**的：`scripts/render_preview.py` 自动选本机最忠实的一个（原生渲染对自家格式更准），一个都没有时才提示安装 LibreOffice。缺中文字体时 `mpl_cjk.py` 会**显式告警**，不会静默渲染出方块。

> Linux / macOS 结论来自代码静态审计，未在相应系统上实跑。

## 验证与自检

- `evals/check_deliverable.py <file>`：纯标准库机检（占位符 / 禁用词 / 模糊数字词 / 个人信息 / emoji / 单块密度），有 hard fail 时返回非零。各路线 workflow 的验收步已接入。
- `evals/grader.md`：独立验收 agent 提示词（生成者≠裁判）；有子 agent 能力时派发。
- `evals/evals.json`、`evals/trigger-eval.json`：行为 eval 集与触发评测集（20 条 should/should-not）。
- `evals/run_trigger_eval.py`：Windows 可用的触发评测。上游 skill-creator 的 `run_eval.py` 用 `select()` 读管道，Windows 不支持（WinError 10038），故本包自带替代版。

## 素材与许可

| 内容 | 来源与许可 | 说明 |
|---|---|---|
| `engines/docx\|pdf\|pptx`、`engines/visual-judge.md` | 改造自 Z.AI 官方 documents/pdf/presentations 技能（v1.1 完整内容随包：routes/scenes/references/scripts、briefs/typesetting/configs 等），`LICENSE.txt` 原样保留 | **个人/教育/非商业用途**；本技能包本身即非商业教育用途。docx 的 `postcheck.py` 需 Python ≥ 3.9（解释器过旧时按其 §7 手工清单自查，脚本完好勿改） |
| 官方 PPT 模板、校徽、校训、学院标识 | 电子科技大学官方视觉物料 | **仅限校内学习使用**，请勿用于商业或对外宣传；如有侵权请联系删除 |
| 图表/图标资产 | [ppt-master](https://github.com/hugohe3/ppt-master) 子集，MIT；图标精选自 Tabler（MIT）、Phosphor（MIT） | 全量库与 CC BY 图标见上游；`THIRD_PARTY_NOTICES.md` 随包保留 |
| LaTeX 模板 | uestcreport（ThesisUESTC 衍生），LPPL-1.3c | `LICENSE-LPPL-1.3c` 随包保留 |

### 图标全量获取

本包仅内置 570 枚精选图标（学术演示常用）。需要全量 12000+ 时，从
`https://github.com/hugohe3/ppt-master`（templates/icons/）下载并替换 `assets/icons-charts/icons/`；
其中 `chunk-filled` 子库为 CC BY 4.0（作者 Noah Jacobus），使用需保留署名，本包默认未收录。

### 字体

不随包分发。PPT 用系统自带的微软雅黑/等线；LaTeX 用本机 TeX 发行版的中文字体（如 SimSun/SimHei）；
正文图表推荐 matplotlib + 微软雅黑。缺少字体时 LibreOffice/PowerPoint 会自动替换。

## 免责声明

本包由学生社区整理，与电子科技大学官方无关。官方视觉素材版权归学校所有，
仅限校内课程学习使用。样本提炼形成的写作规律文档均已匿名化，不含任何个人信息。
