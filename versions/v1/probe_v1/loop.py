"""The whole mechanism: one experimenter, one small job per call, in a loop.

learn step:  PROPOSE one experiment -> run it on the box -> score the model's prediction of it
             -> if the model was wrong: REVISE the model -> keep the new version only if it fits the notebook
                at least as well as the old one (checked by replaying every experiment, in code)
solve step:  for a goal, propose candidate probes -> the model simulates them for free -> run the most promising
             one for real -> it goes into the notebook like any experiment (and can trigger a revision)

Two numbers say whether it is learning, both computed by code, never by the LLM:
    fit      share of the notebook the current model predicts
    heldout  share of a fixed set of random probes (never shown to the experimenter) it predicts
"""
from __future__ import annotations

import csv
import json
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path

from probe_v1 import prompts as P
from probe_v1.memory import Library, Model, Notebook
from probe_v1.simulate import predict_many

OK = 0.999  # a match at or above this counts as "the model got it right"


@dataclass
class Config:
    steps: int = 30          # learn steps
    tasks: int = 0           # solve-mode goals after learning
    tries: int = 3           # real attempts per goal
    candidates: int = 5      # candidate probes per solve step
    retries: int = 1         # extra revise attempts when a new model fits worse
    heldout: int = 100       # size of the held-out test set
    seed: int = 0


def parse_json(text):
    blocks = re.findall(r"```json\s*(.*?)```", text, re.S)
    for b in reversed(blocks):
        try:
            return json.loads(b)
        except Exception:
            pass
    dec = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                return dec.raw_decode(text[i:])[0]
            except Exception:
                continue
    return None


def parse_code(text):
    blocks = re.findall(r"```python\s*(.*?)```", text, re.S)
    return blocks[-1] if blocks else None


