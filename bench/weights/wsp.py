"""Weight-space experiments: can DeepSeek V4.1 Flash read (and edit) neural network weights, and does structure help?

Replicates the setups of "Sparks of Weight-Space Programming" (Takehi, Teoh, Zhang & Khattab, MIT CSAIL, Nov 2026;
networks, prompts and answer keys from github.com/RikiyaT/lm_understand-logs, CC BY 4.0, fetched by
bench/weights/fetch_mit.sh). One file: tasks, a sandbox like theirs, their conversation protocol, our Helix arm, and
the graders.

FORMATS (what the reader can touch):
  text   the weights as text in the prompt, one reply, no tools               (their exp 1, 2: exact prompts)
  code   Python over the weights, the network may not be run                  (their exp 3: exact message; exp 1: new)
  run    Python over the weights + a budget of forward passes, and edits:     (their exp 6/8 condition; new for exp 1)
         `forward(X)` runs the CURRENT network, `save(W)` keeps an edit for later runs
  full   run + the weights as text in the message too                         (new: everything at once)
  blind  forward passes only: the weights are hidden, no reading, no edits     (new: separates running from reading)
PROTOCOLS (how the reader works):
  mit    their protocol: one conversation; to compute, reply with exactly one ```python block; we run it and reply with
         its output; no code block = the final answer
  helix  Helix Probe's structure: narrow roles in series, each with its own system prompt and a fresh context:
         EXPERIMENTER writes one experiment (code + what it expects to print, BEFORE it runs) -> the sandbox runs it ->
         a match is scored (expected vs printed, judged by a separate call) -> if surprised, the UPDATER revises the
         findings (claims citing experiment ids) -> every 6 experiments the THEORIST rewrites the findings from the
         evidence alone -> at the end one call answers the question from the findings and the notebook
CONTROLS: --shuffle reorders the values inside every weight array (a reader that really reads falls to chance);
          --effort none|high (thinking off / on).

    python bench/weights/wsp.py --task exp1 --format code --protocol mit --effort high --reps 3 --out runs/weights/X
    python bench/weights/wsp.py --report runs/weights            # every job under a folder, one table
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from probe.llm import LLM  # noqa: E402

MIT = ROOT / "bench" / "weights" / "mit"
SYSTEM = "Answer the user's request."          # their one-line system instructions, for the mit protocol
_print = threading.Lock()


def say(m):
    with _print:
        print(time.strftime("%H:%M:%S"), m, flush=True)


# =====================================================================================================  the tasks
GAMES = {"breakout": ("breakout", "brick"), "pong": ("pong",), "pacman": ("pac-man", "pacman", "pac man"),
         "freeway": ("freeway", "frogger", "road-crossing", "road crossing", "crossy")}
SHAPES = {"circle": ("circle", "disc", "disk", "round", "oval", "ellipse"), "square": ("square", "rectangle", "box"),
          "triangle": ("triangle", "pyramid", "wedge")}


def answer_line(text, field):
    m = re.search(rf"^\W*{field}\W*?[:：]\W*?(\w.*)$", text, re.I | re.M) or \
        re.search(rf"^\W*{field}\W*?[:：]?\W*\n+\s*(\S.*)$", text, re.I | re.M)   # "X: answer", or a heading then the answer
    return (m.group(1) if m else "").lower()


def keyword_grade(text, field, table):
    line = answer_line(text, field)
    for k, keys in table.items():
        if any(w in line for w in keys):
            return k, line
    return None, line


class Exp1:
    """Which game was this policy network trained on? (4 networks, open answer)"""
    name, chance = "exp1", 0.25
    dir = MIT / "exp1_which_game"
    QUESTION_TAIL = None

    def items(self):
        key = json.loads((self.dir / "eval" / "answer_key.json").read_text())
        return [(nid, v["game"]) for nid, v in key.items()]

    def weights(self, nid):
        """The actor only (what Astra saw), named as the description names them."""
        z = np.load(self.dir / "networks" / f"{nid}.npz")
        names = {"W1": "actor/dense1/kernel", "b1": "actor/dense1/bias", "W2": "actor/dense2/kernel",
                 "b2": "actor/dense2/bias", "W3": "actor/logits/kernel", "b3": "actor/logits/bias"}
        return {k: np.asarray(z[v], np.float64) for k, v in names.items()}

    def text_prompt(self, game):
        return (self.dir / "runs" / game / "prompt.txt").read_text()

    def weights_text(self, nid):
        return (self.dir / "networks" / f"{nid}_actor.txt").read_text()

    def message(self, nid, game, fmt, budget):
        """Their exp-1 description and question, with the computing rules of their exp 3 (code) or exp 6 (run)."""
        p = self.text_prompt(game)
        desc, rest = p.split("\nQUESTION.", 1)
        question = "QUESTION." + rest.split("THE NETWORK'S WEIGHTS")[0]
        question = question.replace(" You have no tools: no code execution, no calculator, nothing to run. This is a "
                                    "single response.", "")
        rules = {"code": CODE_RULES, "blind": BLIND_RULES}.get(fmt, RUN_RULES).replace("{budget}", str(budget))
        names = "W['W1'] is 500 x 32, W['b1'] has 32 entries, W['W2'] is 32 x 32, W['b2'] 32, W['W3'] 32 x 5, W['b3'] 5"
        msg = desc.strip() + "\n\n" + rules.replace("{names}", names) + "\n\n" + question.strip()
        if fmt == "full":
            msg += "\n\nTHE NETWORK'S WEIGHTS (the same values as W, rounded)\n" + self.weights_text(nid)
        return msg

    def forward_src(self):
        return ("def _net(W, X):\n    h1 = np.tanh(X @ W['W1'] + W['b1'])\n    h2 = np.tanh(h1 @ W['W2'] + W['b2'])\n"
                "    return h2 @ W['W3'] + W['b3']\n_IN = 500\n")

    def grade(self, text, truth):
        g, line = keyword_grade(text, "Game", GAMES)
        return {"guess": g, "answer_line": line, "correct": g == truth}


class Exp2(Exp1):
    """Which shape does this diffusion model generate? (3 networks, open answer; text format only)"""
    name, chance = "exp2", 1 / 3
    dir = MIT / "exp2_diffusion"

    def items(self):
        key = json.loads((self.dir / "eval" / "answer_key.json").read_text())
        return [(nid, v["shape"] if isinstance(v, dict) else v) for nid, v in key.items()]

    def text_prompt(self, shape):
        return (self.dir / "runs" / shape / "prompt.txt").read_text()

    def grade(self, text, truth):
        g, line = keyword_grade(text, "Images", SHAPES)
        return {"guess": g, "answer_line": line, "correct": g == truth}


class Exp3:
    """Which text was this character transformer trained on, and which heads copy? (their exact message; code format)"""
    name, chance = "exp3", 1 / 3
    dir = MIT / "exp3_language"

    def items(self):
        return [(lang, lang) for lang in ("python", "romaji", "english")]

    def weights(self, lang):
        z = np.load(self.dir / "networks" / lang / "blocks.npz")
        return {k: z[k] for k in z.files}

    def message(self, lang, truth, fmt, budget):
        return (self.dir / "runs" / f"{lang}_r0" / "message.txt").read_text()

    def grade(self, text, truth):
        corpus = answer_line(text, "corpus").split()[0].strip("*.,") if answer_line(text, "corpus") else None
        heads = json.loads((self.dir / "eval" / "heads.json").read_text())
        truth_heads = heads.get(f"{truth}_L4_H6_d384_s0", {})
        true_copy = {h for h, v in truth_heads.items() if isinstance(v, dict) and v.get("induct", 0) > 0.2}
        named = set(re.findall(r"^\W*(L\dH\d)\W*[:：]?\W*copy\b", text, re.I | re.M))   # the head's label itself
        named = {h.upper() for h in named}
        return {"guess": corpus, "correct": corpus == truth, "copy_named": sorted(named), "copy_true": sorted(true_copy),
                "copy_tp": len(named & true_copy), "copy_fp": len(named - true_copy)}


TASKS = {"exp1": Exp1, "exp2": Exp2, "exp3": Exp3}

CODE_RULES = """HOW YOU COMPUTE. The weights are available to you as numpy arrays: you read them by running Python code. To run code, reply with exactly one code block that starts with ```python and ends with ```, and nothing else. We run it and reply with its printed output. Available: numpy, scipy, scikit-learn, pandas, sympy, networkx. Before your code runs, numpy is imported as np and W is a dict of the weight arrays by name: {names}. Each run is a fresh process (nothing is kept between runs), may take up to 600 seconds, and its output is cut at 20,000 characters. You may run code up to 100 times. When you are done, reply WITHOUT a code block, with your final answer in the order given in the question.

