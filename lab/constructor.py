"""The constructor: an LLM reader that investigates a network with its own code and writes a construction of it,
which the judge (judge.py) tests. The same prompt, tools and tests for every network.

One run:
  1. The reader gets the architecture, the list of weight tensors and activation sites, and the set of inputs the
     network is used on. By default it is NOT told what the network does (blinded).
  2. It works in a persistent Python session over the weights (kernel.py): it can inspect the weights, run the
     network, and record activations.
  3. It submits a construction (a small standalone Python file; see judge.py). The judge's report comes back as
     text. It revises and resubmits.
  4. The run ends when the judge says VERIFIED AND COMPLETE, when the reader stops, or when the step budget is used.
     The best submission is saved as the run's construction.

Everything is written to lab/constructions/<target>/<run id>/ as the run goes, so a run can be inspected at any point:
  run.json              configuration, every step (reader's words, code, outputs), every judge report, token usage
  submission_NN.py      each construction the reader submitted;  submission_NN.json  its judge report
  construction.py       the best submission;  report.txt / report.json  its judge report

Run from a terminal:  python3 lab/constructor.py <target id> [--variant shuffled] [--steps 60] [--told] [--no-weights] [--one-shot]
The prior-only control is  --told --no-weights --one-shot : the task is named, the reader has no weights and cannot
run the network, and it gets one submission with no report (a report would tell it about the network).
"""
import argparse, json, os, queue, subprocess, sys, threading, time, uuid
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
OUT = LAB / "constructions"


def load_env():
    env = LAB / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


load_env()
import luminal  # noqa: E402
import nets     # noqa: E402
import judge as judge_mod  # noqa: E402

PRUNE = """

# ---- added by the constructor at the end of the run ----
# These sites failed the judge's tests in the reader's best submission, so the delivered construction does not claim
# them. The variables stay in model(); they are just not aligned there. See run.json for the attempt and its report.
_UNVERIFIED_SITES = {sites}
ALIGN = {{v: [s for s in where if s not in _UNVERIFIED_SITES] for v, where in ALIGN.items()}}
ALIGN = {{v: where for v, where in ALIGN.items() if where}}
"""

COMPACT_AT = 105_000        # prompt tokens: past this, the conversation is replaced by the reader's own notes
SUBMIT_EVERY = 6            # after this many steps without a submission, the reader's next turn can only submit

