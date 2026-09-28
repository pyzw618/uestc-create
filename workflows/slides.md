# A 路线：汇报 PPT（slides）

> 状态：**v1（阶段 3 完成版）**。分「必守检查点」（⚠）与「弹性做法」两层。

## 输入与产出

- **输入**：论文/报告/项目成果、限定信息（页数/时长/场景）、往期 deck（系列任务时）。
- **产出**：.pptx（+ 讲解词成段文稿 + 按需 PDF/白底打印版）。
- **前置提醒**：成果还没做出来时先说明本路线做呈现；没有可讲的内容不做空壳 PPT。

## ⚠ 第 0 步：开工询问与信息收集（硬性，一次问完）

1. **「使用官方标准模板，还是自建设计？」**（官方 8 套见 `assets/slides/templates/`，可给用户列清单；用户工作区已有模板则直接用，最高优先）。用户选官方模板时留意：**仅红/蓝/白风景/DIY 四套有母版几何 JSON**，电科院×3 与 `PPT_UESTC_M_DIY` 无，走 A1 自由填充分支。
2. 顺带一次问齐：场景（课程展示/组会文献分享/开题/中期/终期/思政/学术报告）、页数或时长、讲者、是否需要讲解词、系列任务是否有往期 deck。
3. 记录 `轨道`：A1 官方模板填充 / A2 自建设计 / A3 LaTeX beamer（数学/化学/理论型课程报告且用户偏好 LaTeX 时主动提出）。

## 第 1 步：场景配方与内容规划

1. 读 `references/slides/scenarios.md` 对应配方（骨架/页数/密度/核心页），**先看配方标题旁的置信标记**：★=≥2 份样本可放心套用；△=单专属样本（§3 开题答辩、§6 思政展示），骨架**保守套用并向用户确认**后再动工；系列任务读 `exemplars.md` §3 建立系列样式卡。
2. 从输入材料提炼**每页一个主张**：先列页级大纲（页码|页标题（结论句）|锚点（图/卡/数字）|素材来源），与用户确认大纲再动工（页数多或场景正式时必确认；小任务可跳过）。
3. 密度守 `scenarios.md` 速查表；数据只引用用户材料里的真实数字，**不编造**。

## 第 2 步：按轨道生成

### A1 官方模板填充
1. 读 `assets/slides/masters/master_*.json`（对应模板的版式占位符几何）→ 按大纲选版式 → python-pptx 填充 → **另存新文件**。**只有红/蓝/白风景/DIY 四套有该 JSON**；用户选了电科院/DIY_M 模板时无 JSON，直接落到第 2 步的自由填充路径。
2. 版式层无占位符的页面（自由文本框型）：解包回读实际形状几何做预算填充（engines/pptx 模板工作流：Clone & fill / Fill-in 判据）。
3. 图表按 `references/slides/charts.md`：原生图表优先；模板 accent 色接管图表配色。
4. **页面级背景图**（官方红/蓝/白实测）：背景不在版式层，而在个别页面的 `<p:bg>` blipFill 里（官方蓝仅 4 页有：封面/目录/致谢，内容页为母版素底）。用 `python scripts/pptx_bg.py --pptx T.pptx --from <源页> --to <目标页…> [--delete-source] --out out.pptx` 克隆——脚本已处理**必须重绑图片关系**（直接复制 rId 会在目标页解析不到、背景丢失）。**背景图上烙有文字**（目录页自带"目 录"），只能给对应功能页复用。
5. **中日韩字体**：pptx 必须设 DrawingML 的 `a:ea`（`w:eastAsia` 是 docx 写法，对 pptx 无效）；生成后兜底跑 `python scripts/cjk.py fix <file.pptx> --ea 微软雅黑`。matplotlib 中文用 `scripts/mpl_cjk.py`（自动注册本机中文字体，避免方块）。

### A2 自建设计
1. 按 `references/slides/brand.md`：选配色家族（蓝橙学术风/深蓝高级风/深蓝科技风/主题化配色/校徽蓝+银杏黄特色）。
2. 成电元素齐备：校标组合（header/封面）、校训水印（封面/结尾）、线稿（目录页）、银杏（点缀，单页 ≤3）；版本正确（白版深底/蓝版浅底）。
3. 长 deck（≥25 页）上左侧导航条（P-16 模式）；分节用数字分节页或提纲回现。
4. 排版遵守 `engines/pptx/SKILL.md` Part 1 设计规范与 Part 2 API 要点（LAYOUT_WIDE、bullet 样式化、阴影参数、避免 AI 味版式：无标题下划线、无彩色边条、卡片 ≤1/5 页）；多列卡组顶/底边对齐、卡内文字填充率与卡头对齐细则见 `references/slides/brand.md` §2–3；视觉锚点选型可参考 `references/slides/charts.md` §4 适配场景——含编号卡/功能行/分节卡的页面有合适图标就配，没有就不硬加，禁止 emoji 与文本圈号顶替。

### A3 beamer 支线
按 `scenarios.md` §7 基线（Madrid+whale、169、columns、脚注引源、红字标签）与其**编译实测要点**（缺图重建 / 多页 PDF 素材的 page+trim 裁切 / 占位图用 PIL 生成 / -no-pdf 分离诊断）；`xelatex` 编译交付 PDF（该链已在 TeX Live 2025 实测，14 页通过）。

## 第 3 步：页面生成纪律

- 载入 `../references/writing-style.md` §2.4：页标题结论式、正文短句数据前置、每页一个主张；讲解词按 §2.5 成段口语化。
- 图表页：图为主角+来源行+"看什么"≤3 条；错误样本/榜单截图圈注关键位置。
- 弹性：用户提供了自己往期的 deck，则继承其视觉语言而非包内家族。

## ⚠ 第 4 步：验收（硬性）

1. 机检：`python evals/check_deliverable.py <成品.pptx>` 跑客观断言（占位符/禁用词/模糊数字/个人信息/密度），hard fail 先清零。
2. 代码 QA：`python scripts/pptx_qa.py <成品.pptx>`（占位符/越界/溢出估算/文本重叠）；细节按 engines/pptx §10。
3. 渲染 QA：`python scripts/render_preview.py <成品.pptx>` 出逐页 PNG，按 `engines/visual-judge.md` 提示词验收（无子 agent 则自查）；fail 项修复后复查。
4. 过 `references/slides/checklist.md` A→E；需要独立判定时派 `evals/grader.md`，报告结果。

## 边界

- 编造实验数据/榜单成绩/引用 → 拒绝；占位数字必须显式标注"示例，待替换"。
- 要文档不要 PPT → 转 B/C；要的是内容规划（开题该做什么）→ 转 D。