You may analyse the weights with any method you like: multiply them, decompose them, compare, cluster or fit them, write any analysis you want. Two things are NOT allowed:
1. A forward pass: do not run the network or any of its layers on any input, whether real, random or constructed, in code, in your head or on paper. Treating the weight matrices as linear-algebra objects (products, eigenvalues, singular vectors, applying one weight matrix to directions taken from other weights) is fine; simulating what the network does to an input is not.
2. Search: do not look anything up (there is no internet access in any case)."""

RUN_RULES = """HOW YOU COMPUTE. The weights are available to you as numpy arrays, and you may run the network and edit it. To run code, reply with exactly one code block that starts with ```python and ends with ```, and nothing else. We run it and reply with its printed output. Available: numpy, scipy, scikit-learn, pandas, sympy, networkx. Before your code runs, numpy is imported as np and W is a dict of the CURRENT weight arrays by name: {names}.
- forward(X) runs the current network on a batch of inputs X (an array of up to 256 rows, one input per row) and returns the outputs. Each call is one forward pass; you have {budget} forward passes in total, across all your runs. Running the network or its layers in any other way (writing the forward computation yourself) is not allowed.
- save(W) keeps your edits: after save(W), later runs and forward passes use the edited weights. reset() restores the original weights. Edit freely: change single weights, rows, columns, whole matrices, by any amount or function you choose.
- A folder that is kept between runs is your working directory: save any files you like there.
Each run may take up to 600 seconds, and its output is cut at 20,000 characters. You may run code up to 100 times. Training or fitting the network to data (gradient descent, optimizers) is not allowed, and there is no internet access. When you are done, reply WITHOUT a code block, with your final answer in the order given in the question."""


BLIND_RULES = """HOW YOU COMPUTE. You cannot see the weights, but you can run the network. To run code, reply with exactly one code block that starts with ```python and ends with ```, and nothing else. We run it and reply with its printed output. Available: numpy, scipy, scikit-learn, pandas, sympy, networkx; numpy is imported as np. forward(X) runs the network on a batch of inputs X (an array of up to 256 rows, one input per row) and returns the outputs. Each call is one forward pass; you have {budget} forward passes in total, across all your runs. Each run may take up to 600 seconds, and its output is cut at 20,000 characters. You may run code up to 100 times. Training or fitting a model of the network to its outputs is allowed only as analysis; there is no internet access. When you are done, reply WITHOUT a code block, with your final answer in the order given in the question."""


# =====================================================================================================  the sandbox
PRELUDE = r'''
import json, os, sys, numpy as np
np.set_printoptions(precision=4, suppress=True, linewidth=160)
_D = os.environ["WSP_DIR"]
_ORIG = dict(np.load(_D + "/orig.npz"))
W = dict(np.load(_D + "/current.npz")) if os.path.exists(_D + "/current.npz") else {k: v.copy() for k, v in _ORIG.items()}
def save(Wd):
    np.savez(_D + "/current.npz", **{k: np.asarray(v) for k, v in Wd.items()})
def reset():
    global W
    if os.path.exists(_D + "/current.npz"):
        os.remove(_D + "/current.npz")
    W = {k: v.copy() for k, v in _ORIG.items()}
'''
FORWARD = r'''
def forward(X):
    X = np.asarray(X, dtype=np.float64)
    if X.ndim == 1:
        X = X[None]
    assert X.shape[0] <= 256 and X.shape[1] == _IN, f"X must be up to 256 rows of {_IN} numbers"
    used = int(open(_D + "/passes").read()) if os.path.exists(_D + "/passes") else 0
    if used >= _BUDGET:
        raise RuntimeError(f"no forward passes left (budget {_BUDGET})")
    open(_D + "/passes", "w").write(str(used + 1))
    return _net(W, X)
'''


_BWRAP = None


def bwrap_status():
    """(usable, reason). bubblewrap can be installed but blocked (Ubuntu 24.04's AppArmor stops unprivileged user
    namespaces), so try it once; if it fails, runs go unisolated and record isolated=false."""
    global _BWRAP
    if _BWRAP is None:
        if not shutil.which("bwrap"):
            _BWRAP = (False, "bubblewrap not installed")
        else:
            try:
                p = subprocess.run(["bwrap", "--unshare-net", "--die-with-parent", "--dev-bind", "/", "/",
                                    sys.executable, "-c", "print('ok')"], capture_output=True, text=True, timeout=30)
                ok = p.returncode == 0 and "ok" in p.stdout
                _BWRAP = (ok, "bubblewrap (no network)" if ok else
                          "bubblewrap installed but blocked here: " + (p.stderr.strip().splitlines() or ["?"])[-1])
            except Exception as e:  # noqa: BLE001
                _BWRAP = (False, f"bubblewrap failed to start: {e}")
    return _BWRAP


class Sandbox:
    """MIT's sandbox, lean: a fresh python -I process per run, the weights preloaded as W, a folder kept between runs
    (edits and the forward-pass count live there), a timeout, output cut at 20,000 characters, no network (bubblewrap
    when the machine has it; otherwise a clean environment, recorded in the run)."""

    def __init__(self, folder, weights, task, fmt, budget, shuffle_seed=None):
        self.dir = Path(folder) / "sandbox"
        self.dir.mkdir(parents=True, exist_ok=True)
        if not (self.dir / "orig.npz").exists():
            W = {k: np.array(v) for k, v in weights.items()}
            if shuffle_seed is not None:
                rng = np.random.default_rng(abs(hash(shuffle_seed)) % 2**32)
                W = {k: rng.permutation(v.ravel()).reshape(v.shape) for k, v in W.items()}
            np.savez(self.dir / "orig.npz", **W)
        self.prelude = PRELUDE
        if fmt in ("run", "full", "blind"):
            self.prelude += task.forward_src() + f"_BUDGET = {budget}\n" + FORWARD
        if fmt == "blind":     # the weights stay inside forward(); the reader gets no W, no edits
            self.prelude = self.prelude.replace("def forward(X):", "_HIDDEN = W\ndel W, save, reset\ndef forward(X):")
            self.prelude = self.prelude.replace("    return _net(W, X)", "    return _net(_HIDDEN, X)")
        self.bwrap = bwrap_status()[0]

    def passes(self):
        p = self.dir / "passes"
        return int(p.read_text()) if p.exists() else 0

    def run(self, code, timeout=600, max_out=20000):
        env = {"WSP_DIR": str(self.dir), "PATH": "/usr/bin:/bin", "HOME": str(self.dir), "OMP_NUM_THREADS": "2",
               "PYTHONPATH": os.pathsep.join(p for p in sys.path if p and "site-packages" in p)}
        work = self.dir / "work"
        work.mkdir(exist_ok=True)
        cmd = [sys.executable, "-c", self.prelude + "\n" + code]
        if self.bwrap:
            cmd = ["bwrap", "--unshare-net", "--die-with-parent", "--dev-bind", "/", "/", "--chdir", str(work)] + cmd
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, cwd=work)
            out = p.stdout + (("\n[stderr]\n" + p.stderr[-6000:]) if p.stderr.strip() else "")
        except subprocess.TimeoutExpired:
            out = f"[timed out after {timeout} s]"
        if len(out) > max_out:
            out = out[:max_out] + f"\n[output cut at {max_out:,} characters]"
        return out or "(no output)"


def code_block(text):
    """The first ```python block of a reply (None = no block = a final answer). Replies with more than one block are
    a format violation in MIT's protocol; we run the first and count the violation (see `extra_blocks`)."""
    blocks = re.findall(r"```python\s*\n(.*?)```", text, re.S)
    if not blocks:
        tail = re.search(r"```python\s*\n(.*)$", text, re.S)      # cut off mid-block by the token limit
        return tail.group(1) if tail else None
    return blocks[0]


