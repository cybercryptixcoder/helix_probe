"""Every word the three roles see, in one place.

experimenter  chooses one experiment          sees: the box, the library, the model, its scores, the evidence
updater       revises the model on surprise   sees: the same, plus the surprise
theorist      writes a model from scratch     sees: the box, the library, the evidence. NOT the current model,
                                              so it can't inherit its patches.
"""
from __future__ import annotations

import json

EXPERIMENTER = """You design experiments on a black box. Nobody has told you how it works inside; the only way to \
learn is to probe it and look at what comes back. A separate step turns results into a model, so your one job is \
to choose the single next experiment that will teach the most. You remember nothing between calls except what is \
written below."""

UPDATER = """You maintain a model of a black box: a Python function predict(probe) that should predict what the \
box returns for ANY probe, including ones nobody has run. The evidence in the notebook is ground truth. Your model \
is only a hypothesis: when an experiment contradicts it, the model is wrong, never the experiment. You remember \
nothing between calls except what is written below."""

THEORIST = """You are given the results of experiments on a black box and must write, from scratch, a model of how \
it works: a Python function predict(probe) that predicts what the box returns for ANY probe, including ones nobody \
has run. You are deliberately NOT shown anyone's earlier model, so that you look at the evidence with fresh eyes. \
The evidence is ground truth."""

MODEL_RULES = """How to write the model:
- It is a model of the MECHANISM: rules stated in terms of the probe's contents, never in terms of particular past \
experiments. "If the probe equals the one in E12, return E12's result" is memorisation: it predicts nothing new and \
it fails the exam, which is scored on sealed probes you will never see.
- A box can be complicated. Several rules, regions or components are fine, if each one would also predict probes \
nobody has run. A real exception (a region where the behaviour changes) is a rule about that region, with \
boundaries; find the boundaries rather than listing cases.
- When an experiment contradicts a rule, rewrite or replace the rule; don't wrap it in a special case.
- If unsure, write your best guess in the code and mark it in a comment with "?".
- Put your beliefs at the top of predict() as comments, one line each, citing evidence: "# A moves up 1 [E3, E7]". \
The comments are the explanation; the code is what gets tested.
- If the box keeps state (the probe carries a "history"), the box may remember things the current state doesn't \
show: counters, items, which switches were used. If the same visible state and action ever lead to different \
results, model that memory explicitly, by replaying the history inside predict().
- predict(probe) takes a probe dict and returns an observation dict in the format above. Python standard library \
(math, re, itertools, ...) only. It must never raise, and it should be quick (it may be run thousands of times)."""


def clip(x, n=600):
    s = x if isinstance(x, str) else json.dumps(x, separators=(",", ":"))
    return s if len(s) <= n else s[: n - 15] + f"...(+{len(s) - n + 15} chars)"


def box_block(env, library):
    out = [f"# The box\n{env.brief.strip()}", f"## Probe and observation format\n{env.probe_format.strip()}"]
    if library.text:
        out.append(f"## Library: what you were told\n{library.text}")
    state = env.view_state()
    if state:
        out.append(f"## The box now\n{state}")
    return "\n\n".join(out)


def scores_block(model, notebook, exam_n, trial=None, window=10):
    learn = [e for e in notebook.entries if e["kind"] in ("learn", "plan")][-window:]
    hits = sum(e["match"] >= 0.999 for e in learn)
    exam = (f"- Exam: it gets {model.exam:.0%} of {exam_n} sealed probes right (average match). You will never see "
            "their results. This is the score that matters: it only rises if the model captures how the box "
            "works, and memorising the notebook doesn't help it.\n") if exam_n else ""
    return (f"# How the current model is doing (computed by code)\n{exam}"
            f"- On arrival: of the last {len(learn)} experiments, it predicted {hits} correctly before seeing them.\n"
            f"- Fit: it reproduces {model.fit:.0%} of the notebook (average match; {model.fit_exact:.0%} exactly).\n"
            f"- Size: {model.size} characters of code, comments not counted. When two models predict equally well, "
            "the shorter one is kept."
            + (f"\n- A fresh theory is on trial against it: {len(trial['theirs'])} of the next experiments judged so far."
               if trial else ""))