class Run:
    def __init__(self, env, folder, llm, cfg: Config, knowledge_files=(), log=print):
        self.env, self.llm, self.cfg, self.log = env, llm, cfg, log
        self.dir = Path(folder)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.notebook, self.model = Notebook(self.dir), Model(self.dir)
        self.library = Library(getattr(env, "knowledge", ""), knowledge_files)
        self.rng = random.Random(cfg.seed)
        self.calls = sum(1 for _ in open(self.dir / "calls.jsonl")) if (self.dir / "calls.jsonl").exists() else 0
        self._heldout_set()
        # the current model's predictions on the notebook (recomputed on resume)
        self.preds, _ = predict_many(self.model.code, self.notebook.probes())
        self.model.matches = [self.env.compare(p, e["observation"]) for p, e in zip(self.preds, self.notebook.entries)]
        self.model.fit = sum(m >= OK for m in self.model.matches) / max(1, len(self.model.matches))

    @staticmethod
    def mean(matches):
        return sum(matches) / len(matches) if matches else 0.0

    # ----------------------------------------------------------------------------------------- bookkeeping
    def _heldout_set(self):
        path = self.dir / "heldout.json"
        if path.exists():
            self.heldout = json.loads(path.read_text())
            return
        rng = random.Random(10_000 + self.cfg.seed)
        probes = [p for p in (self.env.random_probe(rng) for _ in range(self.cfg.heldout)) if p is not None]
        self.heldout = [{"probe": p, "observation": self.env.probe(p)} for p in probes]
        path.write_text(json.dumps(self.heldout))

    def heldout_score(self, code):
        if not self.heldout:
            return None
        preds, _ = predict_many(code, [h["probe"] for h in self.heldout])
        return sum(self.env.compare(p, h["observation"]) >= OK for p, h in zip(preds, self.heldout)) / len(self.heldout)

    def call(self, job, user, temperature=0.7):
        r = self.llm(P.SYSTEM, user, temperature)
        self.calls += 1
        with (self.dir / "calls.jsonl").open("a") as f:
            f.write(json.dumps({"n": self.calls, "job": job, "time": time.time(), "prompt": user, **r}) + "\n")
        return r["text"]

    def curve(self, step, kind, extra=""):
        path = self.dir / "curve.csv"
        new = not path.exists()
        with path.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["step", "kind", "experiments", "model_version", "fit", "heldout", "llm_calls", "note"])
            h = "" if self.model.heldout is None else f"{self.model.heldout:.3f}"
            w.writerow([step, kind, len(self.notebook), self.model.version, f"{self.model.fit:.3f}", h, self.calls, extra])

    def context(self):
        return P.context(self.env, self.library, self.notebook, self.model, self.preds)

    def check_probe(self, p):
        if not isinstance(p, dict):
            return "the probe must be a JSON object"
        try:
            return self.env.validate(p)
        except Exception as e:
            return f"invalid probe: {e}"

    # ------------------------------------------------------------------------------------------ one experiment
    def run_experiment(self, kind, question, probe, expect=""):
        obs = self.env.probe(probe)
        [pred], err = predict_many(self.model.code, [probe])
        match = self.env.compare(pred, obs)
        e = self.notebook.add({"kind": kind, "question": question, "expect": expect, "probe": probe,
                               "observation": obs, "model_version": self.model.version, "model_prediction": pred,
                               "match": match, "model_error": err})
        self.preds.append(pred)
        self.model.matches.append(match)
        self.model.fit = sum(m >= OK for m in self.model.matches) / len(self.model.matches)
        return e

    def learn_step(self, step):
        user = self.context() + "\n\n" + P.PROPOSE
        for attempt in range(3):
            reply = parse_json(self.call("propose", user)) or {}
            probe = reply.get("probe")
            err = self.check_probe(probe)
            if not err:
                break
            user += f"\n\nYour last reply was not usable: {err}. Try again."
        else:
            self.log(f"[{step}] no valid probe after 3 tries; skipping")
            return
        e = self.run_experiment("learn", reply.get("question", ""), probe, reply.get("expect", ""))
        self.log(f"[{step}] {e['id']} {P.clip(e['question'], 90)}  model v{self.model.version} match {e['match']:.2f}")
        if e["match"] < OK:
            self.revise(e)
        self.curve(step, "learn", e["id"])

    # ------------------------------------------------------------------------------------------ model update
    def revise(self, e):
        # accept rule: average match over the notebook (partial credit), so half-right beats empty
        old_fit, old_mean = self.model.fit, self.mean(self.model.matches)
        retry = ""
        for attempt in range(1 + self.cfg.retries):
            user = self.context() + "\n\n" + P.REVISE.format(
                exp_id=e["id"], question=e["question"], probe=P.clip(e["probe"], 800),
                observation=P.clip(e["observation"], 1500), prediction=P.clip(e["model_prediction"], 1000),
                version=e["model_version"], match=e["match"], retry=retry,
                error=f"(predict() raised an error: {e['model_error']})\n" if e.get("model_error") else "")
            text = self.call("revise", user, temperature=0.4)
            meta, code = parse_json(text) or {}, parse_code(text)
            if meta.get("keep") or not code:
                self.log(f"      model kept (v{self.model.version})")
                return
            preds, err = predict_many(code, self.notebook.probes())
            matches = [self.env.compare(p, x["observation"]) for p, x in zip(preds, self.notebook.entries)]
            fit = sum(m >= OK for m in matches) / len(matches)
            mean = self.mean(matches)
            if mean >= old_mean and "def predict" in code:
                beliefs = [str(b) for b in meta.get("beliefs", [])] or self.model.beliefs
                self.model.replace(beliefs, code, meta.get("notes", ""), fit, matches, self.heldout_score(code),
                                   made_at=len(self.notebook))
                self.preds = preds
                h = "-" if self.model.heldout is None else f"{self.model.heldout:.0%}"
                self.log(f"      model v{self.model.version}: fit {fit:.0%} (was {old_fit:.0%}), mean match "
                         f"{mean:.2f} (was {old_mean:.2f}), held-out {h}")
                return
            newly_wrong = [x["id"] for x, m, o in zip(self.notebook.entries, matches, self.model.matches)
                           if m < OK <= o][:12]
            retry = (f"\nYOUR PREVIOUS ATTEMPT WAS REJECTED: its average match over the notebook is {mean:.2f}, the "
                     f"current model's is {old_mean:.2f}. It got these right before and wrong now: {', '.join(newly_wrong) or '-'}."
                     + (f" Error: {err}" if err else "") + " Fix that.\n")
            self.log(f"      revision rejected: mean match {mean:.2f} < {old_mean:.2f}")

    # ------------------------------------------------------------------------------------------ goals
    def solve(self, n, k, task):
        tried = []
        for t in range(self.cfg.tries):
            history = ("\nYour earlier real attempts at this goal, which failed:\n" + "\n".join(tried) + "\n") if tried else ""
            reply = parse_json(self.call("solve", self.context() + "\n\n" + P.SOLVE.format(
                task=task.description, k=k, history=history))) or {}
            cands = [c for c in (reply.get("candidates") or [])[:k] if not self.check_probe(c)]
            if not cands:
                continue
            preds, _ = predict_many(self.model.code, cands)
            chosen = next((c for c, p in zip(cands, preds) if _safe_check(task, p)), cands[0])
            e = self.run_experiment("goal", f"goal {n}: {task.description[:80]} | {reply.get('question', '')}", chosen)
            ok = _safe_check(task, e["observation"])
            self.log(f"[goal {n} try {t + 1}] {e['id']} {'REACHED' if ok else 'missed'} (model match {e['match']:.2f})")
            if e["match"] < OK:
                self.revise(e)
            self.curve(f"goal{n}", "goal", f"{e['id']} {'reached' if ok else 'missed'}")
            if ok:
                return t + 1
            tried.append(f"- {e['id']}: {P.clip(chosen, 300)} -> {P.clip(e['observation'], 400)}")
        return None

    # ------------------------------------------------------------------------------------------ main
    def go(self):
        start = len([e for e in self.notebook.entries if e["kind"] == "learn"])
        self.log(f"Helix Probe on '{self.env.name}': {start} experiments so far, model v{self.model.version}, "
                 f"held-out set of {len(self.heldout)}")
        for step in range(start + 1, start + self.cfg.steps + 1):
            self.learn_step(step)
        results = []
        if self.cfg.tasks:
            tasks = self.env.make_tasks(random.Random(20_000 + self.cfg.seed + len(self.notebook)), self.cfg.tasks)
            for i, task in enumerate(tasks, 1):
                results.append(self.solve(i, self.cfg.candidates, task))
        summary = {"env": self.env.name, "experiments": len(self.notebook), "model_version": self.model.version,
                   "fit": self.model.fit, "heldout": self.model.heldout, "llm_calls": self.calls,
                   "goals": {"tried": len(results), "reached": sum(r is not None for r in results),
                             "tries_used": results},
                   "beliefs": self.model.beliefs}
        (self.dir / "summary.json").write_text(json.dumps(summary, indent=1))
        self.log(json.dumps({k: v for k, v in summary.items() if k != "beliefs"}))
        return summary


def _safe_check(task, obs):
    try:
        return bool(obs) and bool(task.check(obs))
    except Exception:
        return False