def n_blocks(text):
    return len(re.findall(r"```python", text))


def audit(code, fmt):
    """Flag code that may break the format's rules (read by a person later; nothing is blocked)."""
    flags = []
    if fmt == "code" and re.search(r"np\.tanh\s*\(.*@|relu|softmax|layer_norm|np\.maximum\(0", code):
        flags.append("may compute a forward pass")
    if re.search(r"\b(torch\.optim|optimizer|\.backward\(|minimize\(|curve_fit|fit\()", code):
        flags.append("may train or fit")
    return flags


# =====================================================================================================  protocol: mit
def run_mit(llm, task, item, truth, fmt, args, folder):
    """Their protocol: one conversation; code blocks are run and their output returned; no block = final answer."""
    if fmt == "text":
        msg = task.text_prompt(truth) if task.name != "exp3" else None
        if args.shuffle:
            msg = shuffle_text(msg, f"{item}-{args.rep}")
        r = llm(SYSTEM, msg, effort=args.effort, max_tokens=args.max_tokens)
        log_call(folder, 1, msg, r)
        return r["text"], {"turns": 1, "code_runs": 0, "passes": 0}
    sb = Sandbox(folder, task.weights(item), task, fmt, args.budget, f"{item}-{args.rep}" if args.shuffle else None)
    msgs = [{"role": "user", "content": task.message(item, truth, fmt, args.budget)}]
    runs, flags, extra = 0, [], 0
    for turn in range(1, args.max_turns + 1):
        r = llm(SYSTEM, "", effort=args.effort, max_tokens=args.max_tokens, messages=msgs)
        log_call(folder, turn, msgs[-1]["content"], r)
        code = code_block(r["text"])
        extra += max(0, n_blocks(r["text"]) - 1)
        msgs.append({"role": "assistant", "content": r["text"]})
        if code is None or runs >= args.max_runs:
            if code is not None:       # out of runs: ask for the answer
                msgs.append({"role": "user", "content": "You have used all your code runs. Give your final answer now, without a code block."})
                r = llm(SYSTEM, "", effort=args.effort, max_tokens=args.max_tokens, messages=msgs)
                log_call(folder, turn + 1, msgs[-1]["content"], r)
            return r["text"], {"turns": turn, "code_runs": runs, "passes": sb.passes(), "audit": flags, "isolated": sb.bwrap, "extra_blocks": extra}
        out = sb.run(code)
        runs += 1
        fl = audit(code, fmt)
        flags += [f"run {runs}: {f}" for f in fl]
        with open(folder / "tool_calls.jsonl", "a") as fh:
            fh.write(json.dumps({"run": runs, "code": code, "out": out[:8000], "flags": fl}) + "\n")
        msgs.append({"role": "user", "content": out})
    return msgs[-2]["content"] if msgs[-2]["role"] == "assistant" else "", {"turns": args.max_turns, "code_runs": runs,
                                                                             "passes": sb.passes(), "audit": flags, "isolated": sb.bwrap, "extra_blocks": extra}


