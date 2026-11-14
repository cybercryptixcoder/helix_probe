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
NOTES_EVERY = 12            # steps between notes written to disk (what a resumed run continues from)
NOTES_ASK = ("Write your LAB NOTES now, because you may have to continue from these notes alone, with everything else forgotten. "
             "Include: (1) what the network does; (2) every fact you have established about how, with the numbers "
             "(indices, frequencies, coefficients, groupings) needed to rebuild the construction; (3) what you tried that failed and why; "
             "(4) what the latest judge report says passes and fails; (5) what to try next. Do not include the construction code: your "
             "best submission will be given back to you. No tool call.")

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
5. Off-manifold tests, which make states that no input produces (need 50% of the cases where the network's decision changes). Two are run at each site, and passing EITHER is enough: partial (each variable at the site is copied from A while the site's other variables keep their values from B; needs several variables at the site) and edit (a random half of the coordinates of everything you named at the site are copied). Both need realistic coefficients in model(), not just the right decision on ordinary inputs. Where the network keeps parts separate (one per position, per input, per feature group), give each part its own variable, with the coordinates that belong together kept together: copying whole parts keeps every part at a value it really takes.
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

LM_SYSTEM = """You are an interpretability researcher. You are given a real pre-trained transformer language model and a set of prompts on which it shows one behaviour. Your job is to work out HOW the model produces that behaviour, internally, and to write it down as a CONSTRUCTION that an automatic judge will test against the model.

WHAT A CONSTRUCTION IS
A short, standalone Python file that defines:

  DESCRIPTION = "plain-language account of the mechanism"

  def model(x, iv):
      # x: the task's inputs, an integer numpy array [B, n_features] (one row per prompt; the columns are described below).
      # Must return the model's predicted output [B, n_answers]: the logits of the task's answer tokens at the end position.
      # Every named intermediate variable is registered with iv:
      #     v = iv("name", value)        value is an array [B] or [B, k]; iv returns it in the same shape.
      # ALWAYS compute later steps from what iv returned, never from a copy made before the iv call:
      # during intervention tests iv returns a replaced value, and your model must respond to it.
      ...

  ALIGN = {"name": ["site", ...], ...}     # for each variable, the site(s) of the network where it lives

The file can use numpy (as np) and math only. It CANNOT see the weights or run the network: every constant it needs (directions' coefficients, thresholds, small tables) must be written into the file as literals, after you have measured them. Limit: 16,000 characters. It is a compact program a person can read, not a copy of the network.

SITES. A site is one vector per prompt, read at one token position:
  resid{L}@p       the residual stream entering block L at position p. resid0 is the token + position embedding; resid{n_layers} is the final residual stream (before the last LayerNorm and the unembedding). So resid{L} is the state after blocks 0..L-1.
  attn{L}@p        what attention layer L adds to the residual stream at p;     head{L}.{H}@p   what its head H adds at p
  mlp{L}@p         what the MLP of layer L adds at p;                           neur{L}@p       its hidden neurons at p (after GELU)
  pattern{L}.{H}@p the attention weights of head H of layer L from position p to every position
p is one of the task's role names (given below) or a token index (0, 1, ..., -1 for the last).

HOW THE JUDGE TESTS A CONSTRUCTION (on prompts held out from fitting)
1. Behaviour: does model(x) pick the same answer token (largest output) as the network?
2. Alignment: at each site in ALIGN the judge fits ONE affine map from the variables you placed there to the real activations (activation = c + variables @ M). So a variable must be related to the activations linearly. A quantity the network encodes through several nonlinear functions of it (a one-hot code, a few smooth or periodic functions, a few measured coordinates) should be those functions' values, a few coordinates, not the raw quantity.
3. CUTS. All residual sites you name at one depth L (resid{L}@p for several p) are tested TOGETHER as "cut{L}": the state of the computation at depth L.
   - Substitution: the named positions are replaced by your prediction (c + variables @ M) and EVERY OTHER position at that depth by its mean over the prompts; the rest of the network runs. The answers must survive (90%). So a cut must name every position that still matters at that depth, with variables that carry everything the later layers use from it. Positions that hold nothing the later layers need can be left out.
   - Necessity: removing the named subspace from the real activations must destroy the answers.
   - Compactness: the judge reports how many principal components of the cut suffice to keep 99% of the answers; the non-categorical variables you name may have at most about twice that many dimensions in total.
     CATEGORICAL variables are exempt from this limit: the IDENTITY of one token or one quantity may be given as a one-hot vector (np.eye(K)[value]), provided each value occurs in at least 6 prompts on average (so "which number is at position n2" is fine; a one-hot of the whole input is not). A compact code with a few features (periodic, digit-wise, monotone ...) is a stronger result when you can find one, but an identity is a legitimate variable: what matters is where it lives, and what the network computes from it.
   - Interchange: the network is run on prompt B, but the part of the cut that encodes your variables is replaced by what it is on prompt A; the network's new answer must equal what model(B) returns when iv gives those variables their values from A (90%). So the causal wiring of model() must mirror the network.
   - Partial / edit, states that no prompt produces (50% of the cases where the network's answer changes; passing either is enough): partial copies ONE variable from A while the cut's other variables stay as in B; edit copies a random half of the coordinates of everything named (not run on one-hot variables). Give each separately-stored part its own variable (one per position, per feature group). These tests put the network in states such as "the tokens of B, but with variable v as in A", so model() must say what the network does with ANY combination of its variables' values, not only the combinations the prompts contain: find that out by patching (hook) before you write it down.
   Sites of the other kinds (attn, mlp, head, neur, pattern) are tested one at a time with the same tests. They say which component carries a variable; they are welcome detail, but only cuts count toward completeness.
4. STAGES. The model's depth is divided into stages: the embedding (resid0), then four bands of layers (for 12 layers: resid1-3, resid4-6, resid7-9, resid10-12). A stage is explained when one cut inside it is verified. The construction is COMPLETE when it behaves like the network and every stage has a verified cut: it then says what the network holds, where, from the tokens to the answer, and model() says how each stage's variables are computed from the previous stage's. That is the goal, reached one stage at a time.

YOUR TOOLS
- python(code): a persistent session (variables stay between calls). Defined:
    X [N, n_features] the task inputs; X_NAMES; PROMPTS (list of N strings); TOKENS [N, T] token ids; ROLES {role: token position}; ANSWERS (the answer tokens, strings); ANSWER_IDS
    run(x, hook=None) -> [B, n_answers]: the network's answer logits for task prompts. x = rows of X, or a 1-D array of prompt numbers.
    logits(x, hook=None) -> [B, n_vocab]: all logits at the end position.
    acts(x, sites) -> {site: array [B, width]} for the site names you ask for.
    hook = {site: array [B, width] (or [width]) or function(array) -> array}: the run is done with those activations REPLACED. This is how you do your own experiments: mean-ablate a site, patch it from other prompts (acts on prompts A, run on prompts B with hook), add a direction, swap a subspace. Several sites can be hooked at once. "resid{L}@*" addresses all positions at once, flattened [B, T * d_model].
    run_tokens(tokens [B, T'], hook=None, sites=()) -> (logits [B, n_vocab] at the last position, {site: array}): any token sequences, not only the task's prompts (positions in site names must be token indices). tok(text) -> token ids; detok(ids) -> token strings.
    W: dict of the weights (numpy): W_E [n_vocab, d], W_pos, W_U [d, n_vocab], ln_f.w/b, and per layer l: L{l}.W_Q, W_K, W_V [n_heads, d, d_head], b_Q, b_K, b_V, W_O [n_heads, d_head, d], b_O, ln1.w/b, ln2.w/b, W_in [d, d_mlp], b_in, W_out [d_mlp, d], b_out. CFG: sizes.
    unembed(v) -> logits for final-residual vector(s) v (applies the last LayerNorm); top(vocab_vector, k) -> the k largest tokens.
    np, scipy, sklearn. Print what you want to see; output is cut at about 8,000 characters, so print summaries, not raw arrays.
  Cost: a run over 200 prompts takes about 0.2-1 s (less when the hooked sites are late in the network and at late positions). A call is stopped after 600 s: plan scans (for example every layer at a few positions first, heads only where it matters), and use a subset of a few hundred prompts.
- submit(code): sends a construction file to the judge and returns its report (it takes a minute or two). The report is the fastest way to learn what is right: unit by unit, variable by variable, what passes and what fails, next to controls.

SUBMIT EARLY, THEN IMPROVE STAGE BY STAGE
Do not try to understand everything before you submit. A construction with one cut is a valid submission, and partial constructions are expected. Make your first submission within your first 8 steps. After that, submit whenever you have changed something; if you go 6 steps without submitting you will be required to submit what you have. WORK BACKWARDS FROM THE ANSWER: first the last stage (what the end position holds just before the unembedding), then the stage before it (what must be present, and at which positions, for the last stage's variables to be computed), and so on down. Each stage you verify tells you what the stage below has to deliver. Leave the embedding stage for LAST: it is usually the hardest, because its partial tests ask what the model does when one input token is exchanged for another, which needs a full model of the behaviour off the prompts. Do not spend many steps on one failing stage while a later stage is still unverified. Keep verified cuts in every submission; a cut that fails costs judge time, so include only the failing cut you are working on.

HOW TO WORK
1. Find out WHAT the model does on these prompts: which answer it picks as a function of x. Write model(x) for the behaviour first.
2. Find out WHERE the information is at each depth. For a depth L and each position, replace resid{L}@p by its mean (or patch it from another prompt) and see whether the answers change: that gives the positions a cut at L must name, and how information moves between positions across depth. Patching from a prompt that differs in ONE input quantity shows where that quantity lives.
3. Find out WHAT is held there: variables that are functions of x and that the site's activations are a linear function of. Check candidates by regression, and check that they are the part that matters by running the network with the site replaced by your regression's prediction (this is the judge's substitution test; do it yourself before submitting). For a quantity with many values (a token's identity, a number), look at how the activations vary with it: principal components of the per-value means, periodic or monotone structure along the value, digit structure; use the few coordinates that carry the behaviour. Look at the weights too: the embedding and unembedding rows of the tokens involved, which heads' QK attend where and what their OV writes, which directions an MLP reads and writes. Let the numbers decide; do not assume a mechanism because it is familiar.
4. Write the construction: variables at each cut, each computed in model() from the previous cut's variables (or from x at the embedding), the answer logits computed from the last ones. Measure the constants with python and write them into the file. Submit, read the report, fix what fails.
5. If a unit fails, find out why with python before resubmitting (what does the cut depend on that your variables miss? which position did you leave out? is the variable used by the later layers at that depth at all?). You can reproduce every judge test yourself with run, acts and hook.
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


def lm_task_text(meta, cfg):
    c = meta["cfg"]
    L = ["THE NETWORK", meta["arch"], ""]
    L += [f"THE PROMPTS ({meta['n_prompts']} prompts, each {meta['n_tokens']} tokens)", meta["domain"]["text"],
          "Examples: " + " | ".join(repr(p) for p in meta["example_prompts"]),
          f"Features (columns of x): {', '.join(meta['x_names'])}.",
          "Roles (token positions): " + ", ".join(f"{r} = {p}" for r, p in meta["roles"].items()) + ".",
          f"Answer tokens ({len(meta['answers'])}): " + (", ".join(repr(a) for a in meta["answers"]) if len(meta["answers"]) <= 12 else
                                                       ", ".join(repr(a) for a in meta["answers"][:4]) + ", ..., " + repr(meta["answers"][-1])) + ".",
          "", f"SITES: resid0..resid{c['n_layers']}, and attn / mlp / neur for layers 0..{c['n_layers'] - 1}, head / pattern for heads 0..{c['n_heads'] - 1}, "
          "each @ a role or a token index.",
          "STAGES: " + "; ".join(__import__("lmjudge").stage_names(c["n_layers"])[0]) + "."]
    if cfg["told"]:
        L += ["", "WHAT THE MODEL DOES ON THESE PROMPTS", meta.get("context", ""), "Task: " + meta["answer"]["short"]]
    else:
        L += ["", "You are not told what the model does on these prompts. Find out."]
    if cfg.get("one_shot"):
        L += ["", "In this run you get ONE submission and no report back: the run ends when you submit. Make it your best."]
    if not cfg["weights"]:
        L += ["", "In this run you have NO access to the model: W, X, run, logits, acts and the other model tools are not defined in the "
              "python session (only np, X_NAMES, ANSWERS). Write the construction from what you know and what you are told above, "
              "including which sites hold which variables. The judge will still test it against the real model."]
    L += ["", "Begin."]
    return "\n".join(L)


def task_text(meta, W, cfg):
    if meta["forward"] == "lm":
        return lm_task_text(meta, cfg)
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
        self.lm = json.loads((LAB / "models" / target / "meta.json").read_text()).get("forward") == "lm"
        self.cfg = {"lab_dir": str(LAB), "meta": str(LAB / "models" / target / "meta.json"),
                    "weights": str(LAB / "models" / target / "weights.npz") if weights else None,
                    "variant": variant, "allow_forward": allow_forward, "seed": seed, "lm": self.lm}
        self.p = None
        self.start()

    def start(self):
        self.p = subprocess.Popen([sys.executable, "-I", str(LAB / "kernel.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, cwd="/tmp")
        self.q = queue.Queue()
        threading.Thread(target=self._pump, args=(self.p, self.q), daemon=True).start()
        self.p.stdin.write(json.dumps(self.cfg) + "\n"); self.p.stdin.flush()
        self.q.get(timeout=300)

    @staticmethod
    def _pump(p, q):
        for line in p.stdout:
            q.put(line)
        q.put(None)

    def run(self, code, timeout=None):
        timeout = timeout or (600 if self.lm else 120)
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


def next_focus(rep):
    """One mechanical line appended to an LM report: which stage to work on next (the unverified stage nearest the output)."""
    st = list(rep["stages"].items())
    todo = [n for n, s in st if not s["verified"]]
    if not todo:
        return ""
    done = [n for n, s in st if s["verified"]]
    return (f"\nWHERE TO WORK NEXT: verified stages: {', '.join(done) or 'none'}. Work on \"{todo[-1]}\" now (the unverified stage nearest "
            f"the answer; sites {', '.join(rep['stages'][todo[-1]]['sites'])}), and submit it together with the verified cuts only.")


def run_judge(target, variant, path, seed=0, timeout=1500):
    """Judge a construction file in a separate process. Returns (text shown to the reader, report dict or None)."""
    out_json = path.with_suffix(".json")
    import fcntl
    try:
        # one judge at a time on this machine (a lock file): judging a language model takes about 2 GB, and two runs
        # judging at once were killed for memory. A judge that dies without a message is tried once more.
        with open("/tmp/helix_judge.lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            for attempt in range(2):
                p = subprocess.run([sys.executable, str(LAB / "judge.py"), target, str(path), "--variant", variant, "--seed", str(seed),
                                    "--json", str(out_json)], capture_output=True, text=True, timeout=timeout, cwd="/tmp")
                if p.returncode in (0, 1) or "Traceback" in (p.stderr or ""):
                    break
                time.sleep(20)
    except subprocess.TimeoutExpired:
        return f"The judge timed out after {timeout} s: model(x, iv) is too slow. It must run on a few thousand inputs in seconds.", None
    text = (p.stdout or "").strip() or ("The judge crashed:\n" + (p.stderr or "")[-1500:])
    rep = json.loads(out_json.read_text()) if p.returncode == 0 and out_json.exists() else None
    if rep and rep.get("kind") == "lm":
        text += next_focus(rep)
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
              max_tokens=12000, seed=0, emit=None, cancelled=None, title="", one_shot=False, resume=None):
    """resume: the id of an earlier run of this target that stopped or died. The run continues in the same folder from
    the reader's last notes and its best submission (the python session starts empty)."""
    emit = emit or (lambda ev: None)
    cancelled = cancelled or (lambda: False)
    meta = json.loads((LAB / "models" / target / "meta.json").read_text())
    is_lm = meta["forward"] == "lm"
    W = None if is_lm else {k: v.astype(np.float64) for k, v in np.load(LAB / "models" / target / "weights.npz").items()}
    system = LM_SYSTEM if is_lm else SYSTEM
    render = __import__("lmjudge").render if is_lm else judge_mod.render
    best, best_n, nudges = None, None, 0
    if resume:
        run_id = resume
        rdir = OUT / target / run_id
        rec = json.loads((rdir / "run.json").read_text())
        cfg = rec["config"]
        variant, told, weights, allow_forward, seed, one_shot = cfg["variant"], cfg["told"], cfg["weights"], cfg["allow_forward"], cfg["seed"], cfg.get("one_shot", False)
        cfg["max_steps"] = max_steps = max(max_steps, len(rec["steps"]) + 1)
        task = rec["task"]
        rec["status"] = "running"
        rec.setdefault("notes", []); rec.setdefault("resumed", []).append({"at_step": len(rec["steps"]), "time": time.time()})
        for sub in rec["submissions"]:
            jp = rdir / (Path(sub["file"]).stem + ".json")
            if jp.exists():
                r_ = json.loads(jp.read_text())
                if better(r_, best):
                    best, best_n = r_, sub["n"]
        notes = (rec["notes"] or rec["compactions"] or [{"notes": "(the run was interrupted before any notes were written)"}])[-1]["notes"]
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": task},
                {"role": "assistant", "content": "LAB NOTES (written by me earlier in this investigation)\n" + notes}]
        tail = ("Your earlier session on this network was interrupted. Continue the investigation from your notes. The python session "
                "was restarted: your variables are gone, so recompute what you need.")
        if best_n:
            sub = rec["submissions"][best_n - 1]
            tail += (f"\n\nYour best submission so far (number {best_n}):\n```python\n{(rdir / sub['file']).read_text()}\n```\n\n"
                     f"Its judge report:\n{sub['report_text']}")
        msgs.append({"role": "user", "content": tail})
    else:
        cfg = {"target": target, "variant": variant, "told": told, "weights": weights, "allow_forward": allow_forward, "effort": effort,
               "max_steps": max_steps, "max_tokens": max_tokens, "seed": seed, "title": title, "model": luminal.model(), "one_shot": one_shot}
        run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
        rdir = OUT / target / run_id
        rdir.mkdir(parents=True, exist_ok=True)
        task = task_text(meta, W, cfg)
        rec = {"id": run_id, "config": cfg, "started": time.time(), "system": system, "task": task, "steps": [], "submissions": [],
               "compactions": [], "notes": [], "usage": {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0}, "cost": 0.0, "status": "running",
               "best": None, "final_message": ""}
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": task}]

    def save():
        rec["heartbeat"], rec["pid"] = time.time(), os.getpid()
        (rdir / "run.json.tmp").write_text(json.dumps(rec, indent=1))
        os.replace(rdir / "run.json.tmp", rdir / "run.json")

    (rdir / "STOP").unlink(missing_ok=True)
    outer_cancelled = cancelled
    cancelled = lambda: outer_cancelled() or (rdir / "STOP").exists()      # noqa: E731  (a STOP file in the run folder stops the run)
    save()

    emit({"type": "start", "id": run_id, "target": target, "dir": str(rdir.relative_to(LAB.parent))})
    kernel = Kernel(target, variant, weights=weights, allow_forward=allow_forward, seed=seed)
    last_notes = len(rec["steps"])
    try:
        for step in range(len(rec["steps"]), max_steps):
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
                last_notes = step
            elif step - last_notes >= NOTES_EVERY:
                # notes written to disk at intervals, so that a run that dies can be resumed (--resume) from them
                content, _, _, usage, _ = chat(msgs + [{"role": "user", "content": NOTES_ASK}], None, "low", 6000, lambda ev: None, cancelled)
                rec["cost"] += luminal.cost(usage)
                rec["notes"].append({"at_step": step, "notes": content})
                last_notes = step
                save()
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
        (rdir / "report.txt").write_text(render(best) + "\n")
        rec["verdict"] = best["verdict"]
    save()
    emit({"type": "done", "id": run_id, "status": rec["status"], "seconds": rec["seconds"], "best": best_n,
          "verdict": best["verdict"] if best else None, "cost": rec["cost"]})
    return rec


def compact(msgs, rec, rdir, best_n, effort, emit, cancelled):
    """The conversation is near the context limit: have the reader write its notes, then continue from the notes alone."""
    emit({"type": "note", "text": "context nearly full: the reader writes its notes and continues from them"})
    content, _, _, usage, _ = chat(msgs + [{"role": "user", "content": "Your context is nearly full. " + NOTES_ASK}], None, effort, 6000, emit, cancelled)
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
    ap.add_argument("--resume", default=None, help="continue an earlier run of this target (its run id) from its notes and best submission")
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

    rec = construct(a.target, a.variant, told=a.told, weights=not a.no_weights, effort=a.effort, max_steps=a.steps, emit=emit, title=a.title, one_shot=a.one_shot, resume=a.resume)
    print(f"\nstatus {rec['status']}; best submission {rec['best']}; cost ${rec['cost']:.3f}; {rec['seconds']} s; "
          f"{LAB / 'constructions' / a.target / rec['id']}")


if __name__ == "__main__":
    main()