SYSTEM = """You are an interpretability researcher. You are given a trained neural network: its weights, its architecture and the set of inputs it is used on. Your job is to work out HOW it computes its outputs and to write that down as a CONSTRUCTION that an automatic judge will test.

WHAT A CONSTRUCTION IS
A short, standalone Python file that defines:

  DESCRIPTION = "plain-language account of the mechanism"

  def model(x, iv):
      # x: the inputs, a numpy array [B, n_in]. Must return the network's predicted output, an array [B, n_out].
      # Every named intermediate variable is registered with iv:
      #     v = iv("name", value)        value is an array [B] or [B, k]; iv returns it in the same shape.
      # ALWAYS compute later steps from what iv returned, never from a copy made before the iv call:
      # during intervention tests iv returns a replaced value, and your model must respond to it.
      ...

  ALIGN = {"name": ["site", ...], ...}     # for each variable, the activation site(s) of the network where it lives

The file can use numpy (as np) and math only. It CANNOT see the weights W or run the network: every constant it needs (frequencies, thresholds, coefficients, small tables) must be written into the file as literals, after you have measured them. Limit: 16,000 characters. It is meant to be a compact program that a person can read, not a copy of the network.

A small example of the format, for an unrelated toy network (2 inputs, one hidden layer "h1", 1 output) that outputs max(x1, x2):

  DESCRIPTION = "Outputs max(x1, x2). The hidden layer holds relu(x1 - x2) and x2; the output adds them."
  def model(x, iv):
      gap = iv("gap", np.maximum(x[:, 0] - x[:, 1], 0))
      base = iv("base", x[:, 1])
      return (gap + base)[:, None]
  ALIGN = {"gap": ["h1"], "base": ["h1"]}

HOW THE JUDGE TESTS IT (on inputs held out from fitting)
1. Behaviour: does model(x) make the same decision as the network (largest output; sign if there is one output; if the network makes one decision per position, all of them)?
2. Alignment: at each site in ALIGN the judge fits ONE affine map from the variables you placed there to the real activations (activation = c + variables @ M). So a variable must be related to the activations linearly. If the network encodes a quantity through several nonlinear functions of it (for example a one-hot code, or a few smooth functions of it), the variable should be those functions' values, a few coordinates, not the raw quantity.
3. Substitution: the site's activation is replaced by the construction's prediction (c + variables @ M) and the rest of the network runs. The decisions must survive. Removing the named subspace from the real activation must destroy them. And the variables must be compact: the judge reports how many principal components of the site suffice to keep the decisions, and you may name at most about twice that many dimensions. Huge variables (a lookup table of the inputs) fail this.
4. Interchange, at each site s you align to: the network is run on an input B, but at site s the part of the activation that encodes your variables is replaced by what it is on another input A (the variables are read from the two real activations with a linear probe, and the change (v(A) - v(B)) @ M is added at site s); everything after site s is recomputed. The network's new decision must equal what model(B) returns when iv gives those variables their values from A (need 90%). So the causal wiring of model() must mirror the network: a variable must feed the later variables the way the activation at its site feeds the later sites. A variable placed at several sites is tested at each site separately.
5. Partial and edit tests, which make states that no input produces (need 50% of the cases where the network's decision changes). If a site holds several variables, each one is copied from A while the others keep their values from B (partial). If a site holds one variable, a random half of its coordinates are copied (edit). Both need realistic coefficients in model(), not just the right decision on ordinary inputs. Give each independent part of a site its own variable (one per position, per input, per feature group: whatever the network keeps separate, with the coordinates that belong together kept together): copying a whole part is a fairer test than copying half of its coordinates.
A site is verified when it passes 3-5. The network's sites are grouped into STAGES (the successive steps of its computation); a stage is explained when one of its sites is verified. The construction is COMPLETE when it behaves like the network and every stage is explained. That is the goal, reached one stage at a time, with variables that are as low-dimensional as you can make them.

YOUR TOOLS
- python(code): runs in a persistent session (variables stay between calls). Available: W (dict of weight arrays), X (all inputs the network is used on, [N, n_in]), run(x) -> outputs, acts(x) -> {site: activations [B, width]} (every site, exact: you never need to re-implement the forward pass), SITES, np, scipy, sklearn. Print what you want to see; output is cut at about 8,000 characters, so print summaries, not raw arrays.
- submit(code): sends a construction file to the judge and returns its report. The report is the fastest way to learn what is right: it tells you, site by site and variable by variable, what passes and what fails.

SUBMIT EARLY, THEN IMPROVE STAGE BY STAGE
Do not try to understand everything before you submit. A construction that explains only one stage is a valid submission, and partial constructions are expected along the way: stages are added one at a time. Make your first submission within your first 6 steps, as soon as you know what the network does and have one candidate variable at one site. After that, submit whenever you have changed something. If you go 6 steps without submitting, you will be required to submit what you have. Explain the easy stages first and leave the hardest stage for last.

HOW TO WORK
1. Find out WHAT the network does: run it on its inputs and find the rule relating inputs to outputs.
2. Find out HOW, stage by stage. Look at the weights themselves for structure (which rows or columns matter, low rank, sparsity, repeated or regular patterns along an index, groups of similar units), and at the activations at each site as functions of the input. Look for a small set of quantities that each site's activations are simple (linear) functions of, and check candidates by regression before you rely on them. Let the numbers decide; do not assume a mechanism because it is familiar.
3. Write the construction with one or more variables for each stage, computed from the previous stage's variables. Measure the constants with python, write them into the file, submit, read the report, and fix what fails.
4. If a site fails, investigate why with python (what does the activation depend on that your variables miss? is the variable used by the network at that site at all?) before resubmitting. You can reproduce any of the judge's tests yourself with run and acts. A variable that is present at a site but not used by what comes after should be given its own name and not fed forward in model().
Keep each message short. Do the thinking with code. When the judge reports VERIFIED AND COMPLETE, or you are certain you cannot improve further, reply with a short final summary and no tool call."""