def shuffle_text(prompt, seed):
    rng = random.Random(seed)
    head, sep, weights = prompt.partition("THE NETWORK'S WEIGHTS\n")
    if not sep:
        head, sep, weights = prompt.rpartition("\n\n")
    out, block = [], []

    def flush():
        vals = [v for line in block for v in line.split()]
        rng.shuffle(vals)
        it = iter(vals)
        out.extend(" ".join(next(it) for _ in line.split()) for line in block)
        block.clear()

    for line in weights.split("\n"):
        if re.fullmatch(r"[-0-9. ]+", line.strip() or "x"):
            block.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return head + sep + "\n".join(out)


def log_call(folder, turn, prompt, r):
    with open(folder / "calls.jsonl", "a") as fh:
        fh.write(json.dumps({"turn": turn, "prompt_tail": prompt[-3000:], "text": r["text"], "reasoning": r.get("reasoning"),
                             "usage": r.get("usage"), "seconds": r.get("seconds"), "finish": r.get("finish")}) + "\n")


# =====================================================================================================  protocol: helix
H_EXPERIMENTER = """You study a neural network by running one small experiment at a time. You see the task, the current findings (claims about the network, each citing the experiments behind it) and a digest of the experiments so far. Choose ONE experiment that tests the most uncertain or most decisive claim, or opens the most useful new question. Write it as Python (it runs in the sandbox described in the task) that PRINTS a short result. Before it runs, say what you expect it to print if the current findings are right. Reply with exactly:
QUESTION: <one line>
EXPECT: <what the output should show, concretely, if the findings are right>
```python
<code>
```"""
H_JUDGE = """You compare an expectation with an actual result. Reply with one line: MATCH: <a number from 0 to 1> <one short reason>. 1 = the result is what was expected; 0 = it contradicts it."""
H_UPDATER = """You maintain the findings about a neural network: a short list of claims, each one line, each citing the experiments that support it, e.g. "- Channel 2 (reward) weights are concentrated in rows 1-3 [E4, E7]". An experiment just surprised the findings. Revise them so they agree with ALL the evidence: rewrite or remove the claims it contradicts and add what it shows. Evidence wins over any earlier claim; do not add exceptions to save a claim. Keep the findings short. Reply with only the revised findings."""
H_THEORIST = """You see only the evidence about a neural network (the experiments and their results), not anyone's current conclusions. Write the findings from scratch: a short list of one-line claims, each citing the experiments that support it, that together explain the evidence and say what the network was trained to do. Prefer claims that explain many results at once. Reply with only the findings."""
H_ANSWER = """Answer the question about the network from the findings and the evidence. Follow the answer format of the question exactly."""


