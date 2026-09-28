#!/usr/bin/env python3
"""触发评测（Windows 可用的替代版）。

skill-creator 上游 run_eval.py 用 select() 读管道，Windows 上不支持
（WinError 10038），导致所有查询恒判"未触发"。本脚本改为**阻塞读到 EOF +
看门狗线程超时**，在 Windows 上可靠工作。

机制：把技能描述写成一个命令 shim（.claude/commands/<name>.md），再跑
`claude -p <query>`，从 stream-json 的 assistant 消息里检测模型是否用
Skill/Read 工具调用了该 shim。

用法：
  python run_trigger_eval.py --eval-set trigger-eval.json --skill-path <包根>
      [--description "覆盖描述"] [--model sonnet] [--runs-per-query 2]
      [--workers 3] [--timeout 180] [--json-out results.json]

**并发警告**：每次 `claude -p` 启动都要加载全部插件与 hook，很重（单次几十秒）。
并发过高（实测 workers=6 + timeout=90）会**全部超时**，表现为"所有查询 rate=0.0"
的假象——包括本该触发的。建议 workers ≤ 3、timeout ≥ 180；脚本会打印非正常结束数。
退出码 0。
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def skill_description(skill_path):
    text = io.open(Path(skill_path) / "SKILL.md", encoding="utf-8").read()
    m = re.search(r"^description:\s*(.+?)$", text, re.M | re.S)
    if not m:
        raise SystemExit("SKILL.md 未找到 description")
    d = m.group(1).strip()
    if d.startswith('"') and d.endswith('"'):
        d = d[1:-1]
    return d


def run_one(query, shim_name, cwd, model, timeout):
    """返回 (triggered, status)。status ∈ ok / timeout / error / empty。"""
    cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose"]
    if model:
        cmd += ["--model", model]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         cwd=cwd, env=env)

    timed_out = {"v": False}

    def watchdog():
        timed_out["v"] = True
        try:
            p.kill()
        except Exception:
            pass

    t = threading.Timer(timeout, watchdog)
    t.start()
    try:
        out, err = p.communicate()
    finally:
        t.cancel()

    if timed_out["v"]:
        return False, "timeout"
    if not out:
        return False, "error:" + (err or b"")[-120:].decode("utf-8", "replace")

    triggered = False
    saw_assistant = False
    for line in (out or b"").decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            saw_assistant = True
        for item in ev.get("message", {}).get("content", []) if ev.get("type") == "assistant" else []:
            if item.get("type") != "tool_use":
                continue
            name, inp = item.get("name"), item.get("input", {}) or {}
            if name == "Skill" and shim_name in str(inp.get("skill", "")):
                triggered = True
            elif name == "Read" and shim_name in str(inp.get("file_path", "")):
                triggered = True
    return triggered, ("ok" if saw_assistant else "empty")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-set", required=True)
    ap.add_argument("--skill-path", required=True)
    ap.add_argument("--description", default=None)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--runs-per-query", type=int, default=1)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()

    desc = a.description or skill_description(a.skill_path)
    items = json.load(io.open(a.eval_set, encoding="utf-8"))

    skill_name = Path(a.skill_path).name
    shim_name = f"{skill_name}-skill-{uuid.uuid4().hex[:8]}"
    cmd_dir = Path.cwd() / ".claude" / "commands"
    cmd_dir.mkdir(parents=True, exist_ok=True)
    shim = cmd_dir / f"{shim_name}.md"
    # 清掉历史遗留的同类 shim：上游 run_eval 或中断的运行可能没清理。残留 shim 会让
    # 模型调用到旧的那个，而检测器只认本轮名 → 假阴性（实测已踩到）。
    for stale in cmd_dir.glob(f"{skill_name}-skill-*.md"):
        stale.unlink()
    indented = "\n  ".join(desc.split("\n"))
    shim.write_text(f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n",
                    encoding="utf-8")

    jobs = [(it, r) for it in items for r in range(a.runs_per_query)]
    results = []
    try:
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = {ex.submit(run_one, it["query"], shim_name, str(Path.cwd()),
                              a.model, a.timeout): it for it, _ in jobs}
            for f, it in futs.items():
                pass
            from concurrent.futures import as_completed
            per_query = {}
            problems = []
            for f in as_completed(futs):
                it = futs[f]
                q = it["query"]
                try:
                    trg, st = f.result()
                except Exception as e:
                    trg, st = False, "exc:%s" % e
                per_query.setdefault(q, []).append(trg)
                if st != "ok":
                    problems.append("%s ← %s" % (q[:24], st))
            if problems:
                print("⚠ 非正常结束 %d/%d：" % (len(problems), len(jobs)))
                for p in problems[:8]:
                    print("   ", p)
        for it in items:
            q = it["query"]
            trs = per_query.get(q, [False])
            rate = sum(trs) / len(trs)
            should = it["should_trigger"]
            ok = rate >= 0.5 if should else rate < 0.5
            results.append({"query": q, "should_trigger": should,
                            "trigger_rate": round(rate, 3), "pass": ok})
    finally:
        for stale in cmd_dir.glob(f"{skill_name}-skill-*.md"):
            stale.unlink()

    passed = sum(1 for r in results if r["pass"])
    print(f"description: {desc[:80]}...")
    print(f"{'✓' if passed == len(results) else '·'} 通过 {passed}/{len(results)}")
    for r in results:
        mark = "✓" if r["pass"] else "✗"
        print(f"  {mark} rate={r['trigger_rate']:<5} should={str(r['should_trigger']):<5} {r['query']}")
    summary = {"description": desc, "passed": passed, "total": len(results),
               "results": results}
    if a.json_out:
        io.open(a.json_out, "w", encoding="utf-8").write(
            json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