TOOLS = [
    {"type": "function", "function": {
        "name": "python",
        "description": "Run Python in the persistent session over the network (W, X, run, acts, SITES, np are defined). Returns what the code prints.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "submit",
        "description": "Submit a construction file (the full Python source: DESCRIPTION, model(x, iv), ALIGN) to the judge. Returns the judge's report.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
]


def task_text(meta, W, cfg):
    kind = meta["forward"]
    L = ["THE NETWORK", meta["arch"], ""]
    if cfg["weights"]:
        L.append("Weight tensors in W: " + "; ".join(
            f"{t['name']} {tuple(t['shape'])}" + (f" = {t['desc']}" if t.get("desc") else "") for t in meta["tensors"]))
        L.append(f"({meta['params']:,} parameters.)")
    L += ["", "ACTIVATION SITES (name, width, what it is) by stage:"]
    stage = None
    for name, width, desc, st in nets.site_table(kind, W):
        if st != stage:
            stage = st
            L.append(f"  stage: {st}" + ("  (not a site you can align to; model() returns it)" if name == "out" else ""))
        L.append(f"    {name}  [{width}]  {desc}")
    L += ["", "THE INPUTS", meta["domain"]["text"]]
    if cfg["told"]:
        L += ["", "WHAT THE NETWORK DOES", meta.get("context", ""), "Task: " + meta["answer"]["short"]]
    else:
        L += ["", "You are not told what the network does or what its inputs and outputs mean. Find out."]
    if cfg.get("one_shot"):
        L += ["", "In this run you get ONE submission and no report back: the run ends when you submit. Make it your best."]
    if not cfg["weights"]:
        L += ["", "In this run you have NO access to the weights, and you cannot run the network or record activations: W, X, run and acts "
              "are not defined in the python session. Write the construction from what you know and what you are told above. The judge "
              "will still test it against the real network."]
    L += ["", "Begin."]
    return "\n".join(L)


# ---------------------------------------------------------------- the persistent python session
class Kernel:
    def __init__(self, target, variant, weights=True, allow_forward=True, seed=0):
        self.cfg = {"lab_dir": str(LAB), "meta": str(LAB / "models" / target / "meta.json"),
                    "weights": str(LAB / "models" / target / "weights.npz") if weights else None,
                    "variant": variant, "allow_forward": allow_forward, "seed": seed}
        self.p = None
        self.start()

    def start(self):
        self.p = subprocess.Popen([sys.executable, "-I", str(LAB / "kernel.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, cwd="/tmp")
        self.q = queue.Queue()
        threading.Thread(target=self._pump, args=(self.p, self.q), daemon=True).start()
        self.p.stdin.write(json.dumps(self.cfg) + "\n"); self.p.stdin.flush()
        self.q.get(timeout=60)

    @staticmethod
    def _pump(p, q):
        for line in p.stdout:
            q.put(line)
        q.put(None)

    def run(self, code, timeout=120):
        t0 = time.time()
        try:
            self.p.stdin.write(json.dumps({"code": code}) + "\n"); self.p.stdin.flush()
            line = self.q.get(timeout=timeout)
            res = json.loads(line) if line else {"ok": False, "output": "The python session died (out of memory?). It has been restarted: all variables are lost."}
            if line is None:
                self.start()
        except queue.Empty:
            self.p.kill(); self.start()
            res = {"ok": False, "output": f"Timed out after {timeout} s. The python session was restarted: all variables are lost. Use smaller computations."}
        except (BrokenPipeError, OSError):
            self.start()
            res = {"ok": False, "output": "The python session died. It has been restarted: all variables are lost."}
        res["seconds"] = round(time.time() - t0, 2)
        return res

    def close(self):
        try:
            self.p.kill()
        except Exception:  # noqa: BLE001
            pass


def run_judge(target, variant, path, seed=0, timeout=600):
    """Judge a construction file in a separate process. Returns (text shown to the reader, report dict or None)."""
    out_json = path.with_suffix(".json")
    try:
        p = subprocess.run([sys.executable, str(LAB / "judge.py"), target, str(path), "--variant", variant, "--seed", str(seed),
                            "--json", str(out_json)], capture_output=True, text=True, timeout=timeout, cwd="/tmp")
    except subprocess.TimeoutExpired:
        return f"The judge timed out after {timeout} s: model(x, iv) is too slow. It must run on a few thousand inputs in seconds.", None
    text = (p.stdout or "").strip() or ("The judge crashed:\n" + (p.stderr or "")[-1500:])
    rep = json.loads(out_json.read_text()) if p.returncode == 0 and out_json.exists() else None
    return text, rep


# ---------------------------------------------------------------- one model call, streamed
def chat(messages, tools, effort, max_tokens, emit, cancelled):
    payload = {"messages": messages, "max_tokens": max_tokens}
    if tools:
        payload["tools"], payload["tool_choice"] = tools, "auto"
    last = None
    for attempt in range(4):
        content, reasoning, calls, usage, finish = [], [], {}, None, None
        try:
            resp = luminal.open_stream(payload, effort)
            with resp:
                for raw in resp:
                    if cancelled():
                        raise InterruptedError
                    line = raw.decode(errors="replace").strip()
                    if not line.startswith("data:") or line == "data: [DONE]":
                        continue
                    try:
                        chunk = json.loads(line[5:])
                    except json.JSONDecodeError:
                        continue
                    if chunk.get("error"):
                        raise luminal.LuminalError(502, f"Luminal error mid-answer: {str(chunk['error'])[:300]}", retryable=True)
                    usage = chunk.get("usage") or usage
                    for ch in chunk.get("choices") or []:
                        finish = ch.get("finish_reason") or finish
                        d = ch.get("delta") or {}
                        if d.get("reasoning_content"):
                            reasoning.append(d["reasoning_content"]); emit({"type": "thinking", "text": d["reasoning_content"]})
                        if d.get("content"):
                            content.append(d["content"]); emit({"type": "content", "text": d["content"]})
                        for tc in d.get("tool_calls") or []:
                            c = calls.setdefault(tc.get("index", 0), {"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
                            c["id"] = tc.get("id") or c["id"]
                            fn = tc.get("function") or {}
                            c["function"]["name"] += fn.get("name") or ""
                            c["function"]["arguments"] += fn.get("arguments") or ""
            if usage is None and not content and not calls:
                raise luminal.LuminalError(502, "Luminal sent an empty answer.", retryable=True)
            return "".join(content), "".join(reasoning), [calls[i] for i in sorted(calls)], usage or {}, finish
        except (luminal.LuminalError, OSError, TimeoutError) as e:
            last = e
            if isinstance(e, luminal.LuminalError) and not e.retryable:
                raise
            emit({"type": "note", "text": f"connection problem, retrying ({e})"})
            time.sleep(5 * (attempt + 1))
    raise luminal.LuminalError(502, f"Luminal kept failing: {last}")


def tool_code(call):
    """The code argument of a tool call. The reader sometimes sends broken JSON; recover the code where possible."""
    raw = call["function"]["arguments"] or ""
    try:
        v = json.loads(raw)
        if isinstance(v, dict):
            return str(v.get("code", ""))
    except json.JSONDecodeError:
        pass
    i = raw.find('"code"')
    if i >= 0:
        body = raw[raw.find(":", i) + 1:].strip()
        if body.startswith('"'):
            body = body[1:]
            body = body[: body.rfind('"')] if body.rstrip().endswith("}") else body
            try:
                return json.loads('"' + body + '"')
            except json.JSONDecodeError:
                return body.encode().decode("unicode_escape", errors="replace")
    return raw


def better(a, b):
    """Is report a a better result than report b (None = nothing yet)?"""
    if b is None:
        return True
    ka = (a["verdict"]["complete"], a["verdict"]["score"], a["verdict"]["verified"], -len(a["verdict"]["fails"]))
    kb = (b["verdict"]["complete"], b["verdict"]["score"], b["verdict"]["verified"], -len(b["verdict"]["fails"]))
    return ka >= kb


# ---------------------------------------------------------------- the run
def construct(target, variant="original", told=False, weights=True, allow_forward=True, effort="high", max_steps=80,
              max_tokens=12000, seed=0, emit=None, cancelled=None, title="", one_shot=False):
    emit = emit or (lambda ev: None)
    cancelled = cancelled or (lambda: False)
    meta = json.loads((LAB / "models" / target / "meta.json").read_text())
    W = {k: v.astype(np.float64) for k, v in np.load(LAB / "models" / target / "weights.npz").items()}
    cfg = {"target": target, "variant": variant, "told": told, "weights": weights, "allow_forward": allow_forward, "effort": effort,
           "max_steps": max_steps, "max_tokens": max_tokens, "seed": seed, "title": title, "model": luminal.model(), "one_shot": one_shot}
    run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    rdir = OUT / target / run_id
    rdir.mkdir(parents=True, exist_ok=True)
    task = task_text(meta, W, cfg)
    rec = {"id": run_id, "config": cfg, "started": time.time(), "system": SYSTEM, "task": task, "steps": [], "submissions": [],
           "compactions": [], "usage": {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0}, "cost": 0.0, "status": "running",
           "best": None, "final_message": ""}

    def save():
        (rdir / "run.json").write_text(json.dumps(rec, indent=1))

    emit({"type": "start", "id": run_id, "target": target, "dir": str(rdir.relative_to(LAB.parent))})
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    kernel = Kernel(target, variant, weights=weights, allow_forward=allow_forward, seed=seed)
    best, best_n, nudges = None, None, 0
    try:
        for step in range(max_steps):
            if cancelled():
                raise InterruptedError
            emit({"type": "step", "step": step, "of": max_steps})
            since = step - (rec["submissions"][-1]["step"] if rec["submissions"] else -1)
            tools = TOOLS
            if since > SUBMIT_EVERY and (best is None or not best["verdict"]["complete"]):
                # the reader has gone too long without testing anything: this turn it can only submit
                tools = TOOLS[1:]
                msgs.append({"role": "user", "content": (
                    ("You have not submitted a construction yet. " if not rec["submissions"] else f"It is {since - 1} steps since your last submission. ") +
                    "Submit one now: this turn the only tool is submit. Put in what you have established so far, even if it explains "
                    "only one stage or is rough; partial constructions are expected. The judge's report will show what holds, and you "
                    "continue from there.")})
                emit({"type": "note", "text": "asked the reader to submit now"})
            content, thinking, calls, usage, finish = chat(msgs, tools, effort, max_tokens, emit, cancelled)
            rec["usage"]["prompt_tokens"] += usage.get("prompt_tokens") or 0
            rec["usage"]["completion_tokens"] += usage.get("completion_tokens") or 0
            rec["usage"]["calls"] += 1
            rec["cost"] += luminal.cost(usage)
            emit({"type": "usage", "usage": rec["usage"], "cost": rec["cost"], "context": usage.get("prompt_tokens")})
            srec = {"step": step, "content": content, "thinking": thinking, "finish": finish, "context_tokens": usage.get("prompt_tokens"), "tools": []}
            rec["steps"].append(srec)
            if not calls:
                done = best is not None and (best["verdict"]["complete"] or nudges >= 2)
                if done or step == max_steps - 1:
                    rec["final_message"] = content
                    break
                nudges += 1
                msgs.append({"role": "assistant", "content": content, "reasoning_content": thinking})
                msgs.append({"role": "user", "content": (
                    "The construction is not complete yet" + ("" if best else " (nothing has been submitted)") +
                    f". You have {max_steps - step - 1} steps left. Keep going: use python to investigate what fails and submit an improved "
                    "construction. If you are certain you cannot improve it, say so in one line with no tool call.")})
                save()
                continue
            msgs.append({"role": "assistant", "content": content, "reasoning_content": thinking, "tool_calls": calls})
            for c in calls:
                name, code = c["function"]["name"], tool_code(c)
                if name == "submit":
                    n = len(rec["submissions"]) + 1
                    path = rdir / f"submission_{n:02d}.py"
                    path.write_text(code)
                    emit({"type": "tool_call", "tool": "submit", "code": code, "n": n})
                    text, rep = run_judge(target, variant, path, seed)
                    sub = {"n": n, "step": step, "file": path.name, "verdict": rep["verdict"] if rep else None, "report_text": text}
                    rec["submissions"].append(sub)
                    if rep and better(rep, best):
                        best, best_n = rep, n
                        rec["best"] = n
                    emit({"type": "report", "n": n, "text": text, "verdict": sub["verdict"], "best": best_n})
                    srec["tools"].append({"tool": "submit", "n": n, "code": code, "output": text})
                    out = text
                else:
                    emit({"type": "tool_call", "tool": "python", "code": code})
                    res = kernel.run(code)
                    emit({"type": "tool_result", "ok": res["ok"], "output": res["output"], "seconds": res["seconds"]})
                    srec["tools"].append({"tool": "python", "code": code, **res})
                    out = res["output"] or "(no output: print what you want to see)"
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": out + f"\n[{max_steps - step - 1} steps left]"})
            save()
            if one_shot and rec["submissions"]:
                break               # a single submission and no feedback: the judge's report is itself information about the network
            if best is not None and best["verdict"]["complete"] and best_n == len(rec["submissions"]):
                msgs.append({"role": "user", "content": "The judge reports VERIFIED AND COMPLETE. Reply with a short final summary of the mechanism (no tool call)."})
                content, thinking, _, usage, _ = chat(msgs, None, "low", 2000, emit, cancelled)
                rec["final_message"] = content
                rec["cost"] += luminal.cost(usage)
                break
            if (usage.get("prompt_tokens") or 0) > COMPACT_AT:
                msgs = compact(msgs, rec, rdir, best_n, effort, emit, cancelled)
        rec["status"] = "done"
    except InterruptedError:
        rec["status"] = "stopped"
    except luminal.LuminalError as e:
        rec["status"] = "error"; rec["error"] = e.message
        emit({"type": "error", "message": e.message})
    except Exception as e:  # noqa: BLE001
        rec["status"] = "error"; rec["error"] = f"{type(e).__name__}: {e}"
        emit({"type": "error", "message": rec["error"]})
    finally:
        kernel.close()
    rec["seconds"] = round(time.time() - rec["started"], 1)
    if best_n:
        src = (rdir / f"submission_{best_n:02d}.py").read_text()
        failing = [s for s, r in best["sites"].items() if not r["pass"]]
        if failing and len(failing) < len(best["sites"]):
            # the delivered construction claims only what passed: drop the failing sites from ALIGN and judge again
            pruned = src.rstrip() + PRUNE.format(sites=json.dumps(failing))
            path = rdir / "construction.py"
            path.write_text(pruned)
            text, rep = run_judge(target, variant, path, seed)
            (rdir / "construction.json").unlink(missing_ok=True)
            if rep and rep["verdict"]["verified"]:
                rec["pruned_sites"] = failing
                best = rep
            else:
                path.write_text(src)
        else:
            (rdir / "construction.py").write_text(src)
        (rdir / "report.json").write_text(json.dumps(best, indent=1))
        (rdir / "report.txt").write_text(judge_mod.render(best) + "\n")
        rec["verdict"] = best["verdict"]
    save()
    emit({"type": "done", "id": run_id, "status": rec["status"], "seconds": rec["seconds"], "best": best_n,
          "verdict": best["verdict"] if best else None, "cost": rec["cost"]})
    return rec


def compact(msgs, rec, rdir, best_n, effort, emit, cancelled):
    """The conversation is near the context limit: have the reader write its notes, then continue from the notes alone."""
    emit({"type": "note", "text": "context nearly full: the reader writes its notes and continues from them"})
    ask = ("Your context is nearly full. Write your LAB NOTES now, because you will continue from these notes alone and everything else "
           "will be forgotten. Include: (1) what the network does; (2) every fact you have established about how, with the numbers "
           "(indices, frequencies, coefficients, groupings) needed to rebuild the construction; (3) what you tried that failed and why; "
           "(4) what the latest judge report says passes and fails; (5) what to try next. Do not include the construction code: your "
           "best submission will be given back to you. No tool call.")
    content, _, _, usage, _ = chat(msgs + [{"role": "user", "content": ask}], None, effort, 6000, emit, cancelled)
    rec["cost"] += luminal.cost(usage)
    rec["compactions"].append({"at_step": len(rec["steps"]), "notes": content})
    new = [msgs[0], msgs[1], {"role": "assistant", "content": "LAB NOTES (written by me earlier in this investigation)\n" + content}]
    tail = "Continue the investigation from your notes. The python session is still alive with your variables."
    if best_n:
        sub = rec["submissions"][best_n - 1]
        tail += (f"\n\nYour best submission so far (number {best_n}):\n```python\n{(rdir / sub['file']).read_text()}\n```\n\n"
                 f"Its judge report:\n{sub['report_text']}")
    new.append({"role": "user", "content": tail})
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--variant", default="original", choices=["original", "shuffled", "untrained", "permuted"])
    ap.add_argument("--steps", type=int, default=80)
    ap.add_argument("--effort", default="high")
    ap.add_argument("--told", action="store_true", help="tell the reader the task (not blinded)")
    ap.add_argument("--no-weights", action="store_true", help="prior-only control: no weights, no network")
    ap.add_argument("--one-shot", action="store_true", help="the run ends at the first submission (no judge feedback)")
    ap.add_argument("--title", default="")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    def emit(ev):
        t = ev["type"]
        if a.quiet and t in ("thinking", "content"):
            return
        if t == "thinking":
            sys.stdout.write("\033[2m" + ev["text"] + "\033[0m")
        elif t == "content":
            sys.stdout.write(ev["text"])
        elif t == "step":
            print(f"\n===== step {ev['step'] + 1}/{ev['of']}")
        elif t == "tool_call":
            print(f"\n--- {ev['tool']} ---\n{ev['code']}")
        elif t == "tool_result":
            print(f"--- output ({ev['seconds']} s) ---\n{ev['output']}")
        elif t == "report":
            print(f"--- judge report {ev['n']} ---\n{ev['text']}")
        elif t in ("note", "error", "start", "done"):
            print(f"\n[{t}] " + json.dumps({k: v for k, v in ev.items() if k != 'type'}))
        sys.stdout.flush()

    rec = construct(a.target, a.variant, told=a.told, weights=not a.no_weights, effort=a.effort, max_steps=a.steps, emit=emit, title=a.title, one_shot=a.one_shot)
    print(f"\nstatus {rec['status']}; best submission {rec['best']}; cost ${rec['cost']:.3f}; {rec['seconds']} s; "
          f"{LAB / 'constructions' / a.target / rec['id']}")


if __name__ == "__main__":
    main()