def run_helix(llm, task, item, truth, fmt, args, folder):
    """Helix Probe's structure on a weight box (see the module docstring). Every call is fresh; memory is the files."""
    sb = Sandbox(folder, task.weights(item), task, fmt, args.budget, f"{item}-{args.rep}" if args.shuffle else None)
    taskmsg = task.message(item, truth, fmt, args.budget)
    taskmsg = re.sub(r"To run code, reply with exactly one code block.*?with its printed output\. ", "", taskmsg, flags=re.S)
    taskshort = taskmsg.split("\n\nTHE NETWORK'S WEIGHTS")[0]   # only the experimenter reads the weights text
    findings, notebook, hits = "(none yet)", [], []
    nb_path, f_path = folder / "notebook.jsonl", folder / "findings.md"
    if nb_path.exists():                                           # resume
        notebook = [json.loads(l) for l in nb_path.read_text().splitlines() if l.strip()]
        findings = f_path.read_text() if f_path.exists() else findings
        hits = [e["match"] for e in notebook]

    def digest(limit=14000):
        rows = [f"{e['id']} [{e['match']:.1f}] Q: {e['question']}\n   expected: {e['expect'][:300]}\n   got: {e['out'][:900]}"
                for e in notebook]
        s = "\n".join(rows)
        return s if len(s) <= limit else "...(earlier experiments omitted; see the findings)\n" + s[-limit:]

    for k in range(len(notebook) + 1, args.max_runs + 1):
        ctx = f"# The task\n{taskmsg}\n\n# Findings\n{findings}\n\n# Experiments so far\n{digest() or '(none)'}"
        r = llm(H_EXPERIMENTER, ctx, effort=args.effort, max_tokens=args.max_tokens)
        log_call(folder, k, "experimenter", r)
        code = code_block(r["text"])
        if code is None:
            continue
        q = (re.search(r"QUESTION:\s*(.+)", r["text"]) or [None, ""])[1]
        exp = (re.search(r"EXPECT:\s*(.+?)(?:```|$)", r["text"], re.S) or [None, ""])[1].strip()
        out = sb.run(code)
        j = llm(H_JUDGE, f"Expected:\n{exp}\n\nActual output:\n{out[:6000]}", effort="none", max_tokens=200)
        m = re.search(r"MATCH:\s*([01](?:\.\d+)?)", j["text"])
        match = float(m.group(1)) if m else 0.0
        e = {"id": f"E{k}", "question": q.strip(), "expect": exp, "code": code, "out": out[:6000], "match": match,
             "passes_used": sb.passes(), "audit": audit(code, fmt)}
        notebook.append(e)
        hits.append(match)
        with open(nb_path, "a") as fh:
            fh.write(json.dumps(e) + "\n")
        say(f"   {folder.name} {e['id']} match {match:.1f}: {q[:70]}")
        if match < 0.75:
            u = llm(H_UPDATER, f"# Findings\n{findings}\n\n# The surprising experiment\n{e['id']} Q: {q}\nexpected: {exp}\ngot: {out[:4000]}\n\n# All experiments\n{digest()}",
                    effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "updater", u)
            findings = u["text"].strip() or findings
        if k % 6 == 0:
            t = llm(H_THEORIST, f"# The task\n{taskshort}\n\n# The evidence\n{digest()}", effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "theorist", t)
            findings = t["text"].strip() or findings
        f_path.write_text(findings)
        if fmt in ("run", "full", "blind") and sb.passes() >= args.budget and k >= args.min_runs:
            break
    a = llm(H_ANSWER, f"# The task\n{taskshort}\n\n# Findings\n{findings}\n\n# Evidence\n{digest()}", effort=args.effort,
            max_tokens=args.max_tokens)
    log_call(folder, 0, "answer", a)
    return a["text"], {"turns": len(notebook), "code_runs": len(notebook), "passes": sb.passes(),
                       "arrival": sum(hits) / len(hits) if hits else None,
                       "audit": [f"{e['id']}: {f}" for e in notebook for f in e["audit"]], "isolated": sb.bwrap}


