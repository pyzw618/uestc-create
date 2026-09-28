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
| eval-2 论文（LaTeX） | 未跑 | 未跑 | API 余额不足（HTTP 402）中断 |
| eval-3 规划（不产出文件） | 未跑 | 未跑 | 同上 |

**结论**：技能的真实增量集中在**结构合规与撰写纪律**（骨架、标题、语气、检查清单），而非原始内容生成能力——两个 arm 都能产出可用内容，但只有技能版满足成电的交付规范。