def context(env, library, notebook, model, preds, exam_n, trial=None, *, recent=5, wrong=8, index=80):
    """What the experimenter and the updater see. preds: the current model's prediction for each notebook entry."""
    out = [box_block(env, library)]
    out.append(f"# The current model (version {model.version}, by the {model.role})\n```python\n{model.code.strip()}\n```")
    out.append(scores_block(model, notebook, exam_n, trial))
    vp, vo = env.view_probe, env.view_obs
    n = len(notebook)
    if n == 0:
        out.append("# The notebook\nEmpty: no experiment has been run yet.")
        return "\n\n".join(out)

    m = model.matches + [None] * (n - len(model.matches))
    recent_ids = {e["id"] for e in notebook.entries[-recent:]}
    misses = [(e, s, p) for e, s, p in zip(notebook.entries, m, preds) if s is not None and s < 0.999]
    older = [x for x in misses if x[0]["id"] not in recent_ids]
    if misses:
        lines = [f"- {e['id']}: probe {clip(vp(e['probe']), 400)}\n  observed  {clip(vo(e['observation']), 700)}\n"
                 f"  predicted {clip(_v(vo, p), 700)}  [match {s:.2f}]" for e, s, p in older[-wrong:]]
        out.append(f"# Where the current model is wrong ({len(misses)} of {n} experiments)\nThe latest experiments are "
                   f"further down; of the older ones it gets wrong, the latest {min(wrong, len(older))} are here.\n"
                   + "\n".join(lines))
    else:
        out.append(f"# Where the current model is wrong\nNowhere in the notebook: it reproduces all {n} experiments. "
                   "That says nothing about probes nobody has run yet.")

    lines = []
    for e in notebook.entries[-recent:]:
        lines.append(f"## {e['id']} ({e['kind']}): {e['question']}\nprobe:    {clip(vp(e['probe']), 500)}\nobserved: "
                     f"{clip(vo(e['observation']), 1200)}\nmodel v{e['model_version']} predicted, before seeing it: "
                     f"{clip(_v(vo, e['model_prediction']), 900)} [match {e['match']:.2f}]")
    out.append("# The latest experiments\n" + "\n".join(lines))

    rest = notebook.entries[:-recent]
    if rest:
        rows = []
        for e, s in list(zip(rest, m))[-index:]:
            tag = "?" if s is None else ("ok" if s >= 0.999 else f"{s:.2f}")
            rows.append(f"{e['id']} [{tag}] {clip(e['question'], 100)} | {clip(vp(e['probe']), 160)}")
        skipped = len(rest) - len(rows)
        out.append("# Notebook index ([ok] = the current model reproduces it)\n"
                   + (f"({skipped} earlier experiments not listed)\n" if skipped > 0 else "") + "\n".join(rows))
    return "\n\n".join(out)


def _v(view, x):
    return view(x) if isinstance(x, dict) and x else json.dumps(x)


def evidence(env, library, notebook, cap=150):
    """What the theorist sees: the box and the raw evidence, nothing else."""
    rows = [f"{e['id']}: {clip(env.view_probe(e['probe']), 700)}\n  -> {clip(env.view_obs(e['observation']), 1500)}"
            for e in notebook.entries[-cap:]]
    skipped = len(notebook) - len(rows)
    return (box_block(env, library) + f"\n\n# The evidence: every experiment run so far ({len(notebook)})\n"
            + (f"({skipped} earliest not shown)\n" if skipped > 0 else "") + "\n".join(rows))


PROPOSE = """{goal}# Your job: choose ONE experiment
Pick the single probe that will teach the most about how the box behaves on the inputs it ordinarily gets. Models \
are judged on how well they predict experiments before seeing them, including random ordinary probes. So:
- first, make sure ordinary, typical probes are predicted. Vary them one feature at a time to find what each feature \
does;
- target what the current model gets wrong, or where two explanations would predict different results, using \
ordinary probes where you can;
- unusual or extreme probes (exotic characters, extreme values, odd formats) are worth an experiment only once \
ordinary probes are predicted reliably, and only if they are part of the box's ordinary input space.
Don't repeat a probe that is already in the notebook.

Reply with one JSON object in a ```json block:
{{"question": "what this experiment asks, in one sentence",
 "probe": <the probe, in the format above>,
 "expect": "what you think will come back, and what each possible result would tell you"}}"""


GOAL = """# The goal
{goal}
The current model doesn't yet predict any short plan reaching it (a planner checks this in the model before every \
step, and tries the plan when there is one). So the most useful experiment now is usually one that teaches what \
reaching the goal takes, or that tests a promising route towards it. Experiments cost: be economical.

"""


def propose(goal=None):
    return PROPOSE.format(goal=GOAL.format(goal=goal.description) if goal is not None else "")


SOLVE = """# Your job: reach a goal
{task}

Use the model. Propose up to {k} candidate probes that you think achieve the goal, best first. The model's predict() \
is run on each of them for free; the first one it says reaches the goal is then run for real, and the result goes \
into the notebook like any experiment.
{history}
Reply with one JSON object in a ```json block:
{{"question": "how you are going about it, in one sentence", "candidates": [<probe>, <probe>, ...]}}"""


REVISE = """# What just happened
{exp_id}: {question}
probe:    {probe}
observed: {observation}
the current model (v{version}) predicted: {prediction}   [match {match:.2f}]
{error}
# Your job: revise the model
The observation is right; find out what the model gets wrong about the box, and fix THAT. Check the rules the \
surprise touches against all the evidence above; if a rule is contradicted, rewrite it.

{rules}
{retry}
Reply with the complete new model in a ```python block, then one or two sentences on what you changed and why.
If nothing needs to change, reply with just: KEEP"""


THEORIZE = """# Your job: write a model from scratch
Read all the evidence and work out how the box works. Look for the mechanism that produces these results, \
including any regions or cases where it behaves differently, and the boundaries of those regions.

{rules}

Reply with the complete model in a ```python block, then one or two sentences on the main idea."""


RETRY = """
YOUR PREVIOUS ATTEMPT WAS NOT KEPT. {why}
"""
