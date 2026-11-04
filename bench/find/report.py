"""Summarise a FIND job: every arm, every category, against FIND's published agents. Writes report.md + report.json.

    python bench/find/report.py results/find/x
"""
from __future__ import annotations

import json
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bench.find.curve import at, curve  # noqa: E402

PRICE_IN, PRICE_CACHED, PRICE_OUT = 0.30e-6, 0.006e-6, 1.20e-6   # DeepSeek's list price for V4.1 Flash, USD/token


def published_budget(agent, cat, fid):
    """Experiments (PYTHON calls) and inputs a published FIND agent used on one function."""
    p = ROOT / "bench" / "find" / "published" / agent / cat / fid / "history.json"
    if not p.exists():
        return None
    calls = []
    for m in json.loads(p.read_text()):
        if m.get("role") == "assistant":
            calls += re.findall(r"PYTHON\(([^)]*)\)", m.get("content", ""))
    return len(calls), sum(max(0, len(c.split()) - 1) for c in calls)


def run_cost(folder: Path):
    p_in = p_cached = p_out = n = 0
    if (folder / "calls.jsonl").exists():
        for line in (folder / "calls.jsonl").read_text().splitlines():
            try:
                u = json.loads(line).get("usage") or {}
            except json.JSONDecodeError:
                continue
            n += 1
            p_in += u.get("prompt_tokens", 0)
            p_cached += (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
            p_out += u.get("completion_tokens", 0)
    usd = (p_in - p_cached) * PRICE_IN + p_cached * PRICE_CACHED + p_out * PRICE_OUT
    return {"calls": n, "tokens_in": p_in, "tokens_out": p_out, "usd": usd}


def fmt(x, d=2):
    return "-" if x is None else f"{x:.{d}f}"


def main(job):
    job = Path(job)
    cfg = json.loads((job / "job.json").read_text())
    data = ROOT / cfg["data"]
    sample = json.loads((data / "sample.json").read_text())
    main_sample = data.resolve() == (ROOT / "bench" / "find" / "data").resolve()
    published = json.loads((ROOT / "bench/find/published_scores.json").read_text()) if main_sample else {}
    rows, per_fn = {}, []
    for arm_dir in sorted(p for p in job.iterdir() if p.is_dir()):
        for cat in cfg["categories"]:
            for fid in sample[cat]:
                folder = arm_dir / f"{cat}_{fid}"
                if not (folder / "summary.json").exists():
                    continue
                c = curve(folder)
                s = json.loads((folder / "summary.json").read_text())
                cost = run_cost(folder)
                r = {"arm": arm_dir.name, "category": cat, "fid": fid, "final": c["final"], "at3": at(c, 3),
                     "at10": at(c, 10), "experiments": s["experiments"], "exam_probes": c["exam_probes"],
                     "inputs": c.get("inputs_total", 0), "heldout": s.get("heldout"), **cost}
                per_fn.append(r)
                rows.setdefault((arm_dir.name, cat), []).append(r)
    table = []
    for (arm, cat), rs in sorted(rows.items()):
        table.append({"who": arm, "category": cat, "n": len(rs), "final": st.mean(r["final"] for r in rs),
                      "at3": st.mean(r["at3"] for r in rs), "at10": st.mean(r["at10"] for r in rs),
                      "experiments": st.mean(r["experiments"] for r in rs),
                      "inputs": st.mean(r["inputs"] for r in rs), "calls": st.mean(r["calls"] for r in rs),
                      "usd": sum(r["usd"] for r in rs),
                      "heldout": st.mean(r["heldout"] for r in rs if r["heldout"] is not None)
                      if any(r["heldout"] is not None for r in rs) else None})
    for agent, cats in published.items():
        for cat, d in cats.items():
            fids = [f for f in sample[cat] if f in d]
            b = [published_budget(agent, cat, f) for f in fids]
            b = [x for x in b if x]
            table.append({"who": f"published: {agent}", "category": cat, "n": len(fids),
                          "final": st.mean(d[f]["score"] for f in fids), "at3": None, "at10": None,
                          "experiments": st.mean(x[0] for x in b) if b else None,
                          "inputs": st.mean(x[1] for x in b) if b else None, "calls": None, "usd": None,
                          "heldout": None})
    lines = [f"# FIND results: {job.name}", "",
             f"Sample: `{cfg['data']}`; up to {cfg['steps']} learn steps per function; exam of {cfg['exam']} probes "
             "(v2 arms). Scores are FIND's official code-based metrics: numeric = share of functions with normalised "
             "error < 0.1 on x in [-127.5, 127.5]; strings = share of FIND's test pairs reproduced exactly. "
             "`at 3` / `at 10` = the score of the model each run had after 3 / 10 experiments (FIND's GPT-4 agent "
             "used a median of about 3). `experiments` excludes the exam, which adds "
             f"{cfg['exam']} probes per v2 run; `inputs` is every value sent to the function, exam included. "
             "Cost at DeepSeek's list price.", ""]
    for cat in cfg["categories"]:
        lines += [f"## {cat}", "", "| who | n | final | at 3 | at 10 | experiments | inputs | LLM calls | cost | held-out |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for t in sorted((t for t in table if t["category"] == cat), key=lambda t: -t["final"]):
            lines.append(f"| {t['who']} | {t['n']} | **{fmt(t['final'])}** | {fmt(t['at3'])} | {fmt(t['at10'])} | "
                         f"{fmt(t['experiments'], 1)} | {fmt(t['inputs'], 0)} | {fmt(t['calls'], 0)} | "
                         f"{'-' if t['usd'] is None else '$%.2f' % t['usd']} | {fmt(t['heldout'])} |")
        lines.append("")
    (job / "report.md").write_text("\n".join(lines))
    (job / "report.json").write_text(json.dumps({"table": table, "per_function": per_fn}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
