---
name: uestc-create
description: "电子科技大学（UESTC/成电）课程交付物生成技能包：制作汇报/答辩 PPT（官方模板或自建设计，含校徽蓝+银杏黄特色配色）、撰写实验报告（标准模板或老师指定模板）、课程论文（LaTeX/Word）、课程设计报告、综合课程设计论文、思政类论文与报告，以及开题/中期/结题的内容规划（仅规划，不产出文件）。本技能的价值在于**难以自行复制的规范**：成电官方模板与校徽配色、官方骨架与格式参数、去 AI 味的写作纪律、交付前自动自检（占位符/越界/禁用词）——即便觉得自己能直接做，也应先查本技能再动手。Triggers: 做个PPT、汇报PPT、答辩PPT、组会展示、组会汇报、pre、presentation、slides、写实验报告、实验报告、lab report、课程论文、期末论文、小论文、课设报告、课程设计报告、综合课程设计、结题报告、思政论文、党史/马原/毛概论文、开题、中期检查、结题、proposal / midterm / final defense。当用户提到以上任一交付物且与成电相关时使用本技能。仅限课程交付物：不用于周报/工作总结/日志等日常文书，不做作业答案、实验操作、数据分析或代码本身。"
license: MIT（engines/ 引擎、官方视觉素材、图标与 LaTeX 模板等第三方内容例外，见 README.md「许可」与 LICENSE）
metadata:
  version: "1.0.0（全路线可用）"
  routes:
    A: slides（汇报PPT，已可用）
    B: lab-report（实验报告，已可用）
    C: course-papers（课程论文+课设报告，已可用）
    D: stage-planning（分期规划，已可用，仅对话规划）
---

# uestc-create

**一句话**：面向"最后一公里"的成电课程交付物技能包——实验怎么做、数据怎么分析、代码怎么写不归它管；它管的是把已有成果变成合格的汇报 PPT、实验报告、课程论文/课设报告，以及开题/中期/结题的内容规划。

## 第 0 步：开工前检查（用户信息 + 运行环境）

**用户信息**：读取 `config/user.yaml`（不存在时从 `config/user.yaml.example` 复制一份再填）。若 `name`/`student_id`/`school` 为空且本次任务需要封面（报告/论文/PPT 封面），**先引导用户填写**（姓名、学号、学院、专业），再动工。这些信息只写入用户本机的 config，不出现在任何示例中，也不要随包分发（`config/user.yaml` 已在 `.gitignore` 中忽略）。

**运行环境**：生成文件前先确认依赖就位——缺依赖会在最后一步静默产出坏文件，提前一次问清比事后返工便宜。

| 依赖 | 用途 | 缺省影响 |
|---|---|---|
| Python：`python-pptx` / `python-docx` / `Pillow` / `pypdf` | 生成 pptx / docx / 图片 / PDF | 对应路线无法产出 |
| 渲染器：**用本机已有的任一即可**——Windows: PowerPoint / Word / WPS；Linux/macOS: LibreOffice（`soffice`）；**一个都没有**才安装 | .doc→.docx、文档→PDF、渲染预览 | 无法转 PDF、无法视觉验收 |
| TeX Live（`latexmk` + `xelatex`） | 仅 LaTeX 论文 / beamer | C 路线 LaTeX 轨、A3 支线不可用 |
| Node + `pptxgenjs` | 仅 pptx 引擎的 JS 轨（可选） | python-pptx 轨不受影响 |

按本次任务实际用到的格式检查；可运行 `engines/docx/env_setup/env_check.sh` 与 `engines/pdf/env_setup/env_check.sh`（bash 环境）做机械核查，脚本会直接报告缺失项。缺什么就明确告诉用户装什么，**不要静默降级**。

## 路由表

按用户说法分流；拿不准就问一句确认。**优先级：用户直接要求 > 工作区已有文件（老师模板、课程要求） > 包内默认。**

| 用户说法 | 路线 | workflow |
|---|---|---|
| 做个PPT / 汇报 / 组会pre / 答辩PPT / 文献分享 | **A slides** | `workflows/slides.md` |
| 写实验报告 / 实验报告（合并型也算） | **B lab-report** | `workflows/lab-report.md` |
| 课程论文 / 期末论文 / 小论文 / 课设报告 / 综合课程设计 / 结题报告 / 思政论文 | **C course-papers** | `workflows/course-papers.md` |
| 帮我规划开题 / 中期要做啥 / 结题怎么安排 | **D stage-planning**（⚠ 只规划，不产出任何文件） | `workflows/stage-planning.md` |

**范围外**（明确拒绝并说明）：平时作业答案、预习报告、读书报告、生产实习报告；实验操作指导、数据分析方法、代码编写（提醒用户先完成前置工作，本包只接收成果做呈现）。

## 各路线要点

