# evals/

验证基础设施：把"生成者自评"换成可复现的机检与独立判定。

| 文件 | 作用 |
|---|---|
| `check_deliverable.py` | 交付物机检（纯标准库）：占位符 / 禁用词 / 模糊数字 / 个人信息 / emoji / 密度。有 hard fail 返回非零。 |
| `grader.md` | 独立验收 agent 提示词（生成者≠裁判）。 |
| `evals.json` | 4 条行为 eval（A/B/C/D 四路线各一）。 |
| `trigger-eval.json` | 触发评测集：20 条 should/should-not。 |
| `run_trigger_eval.py` | 触发评测器（Windows 可用）。 |

## 用法

```bash
# 机检一份成品
python evals/check_deliverable.py 成品.docx            # .docx / .pptx
python evals/check_deliverable.py 成品.pptx --json

# 触发评测（改 description 后必跑）
python evals/run_trigger_eval.py \
  --eval-set evals/trigger-eval.json \
  --skill-path . --model sonnet --runs-per-query 2 --workers 3 --timeout 180
```

## 触发评测的两个坑（都已内置处理）

1. **上游 `skill-creator` 的 `run_eval.py` 在 Windows 不可用**：它用 `select()` 读管道，Windows 报 `WinError 10038`，导致**所有查询恒判"未触发"**。本包自带 `run_trigger_eval.py`（阻塞读到 EOF + 看门狗超时）替代。
2. **并发会制造假阴性**：每次 `claude -p` 启动要加载全部插件与 hook，很重。实测 `workers=6 + timeout=90` 时 40 个调用**全部超时**并被静默记为"未触发"（表现为全 20 条 0.0）。**务必 workers ≤ 3、timeout ≥ 180**；脚本会打印非正常结束计数。另：脚本每轮会清理历史残留同名 shim，残留 shim 同样造成假阴性。

## 已知测量局限

- **空工作区假象**：查询引用的素材（如 `lab3.xlsx`）不在评测工作区时，模型会去**要文件**而不是调用技能，记为未触发。验证召回率时，工作区里要放真实素材。
- **样本量小**：`--runs-per-query 2` 下 `0.5 ↔ 0.0` 的差异在噪声内，不要据此做细粒度调参。
- 触发行为本身是概率性的：可被直接回答的请求（"做个 PPT"）常常不咨询技能，符合 skill-creator 的观察。

## 已测结果（2026-09-28）

**触发评测**：17/20（should-not **9/9 全过**，0 误触发）。

**行为 eval**（`iteration-1/`，with_skill vs 无技能基线）：

| eval | with_skill | 基线 | 区分点 |
|---|---|---|---|
| eval-0 实验报告 | **6/6** | 4/6 | 官方 12 节骨架 **12/12 vs 5/12**；基线自造八节，丢了「实验步骤」「实验数据及结果分析」「总结及心得体会」 |
| eval-1 组会 PPT | **6/6** | 5/6 | 页标题：技能版为结论句（`RMSE 由 2.31% 降到 1.44%`），基线为栏目名（`07 实验设置`、`08 实验结果`） |
| eval-2 论文（LaTeX） | **6/6** | 未跑（成本考量） | 编译零 error / 零 undefined ref / Overfull 0、引用均为真实出版物、封面用占位身份；**并暴露包内 `create_report.py` 路径 bug（已修）** |
| eval-3 规划（不产出文件） | 4/5 | 4/5 | **打平**：技能独有「跨路线衔接指引」；基线独有「联网核查 UESTC 官方规定并附出处」。「不产出文件」基线同样满足 → 不具区分度 |

**结论（按路线看增量，而不是笼统说"有用"）**：

| 路线 | 技能增量 | 原因 |
|---|---|---|
| B 实验报告 | **大**（骨架 12/12 vs 5/12） | 存在**硬性、可核验**的院校格式 |
| C 课程论文 | **大**（编译零 error、引用规范、占位合规） | 同上，且有 LaTeX 模板与 GB/T 7714 |
| A 汇报 PPT | 中（仅标题风格） | 官方模板是**公开资产**，基线自行找到 → 护城河不在素材 |
| D 分期规划 | **≈0** | 属通用建议，强模型本就擅长；且会更主动联网核查 |

**一句话**：技能的护城河 = **制度性硬格式的合规化**（骨架/格式参数/引用规范/检查清单）。凡属"通用建议质量"的战场（规划），技能没有优势；凡有官方模板可循的战场（模板素材），优势会被公开资产的可得性抵消。据此，投入应优先 B、C 两条路线。
