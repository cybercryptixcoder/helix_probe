"""The mechanism: three roles in series, one call at a time, around a box that is the only judge.

start        draw `exam` random probes from the box, run them, seal the results (no LLM ever sees them)
learn step   EXPERIMENTER proposes one probe -> run on the box -> the current model predicts it (before seeing it)
             -> if wrong: UPDATER revises the model
             -> every `theorist_every` steps, or after the updater fails twice running: THEORIST writes a model
                from the evidence alone
goal step    candidates -> the model simulates them for free -> the best is run for real -> notebook

Every candidate model is scored by code on the whole notebook and on the exam, and replaces the current model
only if it is better in this order: exam (evidence it was never fitted to), then fit (the notebook), then size.

The numbers that say whether it is learning, all computed by code:
    exam      average match on the sealed probes          (the agents see this: their sense of progress)
    arrival   share of experiments predicted correctly before their result was seen
    fit       average match on the notebook
    size      characters of model code, comments excluded
    heldout   share of a separate set of random probes predicted exactly. Measurement only: no role ever sees
              it, and nothing in the loop uses it.
"""
from __future__ import annotations

import csv
import json
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe import prompts as P
from probe.memory import Library, Model, Notebook, code_size
from probe.simulate import predict_many

OK = 0.999  # a match at or above this counts as right


@dataclass
class Config:
    steps: int = 30              # learn steps (one experiment each)
    exam: int = 6                # sealed probes drawn at the start (0 = no exam)
    theorist_every: int = 6      # learn steps between theorist calls (0 = never)
    theorist_on_stall: int = 2   # call the theorist after this many updater failures in a row (0 = never)
    retries: int = 1             # extra updater attempts when a revision isn't kept
    stop_after: int = 8          # stop learning once this many experiments in a row were predicted on arrival and
                                 # the exam is perfect (0 = never stop early)
    experimenter: str = "llm"    # "llm", or "random" (a baseline: probes from the box's random_probe)
    random_every: int = 2        # with "llm": every k-th learn step (1st, 3rd, ...) is a random probe from the box
                                 # instead: representative coverage next to targeted questions (0 = never)
    tasks: int = 0               # goals to attempt after learning
    tries: int = 3               # real attempts per goal
    candidates: int = 5          # candidate probes per goal attempt
    heldout: int = 100           # size of the measurement-only held-out set
    seed: int = 0
    effort: dict = field(default_factory=lambda: {"experimenter": "none", "updater": "none", "theorist": "none"})
    temperature: dict = field(default_factory=lambda: {"experimenter": 0.7, "updater": 0.4, "theorist": 0.6})


def parse_json(text):
    for b in reversed(re.findall(r"```json\s*(.*?)```", text, re.S)):
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


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