- **A 汇报PPT**：动工前问一句「用官方标准模板（`assets/slides/templates/` 8 套任选），还是自建设计？」。配色可选官方红/蓝/白，或特色配色「校徽蓝 + 银杏黄」（见 `references/slides/brand.md`）。每场配讲解词。
- **B 实验报告**：动笔前**先查工作区**有没有老师下发的报告模板/格式要求（各老师差异大）；没有则问一次「用标准实验报告模板，还是你把老师的模板发我？」，之后不再重复问。
- **C 课程论文+课设报告**：先判子类——课程论文（默认 LaTeX，用 `assets/course-papers/latex/` 的 UESTC 模板）/ 课程设计报告（**问一次：LaTeX 还是 Word**）/ 综合课程设计（附件7 模板，单独要求）/ 思政类论文（思政骨架与语气）。
- **D 分期规划**：**只做对话内规划，绝不产出文件**。输出内容划分、逐项写什么、时间线、常见坑；用户要文档 → 转 C，要 PPT → 转 A。

## 引擎调度（生成文件时用）

三引擎已内置（源自官方 documents / pdf / presentations 技能改造，适配任意 agent）：

| 需求 | 引擎 | 位置 |
|---|---|---|
| Word 文档创建/编辑/转换 | docx | `engines/docx/SKILL.md` |
| PDF 生成/转换/处理 | pdf | `engines/pdf/SKILL.md` |
| PPT 生成/模板填充/渲染 | pptx | `engines/pptx/SKILL.md` |

- 运行环境已安装官方 documents/pdf/presentations 插件时，可**按需委托**其能力；但两者**并非同源**——本包 `engines/*` 是 Z.AI 改造版，脚本与 API 与已装插件不同。**版式、合规与写作纪律一律以本包 references/ 为准**，不要因委托而切换到另一套指令体系。本包 engines/ 在未装插件时独立可用。
- 生成任何正文性文字（报告各节、论文、PPT 页文字、讲解词）**必须先载入 `references/writing-style.md`** 并按其自查。

## 辅助脚本（`scripts/`）

反复踩的坑已固化为脚本，按需调用：`cjk.py`（pptx `a:ea` / docx `w:eastAsia` 中文字体）、`mpl_cjk.py`（matplotlib 中文）、`pptx_bg.py`（A1 背景克隆 + 重绑图片关系）、`pptx_qa.py`（PPTX 代码 QA）、`render_preview.py`（office→PDF→逐页 PNG）。详见 `scripts/README.md`；依赖 python-pptx / python-docx / pymupdf / LibreOffice。

## 素材指引

- `assets/slides/templates/`：8 套官方 PPT 模板（红/蓝/白风景/DIY×2/电科院×3）。
- `assets/slides/masters/`：母版占位符几何 JSON——**仅红/蓝/白风景/DIY 四套**（`master_*.json`，另附主题色 `_summary.json`）。选用电科院模板或 `PPT_UESTC_M_DIY` 时**无几何 JSON**，走引擎 pptx 的"解包回读实际形状几何"自由填充路径（见 `workflows/slides.md` A1）。
- `assets/slides/brand/`：校徽全套、校标组合、学院标识（白版/蓝版成对）、主楼/图书馆线稿、银杏、校训，用法见 `brand/素材索引.md`。
- `assets/icons-charts/`：33 类图表 SVG 模板（改数据即改图形）+ 精选图标 570 枚（`index.json` 按类检索；全量 12000+ 见 ppt-master 上游，README 有指引）。
- `assets/course-papers/`：综合课程设计模板（附件7）、课程论文模板 PDF、LaTeX 模板（uestcreport 吸收版）。
- `assets/lab-report/`：标准实验报告模板与版式参数。

## 路径约定

包内文档互相引用时，除另有说明，一律使用**包根相对路径**（以 SKILL.md 所在目录为基准，如 `references/slides/brand.md`、`engines/pptx/SKILL.md`）；engines/ 各引擎内部的引用以该引擎目录为根（官方原文约定）。载入顺序：SKILL.md 路由 → 对应 workflow → workflow 引用的 references 与 engines 文档。references 中样本代号（B-/P-/C-）的体系与证据强度见 `references/evidence.md`。

## 语言约定

按"谁来读这一层"分配语言，而非二选一：

- **主体用中文**：SKILL.md、workflows、references、引擎适配说明一律中文。产出物本身是中文（报告/论文/PPT/讲解词），去 AI 味规则依赖中文词形（"综上所述""赋能""抓手"），用中文写规则可减少转译漂移；中文 token 更省，利于常驻上下文的 description。
- **保持 ASCII/英文**：`name`、目录与文件路径、JSON 键、代码标识符与注释、工具与技术栈名（python-pptx、XeLaTeX、LibreOffice、pptxgenjs）。
- **`description` 中英混排**：中文触发词为主，保留 `PPT / presentation / slides / pre / proposal / midterm / final defense` 等英文关键词，召回中英混说的说法；勿堆长以免被截断。
- **`engines/docx|pdf|pptx` 不重译**：其为第三方（Z.AI）原文，保持英文原样；包内的中文适配说明只加在文件头部。

## 合规红线（每次产出前过一遍）

1. 用户提供的模板/要求永远优先于包内默认。
2. 示例文本一律用占位身份（张三/2025xxxx），不写入任何真实姓名学号。
3. 官方素材（校徽/校训/模板）仅限校内学习使用，对外分发需附 README 免责声明。