# =====================================================================================================  the job
def one(llm, task, item, truth, rep, args):
    args = argparse.Namespace(**{**vars(args), "rep": rep})
    folder = Path(args.out) / f"{truth}_{item}_r{rep}"
    if (folder / "result.json").exists():
        return json.loads((folder / "result.json").read_text())
    folder.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    run = run_mit if args.protocol == "mit" or args.format == "text" else run_helix
    text, info = run(llm, task, item, truth, args.format, args, folder)
    res = {"task": task.name, "item": item, "truth": truth, "rep": rep, "format": args.format, "protocol": args.protocol,
           "effort": args.effort, "shuffled": args.shuffle, **task.grade(text, truth), **info,
           "seconds": round(time.time() - t0, 1)}
    (folder / "answer.md").write_text(text)
    (folder / "result.json").write_text(json.dumps(res, indent=1))
    say(f"== {task.name} {args.format}/{args.protocol}/{args.effort}{' shuffled' if args.shuffle else ''} {truth} r{rep}: "
        f"{'RIGHT' if res['correct'] else 'wrong'} ({res['guess']}), {info.get('code_runs', 0)} runs, {info.get('passes', 0)} passes")
    return res


def report(root):
    rows = {}
    for f in Path(root).glob("**/result.json"):
        r = json.loads(f.read_text())
        k = (r["task"], r["format"], r["protocol"] if r["format"] != "text" else "-", r["effort"], r["shuffled"])
        rows.setdefault(k, []).append(r)
    lines = ["| task | format | protocol | thinking | weights | correct | code runs | passes | extra |", "|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(rows):
        rs = rows[k]
        c = sum(r["correct"] for r in rs)
        extra = ""
        if k[0] == "exp3":
            extra = f"copy heads named right {sum(r['copy_tp'] for r in rs)}, wrong {sum(r['copy_fp'] for r in rs)}"
        if any(r.get("arrival") is not None for r in rs):
            extra += f" arrival {np.mean([r['arrival'] for r in rs if r.get('arrival') is not None]):.2f}"
        lines.append(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {'shuffled' if k[4] else 'real'} | {c}/{len(rs)} | "
                     f"{np.mean([r.get('code_runs', 0) for r in rs]):.1f} | {np.mean([r.get('passes', 0) for r in rs]):.1f} | {extra} |")
    text = "\n".join(lines) + "\n"
    Path(root).mkdir(parents=True, exist_ok=True)
    (Path(root) / "report.md").write_text(text)
    return text


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--task", choices=sorted(TASKS), default="exp1")
    a.add_argument("--format", choices=["text", "code", "run", "full", "blind"], default="text")
    a.add_argument("--protocol", choices=["mit", "helix"], default="mit")
    a.add_argument("--effort", default="high")
    a.add_argument("--shuffle", action="store_true")
    a.add_argument("--reps", type=int, default=3)
    a.add_argument("--budget", type=int, default=50, help="forward passes (run/full formats)")
    a.add_argument("--max-runs", type=int, default=100, help="code runs (mit) / experiments (helix)")
    a.add_argument("--min-runs", type=int, default=12)
    a.add_argument("--max-turns", type=int, default=120)
    a.add_argument("--max-tokens", type=int, default=32000)
    a.add_argument("--workers", type=int, default=2)
    a.add_argument("--items", nargs="*", help="only these network ids / truths (tests)")
    a.add_argument("--out")
    a.add_argument("--report")
    args = a.parse_args()
    if args.report:
        print(report(args.report))
        return
    task = TASKS[args.task]()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "job.json").write_text(json.dumps(vars(args), indent=1))
    llm = LLM()
    jobs = [(item, truth, rep) for item, truth in task.items() for rep in range(args.reps)
            if not args.items or item in args.items or truth in args.items]
    with ThreadPoolExecutor(args.workers) as pool:
        res = list(pool.map(lambda j: one(llm, task, *j, args), jobs))
    c = sum(r["correct"] for r in res)
    say(f"== {args.task} {args.format}/{args.protocol}: {c}/{len(res)} correct (chance {task.chance:.2f})")


if __name__ == "__main__":
    main()