class Run:
    def __init__(self, env, folder, llm, cfg: Config, knowledge_files=(), log=print, should_stop=lambda: False):
        self.env, self.llm, self.cfg, self.log, self.should_stop = env, llm, cfg, log, should_stop
        self.dir = Path(folder)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.notebook, self.model = Notebook(self.dir), Model(self.dir)
        self.library = Library(getattr(env, "knowledge", ""), knowledge_files)
        self.rng = random.Random(cfg.seed + 7919 * len(self.notebook))
        self.calls = sum(1 for _ in open(self.dir / "calls.jsonl")) if (self.dir / "calls.jsonl").exists() else 0
        self.exam = self._sealed("exam.json", cfg.exam, 30_000 + cfg.seed)
        self.heldout = self._sealed("heldout.json", cfg.heldout, 10_000 + cfg.seed)
        self.stall = 0
        s = self.score(self.model.code)          # rescore on resume: the notebook may have grown since the save
        self.preds = s["preds"]
        for k in ("exam", "fit", "fit_exact", "size", "matches"):
            setattr(self.model, k, s[k])
        if self.model.heldout is None:
            self.model.heldout = self.heldout_score(self.model.code)

    # --------------------------------------------------------------------------------------------- scoring
    def _sealed(self, name, n, seed):
        path = self.dir / name
        if path.exists():
            return json.loads(path.read_text())
        rng = random.Random(seed)
        probes = [p for p in (self.env.random_probe(rng) for _ in range(n)) if p is not None] if n else []
        out = [{"probe": p, "observation": self.env.probe(p)} for p in probes]
        path.write_text(json.dumps(out))
        return out

    def score(self, code):
        """Everything code knows about a model: predictions, matches, exam, fit, size. One sandbox call."""
        nb = self.notebook.entries
        probes = [e["probe"] for e in nb] + [x["probe"] for x in self.exam]
        preds, err = predict_many(code, probes)
        matches = [self.env.compare(p, e["observation"]) for p, e in zip(preds[:len(nb)], nb)]
        exam = [self.env.compare(p, x["observation"]) for p, x in zip(preds[len(nb):], self.exam)]
        return {"preds": preds[:len(nb)], "matches": matches, "fit": mean(matches),
                "fit_exact": mean([m >= OK for m in matches]), "exam": mean(exam), "size": code_size(code),
                "error": err}

    def heldout_score(self, code):
        if not self.heldout:
            return None
        preds, _ = predict_many(code, [h["probe"] for h in self.heldout])
        return mean([self.env.compare(p, h["observation"]) >= OK for p, h in zip(preds, self.heldout)])

    @staticmethod
    def better(new, cur, eps=1e-9):
        """Exam first (evidence never fitted to), then fit, then size."""
        for k in ("exam", "fit"):
            if new[k] > cur[k] + eps:
                return True, f"{k} {cur[k]:.3f} -> {new[k]:.3f}"
            if new[k] < cur[k] - eps:
                return False, f"its {k} is {new[k]:.3f}, the current model's is {cur[k]:.3f}"
        if new["size"] < cur["size"]:
            return True, f"same scores, smaller ({cur['size']} -> {new['size']} chars)"
        return False, f"same scores and not smaller ({new['size']} vs {cur['size']} chars)"

    def current(self):
        return {k: getattr(self.model, k) for k in ("exam", "fit", "size")}

    def offer(self, code, role, notes):
        """A candidate model. Returns (kept, reason, scores)."""
        if not code or "def predict" not in code:
            return False, "no predict() in the reply", None
        s = self.score(code)
        kept, why = self.better(s, self.current())
        if kept:
            self.model.replace(code, role, notes, s, len(self.notebook), self.heldout_score(code))
            self.preds = s["preds"]
            h = "-" if self.model.heldout is None else f"{self.model.heldout:.0%}"
            self.log(f"      model v{self.model.version} by the {role}: exam {s['exam']:.2f}, fit {s['fit']:.2f}, "
                     f"size {s['size']} ({why}); held-out {h}")
        else:
            self.log(f"      {role}'s model not kept: {why}")
        self._trace("offers.jsonl", {"role": role, "kept": kept, "why": why, "made_at": len(self.notebook),
                                     "exam": s["exam"], "fit": s["fit"], "size": s["size"], "error": s["error"],
                                     "code": code})
        return kept, why, s

    # --------------------------------------------------------------------------------------------- calls and logs
    def call(self, role, system, user):
        r = self.llm(system, user, temperature=self.cfg.temperature[role], effort=self.cfg.effort[role])
        self.calls += 1
        self._trace("calls.jsonl", {"n": self.calls, "role": role, "time": time.time(), "system": system,
                                    "prompt": user, **r})
        return r["text"]

    def _trace(self, name, row):
        with (self.dir / name).open("a") as f:
            f.write(json.dumps(row) + "\n")

    def curve(self, step, kind, note=""):
        path = self.dir / "curve.csv"
        new = not path.exists()
        learn = [e for e in self.notebook.entries if e["kind"] == "learn"]
        with path.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["step", "kind", "experiments", "box_probes", "model_version", "model_role", "exam", "fit",
                            "size", "arrival_last10", "heldout", "llm_calls", "note"])
            h = "" if self.model.heldout is None else f"{self.model.heldout:.3f}"
            arr = mean([e["match"] >= OK for e in learn[-10:]])
            w.writerow([step, kind, len(self.notebook), len(self.notebook) + len(self.exam), self.model.version,
                        self.model.role, f"{self.model.exam:.3f}", f"{self.model.fit:.3f}", self.model.size,
                        f"{arr:.2f}", h, self.calls, note])

    def context(self):
        return P.context(self.env, self.library, self.notebook, self.model, self.preds, len(self.exam))

    def check_probe(self, p):
        if not isinstance(p, dict):
            return "the probe must be a JSON object"
        try:
            return self.env.validate(p)
        except Exception as e:
            return f"invalid probe: {e}"

    # --------------------------------------------------------------------------------------------- the roles
    def run_experiment(self, kind, question, probe, expect=""):
        obs = self.env.probe(probe)
        [pred], err = predict_many(self.model.code, [probe])
        match = self.env.compare(pred, obs)
        e = self.notebook.add({"kind": kind, "question": question, "expect": expect, "probe": probe,
                               "observation": obs, "model_version": self.model.version, "model_prediction": pred,
                               "match": match, "model_error": err})
        self.preds.append(pred)
        self.model.matches.append(match)
        self.model.fit = mean(self.model.matches)
        self.model.fit_exact = mean([m >= OK for m in self.model.matches])
        return e

    def propose(self, step=0):
        k = self.cfg.random_every
        if self.cfg.experimenter == "random" or (k and step % k == 1 % k):
            for _ in range(20):
                p = self.env.random_probe(self.rng)
                if p not in self.notebook.probes():
                    return {"question": "a random ordinary probe", "probe": p, "expect": ""}
            return {"question": "a random ordinary probe", "probe": p, "expect": ""}
        user = self.context() + "\n\n" + P.PROPOSE
        for _ in range(3):
            reply = parse_json(self.call("experimenter", P.EXPERIMENTER, user)) or {}
            err = self.check_probe(reply.get("probe"))
            if not err:
                return reply
            user += f"\n\nYour last reply was not usable: {err}. Try again."
        return None

    def update(self, e):
        retry = ""
        for _ in range(1 + self.cfg.retries):
            user = self.context() + "\n\n" + P.REVISE.format(
                exp_id=e["id"], question=e["question"], probe=P.clip(e["probe"], 1000),
                observation=P.clip(e["observation"], 1500), prediction=P.clip(e["model_prediction"], 1200),
                version=e["model_version"], match=e["match"], rules=P.MODEL_RULES, retry=retry,
                error=f"(predict() raised an error: {e['model_error']})\n" if e.get("model_error") else "")
            text = self.call("updater", P.UPDATER, user)
            code = parse_code(text)
            if (not code and "KEEP" in text) or (code and code.strip() == self.model.code.strip()):
                self.log("      updater: keep")
                return False
            kept, why, s = self.offer(code, "updater", text.split("```")[-1].strip()[:400])
            if kept:
                return True
            broke = ""
            if s:
                broke = [x["id"] for x, m, o in zip(self.notebook.entries, s["matches"], self.model.matches)
                         if m < OK <= o][:12]
                broke = f" It got these right before and wrong now: {', '.join(broke)}." if broke else ""
                broke += f" Error: {s['error']}" if s.get("error") else ""
            retry = P.RETRY.format(why=f"Compared with the current model, {why}.{broke}")
        return False

    def theorize(self):
        user = P.evidence(self.env, self.library, self.notebook) + "\n\n" + P.THEORIZE.format(rules=P.MODEL_RULES)
        text = self.call("theorist", P.THEORIST, user)
        kept, _, _ = self.offer(parse_code(text), "theorist", text.split("```")[-1].strip()[:400])
        return kept

    def learn_step(self, step):
        reply = self.propose(step)
        if reply is None:
            self.log(f"[{step}] no usable probe after 3 tries; step skipped")
            return
        e = self.run_experiment("learn", reply.get("question", ""), reply["probe"], reply.get("expect", ""))
        self.log(f"[{step}] {e['id']} {P.clip(e['question'], 90)}  (v{e['model_version']} predicted it: "
                 f"match {e['match']:.2f})")
        if e["match"] < OK:
            self.stall = 0 if self.update(e) else self.stall + 1
        due = self.cfg.theorist_every and step % self.cfg.theorist_every == 0
        stalled = self.cfg.theorist_on_stall and self.stall >= self.cfg.theorist_on_stall
        if due or stalled:
            self.log(f"      theorist ({'every ' + str(self.cfg.theorist_every) + ' steps' if due else 'updater stalled'})")
            if self.theorize() or stalled:
                self.stall = 0
        self.curve(step, "learn", e["id"])

    def settled(self):
        k = self.cfg.stop_after
        learn = [e for e in self.notebook.entries if e["kind"] == "learn"]
        return bool(k) and len(learn) >= k and all(e["match"] >= OK for e in learn[-k:]) \
            and (not self.exam or self.model.exam >= OK)

    def solve(self, n, task):
        tried = []
        for t in range(self.cfg.tries):
            history = ("\nYour earlier real attempts at this goal, which failed:\n" + "\n".join(tried) + "\n") if tried else ""
            reply = parse_json(self.call("experimenter", P.EXPERIMENTER, self.context() + "\n\n" + P.SOLVE.format(
                task=task.description, k=self.cfg.candidates, history=history))) or {}
            cands = [c for c in (reply.get("candidates") or [])[:self.cfg.candidates] if not self.check_probe(c)]
            if not cands:
                continue
            preds, _ = predict_many(self.model.code, cands)
            chosen = next((c for c, p in zip(cands, preds) if _safe_check(task, p)), cands[0])
            e = self.run_experiment("goal", f"goal {n}: {task.description[:80]} | {reply.get('question', '')}", chosen)
            ok = _safe_check(task, e["observation"])
            self.log(f"[goal {n} try {t + 1}] {e['id']} {'REACHED' if ok else 'missed'} (model match {e['match']:.2f})")
            if e["match"] < OK:
                self.update(e)
            self.curve(f"goal{n}", "goal", f"{e['id']} {'reached' if ok else 'missed'}")
            if ok:
                return t + 1
            tried.append(f"- {e['id']}: {P.clip(chosen, 300)} -> {P.clip(e['observation'], 400)}")
        return None

    def go(self):
        done = len([e for e in self.notebook.entries if e["kind"] == "learn"])
        self.log(f"Helix Probe v2 on '{self.env.name}': {done} experiments so far, model v{self.model.version}, "
                 f"exam of {len(self.exam)}, held-out set of {len(self.heldout)}")
        for step in range(done + 1, self.cfg.steps + 1):
            if self.should_stop():
                self.log(f"stop requested: stopping after step {step - 1}; run again to continue")
                return None
            if self.settled():
                self.log(f"stopping early: the last {self.cfg.stop_after} experiments were all predicted on arrival"
                         + (" and the exam is perfect" if self.exam else ""))
                break
            self.learn_step(step)
        results = []
        if self.cfg.tasks and not (self.dir / "summary.json").exists():
            tasks = self.env.make_tasks(random.Random(20_000 + self.cfg.seed), self.cfg.tasks)
            results = [self.solve(i, t) for i, t in enumerate(tasks, 1)]
        summary = {"env": self.env.name, "experiments": len(self.notebook), "exam_probes": len(self.exam),
                   "model_version": self.model.version, "model_role": self.model.role, "exam": self.model.exam,
                   "fit": self.model.fit, "size": self.model.size, "heldout": self.model.heldout,
                   "llm_calls": self.calls, "goals": {"tried": len(results),
                                                      "reached": sum(r is not None for r in results),
                                                      "tries_used": results}}
        (self.dir / "summary.json").write_text(json.dumps(summary, indent=1))
        self.log(json.dumps(summary))
        return summary


def _safe_check(task, obs):
    try:
        return bool(obs) and bool(task.check(obs))
    except Exception:
        return False
