<div align="center">

<img src="assets/slides/brand/%E6%A0%A1%E5%BE%BD.png" width="130" alt="电子科技大学校徽"/>

# uestc-create

**uestc课程交付物skill包** —— 课程PPT · 实验报告 · 课程论文与课设报告 · 项目式课程规划

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-pptxgenjs-5FA04E?logo=nodedotjs&logoColor=white)
![LaTeX](https://img.shields.io/badge/XeLaTeX-TeX%20Live-008080?logo=latex&logoColor=white)
![UESTC](https://img.shields.io/badge/%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6-UESTC-164C8C)

</div>

**uestc-create** 是一个面向电子科技大学（UESTC）课程场景的 agent 技能包，覆盖四类交付物：**课程汇报 PPT、实验报告、课程论文与课程设计报告、项目式课程规划（开题/中期/结题）**。

它的定位是"最后一公里"：实验操作、数据分析与代码实现不在其职责范围内；当研究成果已经完成，由本技能包负责将既有成果转化为符合院校规范的交付物。课程交付物制作的典型困难在于——官方模板的母版占位符结构缺乏公开文档、实验报告的节骨架因课程与教师而异、LaTeX 模板编译链配置繁琐、模型直出的文本带有明显的机器痕迹。本技能包将上述规范固化为可由 agent 执行的文档、脚本与评测，其内容来自 52 份真实学生交付物的精读蒸馏，难以通过公开检索复现。

## 目录

- [1. 项目简介](#1-项目简介)
- [2. 核心价值：难以自行复制的规范](#2-核心价值难以自行复制的规范)
- [3. 实测对比](#3-实测对比)
- [4. 功能路线](#4-功能路线)
- [5. 安装](#5-安装)
- [6. 使用示例](#6-使用示例)
- [7. 目录结构](#7-目录结构)
- [8. 兼容性与平台](#8-兼容性与平台)
- [9. 验证与自检](#9-验证与自检)
- [10. 许可](#10-许可)
- [11. 鸣谢](#11-鸣谢)
- [12. 免责声明](#12-免责声明)

## 1. 项目简介

| 路线 | 交付物 | 说法示例 |
|---|---|---|
| **A slides** | 汇报 PPT（官方模板填充 / 自建设计 / LaTeX beamer）+ 逐页讲解词 | "做个组会 PPT""12 页中期答辩，用官方蓝模板" |
| **B lab-report** | 实验报告（标准模板或老师指定模板） | "数电实验三的数据在 lab3.xlsx，按标准格式写报告" |
| **C course-papers** | 课程论文（LaTeX/Word）、课设报告、综合课程设计、结题报告、思政论文 | "党史课期末论文，题目自选，3000 字" |
| **D stage-planning** | 开题/中期/结题内容规划（仅对话规划，不产出文件） | "我下个月开题，帮我理一理要做哪些事" |

**范围外**（会明确拒绝并说明）：平时作业答案、实验操作指导、数据分析方法、代码本身、周报/工作总结等日常文书。

## 2. 核心价值：难以自行复制的规范

先说一个诚实的结论（来自我们自己的对照评测，见第 3 节）：**强模型自己就能写出"内容可用"的报告和 PPT**。本包的价值不在内容生成，而在**制度性硬格式的合规化**——那些基线 agent 拿不到、查不到、试不起的部分。

### 2.1 52 份真实高分样本蒸馏

| 代号 | 样本量 | 类型构成（匿名） |
|---|---|---|
| **B-xx** 实验报告 | 16 份 | 官方 12 节骨架 / 实践变体 / 计组完整与极简版 / 教师自定学术型 / 合并型 / 结对小组 等 |
| **P-xx** 汇报 PPT | 16 份 | 课程展示 / 过程汇报 / 文献分享（综述·精读·算法）/ 开题 / 中期 / 终期 / 思政 / beamer 学术 / 长讲座 |
| **C-xx** 课程论文与课设 | 20 份 | 思政 / 观点 / 理论推导 / 学术综述 / 课程设计与综合课设 / 结题报告 / 数模 / LaTeX 工程 |

开发期对这些真实学生交付物逐份精读，蒸馏出 `references/` 下的全部规范：场景叙事配方（含 ★/△ 证据强度标记）、页标题结论式与卡片两级结构、实验报告语气双轨制、负结果诚实范式、思政三件套……其中**去 AI 味禁用词表经过四轮样本证据校准**——比如真实学生语料中"综上所述"在结论处属正常用法，禁的是空洞化滥用。这种分寸感，只有读过真样本才有。样本原件不随包分发、已全部匿名化（见 `references/evidence.md`）。

### 2.2 四条难复制资产

1. **成电官方模板与院校视觉体系** —— 8 套官方 PPT 模板随包，红/蓝/白风景/DIY 四套完成母版占位符几何提取（JSON 化，可程序化填充）；**校徽全套与 15 个学院标识精选随包**——8 个学院提供白色版/校徽蓝版深浅底双版本对照，覆盖计算机、集成电路、信息与通信、机械与电气、物理等主要学院，**满足不同学院与学科的需求**；主楼/图书馆建筑线稿、银杏、校训等特色素材齐备，自建轨另有特色配色「校徽蓝 + 银杏黄」（含实测色值）。生成 PPT 时按默认出场表主动配齐：封面、header、结尾的校/院标识，目录与分节页的线稿装饰，银杏点缀与校训水印。
2. **官方骨架与格式参数** —— 实验报告官方 12 节骨架与版式参数；UESTC LaTeX 论文模板（XeLaTeX 编译实测通过）；GB/T 7714 引用规范。
3. **去 AI 味写作纪律** —— 四条正面原则（成段成体系/拒绝名词罗列/深入浅出/去 AI 味）+ 报告、论文、思政、PPT、讲解词分场景细则 + 生成前后自查清单。
4. **交付前自动自检** —— 机检脚本（占位符/禁用词/模糊数字/个人信息/emoji/密度）→ python-pptx 代码 QA（溢出/重叠/越界）→ 真渲染逐页视觉验收 → 独立裁判 agent（生成者≠裁判）。

### 2.3 工程化闭环

触发评测（20 条 should/should-not，should-not **9/9 零误触发**）、渲染后端探测（PowerPoint/Word/WPS/LibreOffice 自动择优）、跨平台审计（Windows 实测 + Linux/macOS 静态审计）、用户反馈驱动的修订闭环（版式对齐、文字填充率、标题语域、SVG 适配等 17 项改造全部留痕）。

## 3. 实测对比

同一任务、两条 arm（加载本技能 vs 无技能基线）的行为评测：

| 任务 | 本技能 | 基线 | 关键区分点 |
|---|---|---|---|
| 实验报告 | **6/6** | 4/6 | 官方 12 节骨架命中 **12/12 vs 5/12**——基线自造八节，丢掉「实验步骤」「实验数据及结果分析」「总结及心得体会」 |
| 组会 PPT | **6/6** | 5/6 | 页标题结论句（"RMSE 由 2.31% 降到 1.44%"）vs 基线栏目名（"07 实验设置""08 实验结果"）——正是本包明令禁止的写法 |
| 论文 LaTeX | **6/6** | 未跑* | XeLaTeX 编译零 error / 零 undefined ref / Overfull 0；引用 6 条全部真实可查 |
| 分期规划 | 4/5 | 4/5 | 打平——通用规划强模型已擅长 |

\* 基线未跑系成本考量（与实验报告路线区分点重叠）；PPT 组双臂均在模型余额告警下提前终止，但 .pptx 已完整产出、断言已跑完。

**按路线看增量**：

| 路线 | 增量 | 原因 |
|---|---|---|
| B 实验报告 | **大** | 有硬性可核验的院校格式（12/12 vs 5/12） |
| C 课程论文 | **大** | LaTeX 模板 + GB/T 7714 + 编译链 |
| A 汇报 PPT | 中 | 官方模板是公开资产，基线也会去找；增量在标题风格与写作纪律 |
| D 分期规划 | ≈0 | 强模型已擅长，且会更主动联网核查 |

> 护城河不在素材本身，而在**把素材、骨架、纪律、自检串成流程的规范**。评测还顺带抓出并修复了包内 1 个必然崩的路径 bug——评测不是走过场。

## 4. 功能路线

| 需求 | 路线 | workflow |
|---|---|---|
| 汇报 PPT / 答辩 / 组会 pre / 文献分享 | **A slides** | `workflows/slides.md` |
| 实验报告（合并型也算） | **B lab-report** | `workflows/lab-report.md` |
| 课程论文 / 课设报告 / 综合课程设计 / 结题 / 思政论文 | **C course-papers** | `workflows/course-papers.md` |
| 规划开题 / 中期 / 结题怎么安排 | **D stage-planning**（只规划不产出文件） | `workflows/stage-planning.md` |

动工前技能会问清关键选择（官方模板还是自建设计、LaTeX 还是 Word、校徽还是学院标识），信息齐了不再重复问；用户工作区已有的老师模板/格式要求永远优先于包内默认。

## 5. 安装

### 5.1 手动安装（git clone）

```bash
# 克隆到 agent 技能目录（克隆目录名须为 uestc-create）
# ZCode / 通用 agent —— Windows (PowerShell)：
git clone https://github.com/pyzw618/uestc-create.git "$env:USERPROFILE\.agents\skills\uestc-create"
# ZCode / 通用 agent —— Linux / macOS：
git clone https://github.com/pyzw618/uestc-create.git ~/.agents/skills/uestc-create
# Claude Code：
git clone https://github.com/pyzw618/uestc-create.git ~/.claude/skills/uestc-create
```

> 也可以克隆到任意位置，再把整个 `uestc-create/` 文件夹拷入所用 agent 的技能目录，或按所用工具的方式注册该文件夹为技能。更新：进入目录 `git pull` 即可。

**2. 填写你的信息**：首次使用从 `config/user.yaml.example` 复制一份 `config/user.yaml` 并填写（姓名/学号/学院/专业，生成封面要用）。该文件只存在本机，已被 `.gitignore` 忽略，不会随包分发；留空则首次生成封面时技能会引导你填。

**3. 依赖**（按需，缺什么装什么）：

- Python 3.9+：`python-pptx`、`python-docx`、`Pillow`、`pypdf`、`matplotlib`、`pymupdf`
- 渲染器（预览与视觉验收）：**用本机已有的任一即可，无需额外安装**——Windows：PowerPoint / Word / WPS（原生渲染对自家格式更忠实）；Linux / macOS：LibreOffice。**一个都没有时**再装 [LibreOffice](https://mirrors.tuna.tsinghua.edu.cn/libreoffice/libreoffice/stable/)（清华镜像快）
- TeX Live（XeLaTeX + latexmk，仅 LaTeX 论文路线需要）
- Node.js + `pptxgenjs`（pptx 引擎的 JS 生成轨，可选）

### 5.2 提示词安装（交给 agent 执行）

复制以下提示词发给你的 agent（具备文件读写与 shell 能力即可），自动完成安装：

```text
请帮我安装 uestc-create 技能包，步骤：
1. git clone https://github.com/pyzw618/uestc-create.git 到本机 agent 技能目录
   （ZCode/通用：~/.agents/skills/；Claude Code：~/.claude/skills/；Windows 注意用对应
   用户目录。目录已存在则进入目录 git pull 更新）；
2. 若目录下没有 config/user.yaml，从 config/user.yaml.example 复制一份，逐项询问我的
   姓名/学号/学院/专业后帮我填好（这些信息只写本机配置，不要外传）；
3. 检查 Python 依赖 python-pptx / python-docx / Pillow / pypdf / matplotlib / pymupdf，
   缺哪个用 pip 装哪个；再探测本机渲染器（PowerPoint / Word / WPS / LibreOffice）并告诉我
   视觉验收会用哪个；
4. 装完报告结果，并举两个例子说明怎么触发本技能。
```

## 6. 使用示例

- 「把这篇论文做成 12 页中期答辩 PPT，用官方蓝模板」
- 「数电实验三的数据在 lab3.xlsx，按标准实验报告格式写报告」
- 「党史课期末论文，题目自选，3000 字」
- 「我下个月开题，帮我理一理要做哪些事」（只给规划，不产出文件）

即便你觉得自己能直接做，也建议先让它跑一遍——对比效果见[第 3 节](#3-实测对比)。

## 7. 目录结构

```
SKILL.md                总路由（先读这个）
config/user.yaml        你的信息（只存在本机，不入库）
workflows/              四条路线的工作流
references/             写作纪律(writing-style.md) + 各路线规范 + 样本证据索引
scripts/                固化脚本（cjk / mpl_cjk / pptx_bg / pptx_qa / render_preview）
evals/                  机检与评测（check_deliverable / run_trigger_eval / grader）
assets/
  slides/templates/     8 套官方 PPT 模板
  slides/masters/       红/蓝/白风景/DIY 四套母版几何 JSON（其余 4 套无，走自由填充）
  slides/brand/         校徽/校标/院徽(15 学院)/线稿/银杏 等官方素材
  icons-charts/         图表 SVG 模板 ×33 + 精选图标 ×570
  course-papers/        论文/课设模板 + LaTeX 模板
  lab-report/           标准实验报告模板与版式参数
engines/
  docx/ pdf/ pptx/      三引擎（官方技能完整内容随包，轻量适配任意 agent）
  visual-judge.md       视觉验收提示词（子 agent 可派发；无子 agent 能力按其自查）
```

## 8. 兼容性与平台

**Agent 兼容性**：内容与 agent 无关——不依赖任何宿主专属工具（无 Task/Skill/artifacts 之类调用）。子 agent 全程**可选**：视觉验收与独立打分处都写了"无子 agent 能力时按同一标准自查"的降级路径（`engines/visual-judge.md`、`evals/grader.md`）。唯一前提：「技能被自动发现」依赖宿主具备 skill 机制（如 SKILL.md 约定）；在不具备该机制的框架或裸 API 下，内容同样可用，但需把 `SKILL.md` 显式交给模型。

**平台兼容性**：

| 项 | Windows | Linux / macOS |
|---|---|---|
| python 脚本（`scripts/`、`evals/`） | ✅ 已实测 | 静态审计通过，**未实机验证** |
| 渲染器 | PowerPoint / Word / WPS（经 `pywin32` COM） | LibreOffice（`soffice`） |
| 中文字体默认 | 微软雅黑 | Linux: Noto Sans CJK SC · macOS: PingFang SC |
| shell 脚本（`engines/*/env_check.sh`、`setup.sh`） | 需 Git Bash 或 WSL | ✅ 原生 bash |

渲染器是**探测式**的：`scripts/render_preview.py` 自动选本机最忠实的一个，一个都没有时才提示安装 LibreOffice。缺中文字体时 `mpl_cjk.py` 会**显式告警**，不会静默渲染出方块。

> Linux / macOS 结论来自代码静态审计，未在相应系统上实跑。

## 9. 验证与自检

- `evals/check_deliverable.py <file>`：纯标准库机检（占位符 / 禁用词 / 模糊数字词 / 个人信息 / emoji / 单块密度），有 hard fail 时返回非零。各路线 workflow 的验收步已接入。
- `evals/grader.md`：独立验收 agent 提示词（生成者≠裁判）；有子 agent 能力时派发。
- `evals/evals.json`、`evals/trigger-eval.json`：行为 eval 集与触发评测集（20 条 should/should-not）。
- `evals/run_trigger_eval.py`：Windows 可用的触发评测。上游 skill-creator 的 `run_eval.py` 用 `select()` 读管道，Windows 不支持（WinError 10038），故本包自带替代版。

## 10. 许可

本仓库的技能文档与脚本（`SKILL.md`、`workflows/`、`references/`、`scripts/`、`evals/`）以 **[MIT](./LICENSE)** 发布。第三方内容保留原许可：

| 内容 | 来源与许可 | 说明 |
|---|---|---|
| `engines/docx\|pdf\|pptx`、`engines/visual-judge.md` | 改造自 Z.AI 官方 documents/pdf/presentations 技能（v1.1 完整内容随包），`LICENSE.txt` 原样保留 | **个人/教育/非商业用途**；本技能包本身即非商业教育用途。docx 的 `postcheck.py` 需 Python ≥ 3.9（解释器过旧时按其 §7 手工清单自查，脚本完好勿改） |
| 官方 PPT 模板、校徽、校训、学院标识 | 电子科技大学官方视觉物料 | **仅限校内学习使用**，请勿用于商业或对外宣传；如有侵权请联系删除 |
| 图表/图标资产 | [ppt-master](https://github.com/hugohe3/ppt-master) 子集，MIT；图标精选自 Tabler（MIT）、Phosphor（MIT） | 全量库与 CC BY 图标见上游；`assets/icons-charts/THIRD_PARTY_NOTICES.md` 随包保留 |
| LaTeX 模板 | uestcreport（ThesisUESTC 衍生），LPPL-1.3c | `assets/course-papers/latex/LICENSE-LPPL-1.3c` 随包保留 |

### 10.1 图标全量获取

本包仅内置 570 枚精选图标（学术演示常用）。需要全量 12000+ 时，从
`https://github.com/hugohe3/ppt-master`（templates/icons/）下载并替换 `assets/icons-charts/icons/`；
其中 `chunk-filled` 子库为 CC BY 4.0（作者 Noah Jacobus），使用需保留署名，本包默认未收录。

### 10.2 字体

不随包分发。PPT 用系统自带的微软雅黑/等线；LaTeX 用本机 TeX 发行版的中文字体（如 SimSun/SimHei）；
正文图表推荐 matplotlib + 微软雅黑。缺少字体时 LibreOffice/PowerPoint 会自动替换。

## 11. 鸣谢

由衷感谢**计算机科学与工程学院苑同学（珠峰）、集成电路科学与工程学院高同学（强芯）、信息与通信工程学院张同学、物理学院刘同学等**，他们慷慨提供了自己的高分课程交付物——实验报告、汇报 PPT、课程论文与课设报告共 **52 份**——作为开发期精读样本。本包 `references/` 中的全部写作规律、格式阈值与禁用词表均蒸馏自这些真实样本；样本原件不随包分发，且已全部匿名化（`references/evidence.md`）。

同时感谢：

- **uestcreport 技能** —— 课程论文 LaTeX 路线的模板与 `create_report.py` 工程化脚本源自作者的同系技能 uestcreport（ThesisUESTC 衍生，LPPL-1.3c 随包保留）；
- **[ppt-master](https://github.com/hugohe3/ppt-master)** —— 33 类图表 SVG 模板与图标资产的上游（MIT）；
- **ZCode 官方 documents / pdf / presentations 技能（Z.AI）** —— `engines/` 三引擎的改造源头，原许可条款随包保留；
- **Tabler** 与 **Phosphor** —— 精选图标各自的上游（均为 MIT）。

## 12. 免责声明

本包由学生社区整理，与电子科技大学官方无关。官方视觉素材版权归学校所有，仅限校内课程学习使用。样本提炼形成的写作规律文档均已匿名化，不含任何个人信息。本软件按 MIT 许可"原样"提供，不附带任何担保；使用本包产出的内容请自行核对真实性与合规性。
