"""The mechanism: three roles in series, one call at a time, around a box that is the only judge.

each step
  1. ACT      if the box has a goal and some plan reaches it in the current model, try the shortest such plan
              (the planner: plain code, the model as a simulator, no LLM call, no real action spent searching);
              otherwise the EXPERIMENTER picks one experiment (every `random_every`-th step a random one instead)
  2. RUN      the box answers; the model predicted the answer before seeing it (that prediction is a free test)
  3. REPAIR   if the model was wrong, the UPDATER fixes it              -> a fix must explain the past better
  4. RETHINK  every few steps, or when fixes stall, the THEORIST writes a model from scratch, from the evidence
              alone, never seeing the current model                    -> a new theory must predict the future
stop          when the step or cost budget is spent, the box is done, or (no goal left) the model has predicted
              the last `stop_after` experiments in a row

The two judgements (all in code):
  a fix        is kept if it fits the notebook better than the current model (ties: shorter code wins)
  a theory     goes on trial: for the next `trial` experiments both models predict before seeing; the theory
               replaces the current model if it predicted them at least as well (ties: better fit, then shorter)
  sealed exam  optional (`exam` > 0, for boxes where probes are cheap): a few random probes run at the start whose
               results no role sees; every candidate must then also be at least as good on them, checked first

Numbers that say whether it is learning, all computed by code: on arrival (predicted before seen), fit (the
notebook), size (code, comments excluded), exam (if any), held-out (measurement only: no role ever sees it).
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
    steps: int = 30              # most experiments (learn + plan) in a run
    budget: float = 0            # most total cost (the box's cost units, e.g. actions); 0 = no limit
    random_every: int = 2        # every k-th experiment is a random probe from the box (0 = never)
    experimenter: str = "llm"    # "llm", or "random" (a baseline: every experiment random)
    theorist_every: int = 6      # experiments between theorist calls (0 = never)
    theorist_on_stall: int = 2   # call the theorist after this many failed fixes in a row (0 = never)
    trial: int = 3               # experiments a new theory is tried on before it can replace the model
    exam: int = 0                # sealed random probes drawn at the start (0 = none)
    retries: int = 1             # extra updater attempts when a fix isn't kept
    stop_after: int = 8          # stop once this many experiments in a row were predicted (with no goal left)
    plan: bool = True            # use the planner when the box has goals
    tasks: int = 0               # goals to attempt after learning (stateless boxes with make_tasks)
    tries: int = 3               # real attempts per such goal
    candidates: int = 5          # LLM-proposed candidates per such attempt
    heldout: int = 100           # size of the measurement-only held-out set (stateless boxes only)
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
        if env.stateful and len(self.notebook):
            env.restore(self.notebook.entries)       # resume: the box back where the run stopped
        self.exam = self._sealed("exam.json", cfg.exam, 30_000 + cfg.seed)
        self.heldout = [] if env.stateful else self._sealed("heldout.json", cfg.heldout, 10_000 + cfg.seed)
        self.trial = self._load_trial()
        self.stall = 0
        s = self.score(self.model.code)
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
        out = []
        for _ in range(n):
            p = self.env.random_probe(rng)
            if p is None:
                break
            out.append({"probe": self.env.full_probe(p), "observation": self.env.probe(p)})
        path.write_text(json.dumps(out))
        return out

    def score(self, code):
        """Everything code knows about a model on the evidence so far: predictions, matches, fit, exam, size."""
        nb = self.notebook.entries
        probes = [e["probe"] for e in nb] + [x["probe"] for x in self.exam]
        preds, err = predict_many(code, probes, timeout=60 if self.env.stateful else 30)
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
    def better(new, cur, keys=("exam", "fit"), eps=1e-9):
        """Compare on the keys in order; ties go to the shorter model."""
        for k in keys:
            if new[k] > cur[k] + eps:
                return True, f"{k} {cur[k]:.3f} -> {new[k]:.3f}"
            if new[k] < cur[k] - eps:
                return False, f"its {k} is {new[k]:.3f}, the current model's is {cur[k]:.3f}"
        if new["size"] < cur["size"]:
            return True, f"same scores, smaller ({cur['size']} -> {new['size']} chars)"
        return False, f"same scores and not smaller ({new['size']} vs {cur['size']} chars)"

    def current(self):
        return {k: getattr(self.model, k) for k in ("exam", "fit", "size")}

    def keep(self, code, role, notes, s, why):
        self.model.replace(code, role, notes, s, len(self.notebook), self.heldout_score(code))
        self.preds = s["preds"]
        h = "" if self.model.heldout is None else f"; held-out {self.model.heldout:.0%}"
        self.log(f"      model v{self.model.version} by the {role}: fit {s['fit']:.2f}, size {s['size']}"
                 + (f", exam {s['exam']:.2f}" if self.exam else "") + f" ({why}){h}")

    def offer_fix(self, code, notes):
        """The updater's fix: kept if it explains the evidence better (exam first, if there is one)."""
        if not code or "def predict" not in code:
            return False, "no predict() in the reply", None
        s = self.score(code)
        kept, why = self.better(s, self.current(), ("exam", "fit") if self.exam else ("fit",))
        if kept:
            self.keep(code, "updater", notes, s, why)
        else:
            self.log(f"      updater's fix not kept: {why}")
        self._trace("offers.jsonl", {"role": "updater", "kept": kept, "why": why, "made_at": len(self.notebook),
                                     **{k: s[k] for k in ("fit", "exam", "size", "error")}, "code": code})
        return kept, why, s

    def offer_theory(self, code, notes):
        """The theorist's theory: goes on trial against the current model (if it passes the exam, when there is one)."""
        if not code or "def predict" not in code:
            return False
        s = self.score(code)
        if self.exam and s["exam"] < self.model.exam - 1e-9:
            why = f"its exam is {s['exam']:.3f}, the current model's is {self.model.exam:.3f}"
            self.log(f"      theorist's model not tried: {why}")
            kept = False
        else:
            self.trial = {"code": code, "notes": notes, "since": len(self.notebook), "theirs": [], "ours": [],
                          "fit": s["fit"], "size": s["size"]}
            self._save_trial()
            why = f"on trial for {self.cfg.trial} experiments (fit {s['fit']:.2f}, size {s['size']})"
            self.log(f"      theorist's model {why}")
            kept = True
        self._trace("offers.jsonl", {"role": "theorist", "kept": kept, "why": why, "made_at": len(self.notebook),
                                     **{k: s[k] for k in ("fit", "exam", "size", "error")}, "code": code})
        return kept

    def judge_trial(self, pred_mine, obs):
        """Called after every experiment while a theory is on trial."""
        t = self.trial
        [theirs], _ = predict_many(t["code"], [self.notebook.entries[-1]["probe"]])
        t["theirs"].append(self.env.compare(theirs, obs))
        t["ours"].append(self.env.compare(pred_mine, obs))
        self._save_trial()
        if len(t["theirs"]) < self.cfg.trial:
            return
        a, b = mean(t["theirs"]), mean(t["ours"])
        s = self.score(t["code"])
        win = a > b + 1e-9 or (abs(a - b) <= 1e-9 and self.better(s, self.current(), ("fit",))[0])
        why = f"on trial it predicted {a:.2f} of {len(t['theirs'])} new experiments, the current model {b:.2f}"
        self._trace("trials.jsonl", {"since": t["since"], "decided_at": len(self.notebook), "theirs": t["theirs"],
                                     "ours": t["ours"], "won": win, "fit": s["fit"], "size": s["size"]})
        if win:
            self.keep(t["code"], "theorist", t["notes"], s, why)
            self.stall = 0
        else:
            self.log(f"      theorist's model lost its trial: {why}")
        self.trial = None
        self._save_trial()

    def _save_trial(self):
        path = self.dir / "trial.json"
        if self.trial is None:
            path.unlink(missing_ok=True)
        else:
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.trial))
            tmp.replace(path)

    def _load_trial(self):
        path = self.dir / "trial.json"
        return json.loads(path.read_text()) if path.exists() else None

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

    def spent(self):
        return sum(e.get("cost", 1) for e in self.notebook.entries) + sum(1 for _ in self.exam)

    def curve(self, step, kind, note=""):
        path = self.dir / "curve.csv"
        new = not path.exists()
        recent = [e for e in self.notebook.entries if e["kind"] in ("learn", "plan")][-10:]
        with path.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["step", "kind", "experiments", "cost", "model_version", "model_role", "fit", "size",
                            "exam", "arrival_last10", "heldout", "llm_calls", "note"])
            h = "" if self.model.heldout is None else f"{self.model.heldout:.3f}"
            w.writerow([step, kind, len(self.notebook), self.spent(), self.model.version, self.model.role,
                        f"{self.model.fit:.3f}", self.model.size, f"{self.model.exam:.3f}",
                        f"{mean([e['match'] >= OK for e in recent]):.2f}", h, self.calls, note])

    def context(self):
        return P.context(self.env, self.library, self.notebook, self.model, self.preds, len(self.exam), self.trial)

    def check_probe(self, p):
        if not isinstance(p, dict):
            return "the probe must be a JSON object"
        try:
            return self.env.validate(p)
        except Exception as e:
            return f"invalid probe: {e}"

    # --------------------------------------------------------------------------------------------- one experiment
    def run_experiment(self, kind, question, probe, expect=""):
        full = self.env.full_probe(probe)              # what the model predicts from: probe + where the box is now
        [pred], err = predict_many(self.model.code, [full])
        obs = self.env.probe(probe)
        match = self.env.compare(pred, obs)
        e = self.notebook.add({"kind": kind, "question": question, "expect": expect, "probe": full,
                               "observation": obs, "cost": self.env.cost(probe, obs),
                               "model_version": self.model.version, "model_prediction": pred, "match": match,
                               "model_error": err})
        self.preds.append(pred)
        self.model.matches.append(match)
        self.model.fit = mean(self.model.matches)
        self.model.fit_exact = mean([m >= OK for m in self.model.matches])
        if self.trial:
            self.judge_trial(pred, obs)
        return e

    # --------------------------------------------------------------------------------------------- the roles
    def propose(self, n):
        k = self.cfg.random_every
        if self.cfg.experimenter == "random" or (k and n % k == 1 % k):
            seen = [json.dumps(e["probe"], sort_keys=True) for e in self.notebook.entries]
            for _ in range(20):
                p = self.env.random_probe(self.rng)
                if p is not None and json.dumps(self.env.full_probe(p), sort_keys=True) not in seen:
                    break
            if p is not None:
                return {"question": "a random ordinary probe", "probe": p, "expect": ""}
        user = self.context() + "\n\n" + P.propose(self.env.goal())
        for _ in range(3):
            reply = parse_json(self.call("experimenter", P.EXPERIMENTER, user)) or {}
            err = self.check_probe(reply.get("probe"))
            if not err:
                return reply
            user += f"\n\nYour last reply was not usable: {err}. Try again."
        return None

    def plan(self, goal, max_states=4000, max_depth=40):
        """Breadth-first search through the current model (no LLM, no real action): from where the box is, try each
        action, let the model predict, move to the predicted state, skip states already reached. Returns the
        shortest action sequence the model says reaches the goal, or None."""
        actions = self.env.plan_actions()
        if not actions:
            return None
        start = self.env.full_probe({"actions": []})
        frontier, seen, expanded = [(start, [])], {self.env.state_key(start)}, 0
        for _ in range(max_depth):
            batch = [(fp, seq, a) for fp, seq in frontier for a in actions]
            if not batch or expanded > max_states:
                return None
            expanded += len(batch)
            preds, _ = predict_many(self.model.code, [{**fp, "actions": [a]} for fp, _, a in batch], timeout=120)
            nxt = []
            for (fp, seq, a), p in zip(batch, preds):
                if not isinstance(p, dict) or not p:
                    continue
                if _safe_check(goal, p):
                    return seq + [a]
                f2 = self.env.advance(fp, a, p)
                if f2 is None:
                    continue
                k = self.env.state_key(f2)
                if k not in seen:
                    seen.add(k)
                    nxt.append((f2, seq + [a]))
            frontier = nxt
        return None

    def update(self, e):
        retry = ""
        for _ in range(1 + self.cfg.retries):
            user = self.context() + "\n\n" + P.REVISE.format(
                exp_id=e["id"], question=e["question"], probe=P.clip(self.env.view_probe(e["probe"]), 1200),
                observation=P.clip(self.env.view_obs(e["observation"]), 2500),
                prediction=P.clip(self.env.view_obs(e["model_prediction"]) if isinstance(e["model_prediction"], dict)
                                  and e["model_prediction"] else json.dumps(e["model_prediction"]), 2000),
                version=e["model_version"], match=e["match"], rules=P.MODEL_RULES, retry=retry,
                error=f"(predict() raised an error: {e['model_error']})\n" if e.get("model_error") else "")
            text = self.call("updater", P.UPDATER, user)
            code = parse_code(text)
            if (not code and "KEEP" in text) or (code and code.strip() == self.model.code.strip()):
                self.log("      updater: keep")
                return False
            kept, why, s = self.offer_fix(code, text.split("```")[-1].strip()[:400])
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
        return self.offer_theory(parse_code(text), text.split("```")[-1].strip()[:400])

    def step(self, n):
        goal = self.env.goal() if self.cfg.plan else None
        plan = self.plan(goal) if goal is not None and self.model.version > 0 else None
        if plan is not None:
            piece = plan[:max(1, self.env.max_probe)]
            reply, kind = {"question": f"the model's plan for the goal ({len(plan)} actions; running the first "
                           f"{len(piece)}): {goal.description}", "probe": {"actions": piece}}, "plan"
        else:
            reply, kind = self.propose(n), "learn"
            if reply is None:
                self.log(f"[{n}] no usable probe after 3 tries; step skipped")
                return
        e = self.run_experiment(kind, reply.get("question", ""), reply["probe"], reply.get("expect", ""))
        reached = goal is not None and _safe_check(goal, e["observation"])
        self.log(f"[{n}] {e['id']} {kind}: {P.clip(e['question'], 80)}  (v{e['model_version']} predicted it: "
                 f"match {e['match']:.2f}; cost {e['cost']}, spent {self.spent()})" + ("  GOAL REACHED" if reached else ""))
        if e["match"] < OK:
            self.stall = 0 if self.update(e) else self.stall + 1
        due = self.cfg.theorist_every and n % self.cfg.theorist_every == 0
        stalled = self.cfg.theorist_on_stall and self.stall >= self.cfg.theorist_on_stall
        if (due or stalled) and self.trial is None:
            self.log(f"      theorist ({'every ' + str(self.cfg.theorist_every) + ' experiments' if due else 'fixes stalled'})")
            self.theorize()
            if stalled:
                self.stall = 0
        self.curve(n, kind, e["id"] + (" goal" if reached else ""))

    def settled(self):
        k = self.cfg.stop_after
        recent = [e for e in self.notebook.entries if e["kind"] in ("learn", "plan")]
        return (bool(k) and self.env.goal() is None and len(recent) >= k and all(e["match"] >= OK for e in recent[-k:])
                and (not self.exam or self.model.exam >= OK))

    def solve(self, n, task):
        """Stateless boxes with make_tasks(): candidates from the experimenter, screened in the model."""
        tried = []
        for t in range(self.cfg.tries):
            history = ("\nYour earlier real attempts at this goal, which failed:\n" + "\n".join(tried) + "\n") if tried else ""
            reply = parse_json(self.call("experimenter", P.EXPERIMENTER, self.context() + "\n\n" + P.SOLVE.format(
                task=task.description, k=self.cfg.candidates, history=history))) or {}
            cands = [c for c in (reply.get("candidates") or [])[:self.cfg.candidates] if not self.check_probe(c)]
            if not cands:
                continue
            preds, _ = predict_many(self.model.code, [self.env.full_probe(c) for c in cands])
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
        done = len([e for e in self.notebook.entries if e["kind"] in ("learn", "plan")])
        self.log(f"Helix Probe v3 on '{self.env.name}': {done} experiments so far, model v{self.model.version}, "
                 f"spent {self.spent()}" + (f", exam of {len(self.exam)}" if self.exam else "")
                 + (f", a theory on trial" if self.trial else ""))
        for n in range(done + 1, self.cfg.steps + 1):
            if self.should_stop():
                self.log(f"stop requested: stopping after experiment {n - 1}; run again to continue")
                return None
            if self.env.done():
                self.log("the box is done (every goal reached)")
                break
            if self.cfg.budget and self.spent() >= self.cfg.budget:
                self.log(f"budget spent ({self.spent()} of {self.cfg.budget})")
                break
            if self.settled():
                self.log(f"stopping early: the last {self.cfg.stop_after} experiments were all predicted on arrival")
                break
            self.step(n)
        results = []
        if self.cfg.tasks and not (self.dir / "summary.json").exists():
            tasks = self.env.make_tasks(random.Random(20_000 + self.cfg.seed), self.cfg.tasks)
            results = [self.solve(i, t) for i, t in enumerate(tasks, 1)]
        summary = {"env": self.env.name, "experiments": len(self.notebook), "cost": self.spent(),
                   "model_version": self.model.version, "model_role": self.model.role, "fit": self.model.fit,
                   "size": self.model.size, "exam": self.model.exam if self.exam else None,
                   "heldout": self.model.heldout, "llm_calls": self.calls,
                   "goals": {"tried": len(results), "reached": sum(r is not None for r in results),
                             "tries_used": results}}
        if hasattr(self.env, "score"):
            summary["box_score"] = self.env.score()
        (self.dir / "summary.json").write_text(json.dumps(summary, indent=1))
        self.log(json.dumps(summary))
        return summary


def _safe_check(task, obs):
    try:
        return bool(obs) and bool(task.check(obs))
    except Exception:
        return False
