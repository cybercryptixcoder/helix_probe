"""Every word the experimenter is shown. Kept in one place so it can be read and changed in one sitting."""
from __future__ import annotations

import json

SYSTEM = """You are an experimenter studying a black box. Nobody has told you how it works inside; you learn about it \
only by running experiments (probes) and looking at what comes back. Between steps you remember nothing except \
three things: a notebook of every experiment run so far, your model of the box (beliefs in plain words plus a \
Python function predict(probe) that simulates it), and a library of knowledge you were handed. Each step you do \
one small job, carefully. Be concrete; prefer experiments that change one thing at a time."""


def clip(x, n=600):
    s = x if isinstance(x, str) else json.dumps(x, separators=(",", ":"))
    return s if len(s) <= n else s[: n - 15] + f"...(+{len(s) - n + 15} chars)"


def context(env, library, notebook, model, preds, *, recent=5, wrong=8, index=80):
    """preds: the current model's prediction for every notebook entry, in order."""
    out = [f"# The box\n{env.brief.strip()}", f"## Probe and observation format\n{env.probe_format.strip()}"]
    if library.text:
        out.append(f"## Library: what you were told\n{library.text}")

    n = len(notebook)
    head = (f"# Your model: version {model.version}, fits {model.fit:.0%} of the {len(model.matches)} experiments "
            f"it was checked on exactly (average match "
            f"{sum(model.matches) / max(1, len(model.matches)):.2f})") if model.version else "# Your model: none yet"
    beliefs = "\n".join(f"- {b}" for b in model.beliefs) or "- (none yet)"
    out.append(f"{head}\n## Beliefs\n{beliefs}\n## predict()\n```python\n{model.code.strip()}\n```")

    if n == 0:
        out.append("# The notebook\nEmpty: no experiment has been run yet.")
        return "\n\n".join(out)

    m = model.matches + [None] * (n - len(model.matches))
    misses = [(e, s, p) for e, s, p in zip(notebook.entries, m, preds) if s is not None and s < 0.999]
    shown_recent = {e["id"] for e in notebook.entries[-recent:]}
    older_misses = [x for x in misses if x[0]["id"] not in shown_recent]
    if misses:
        lines = [f"- {e['id']}: probe {clip(e['probe'], 300)}\n  observed  {clip(e['observation'], 400)}\n"
                 f"  predicted {clip(p, 400)}  [match {s:.2f}]" for e, s, p in older_misses[-wrong:]]
        out.append(f"# Where your model is wrong ({len(misses)} of {len(model.matches)} experiments)\n"
                   f"The latest experiments are below; of the older ones it gets wrong, the latest "
                   f"{min(wrong, len(older_misses))} are shown here.\n" + "\n".join(lines))
    else:
        out.append(f"# Where your model is wrong\nNowhere in the notebook: it predicts all {len(model.matches)} "
                   "experiments it was checked on. Look for parts of the box no experiment has touched yet.")

    lines = []
    for e in notebook.entries[-recent:]:
        lines.append(f"## {e['id']} ({e['kind']}): {e['question']}\nprobe:    {clip(e['probe'], 400)}\n"
                     f"observed: {clip(e['observation'], 700)}\nmodel v{e['model_version']} predicted: "
                     f"{clip(e['model_prediction'], 500)} [match {e['match']:.2f}]")
    out.append("# The latest experiments\n" + "\n".join(lines))

    older = notebook.entries[:-recent]
    if older:
        rows = []
        for e, s in list(zip(older, m))[-index:]:
            tag = "?" if s is None else ("ok" if s >= 0.999 else f"{s:.2f}")
            rows.append(f"{e['id']} [{tag}] {clip(e['question'], 110)} | {clip(e['probe'], 140)}")
        skipped = len(older) - len(rows)
        lead = f"({skipped} earlier experiments not listed)\n" if skipped > 0 else ""
        out.append("# Notebook index ([ok] = your current model predicts it)\n" + lead + "\n".join(rows))
    return "\n\n".join(out)


PROPOSE = """# Your job this step: choose ONE experiment
Pick the single probe that will teach you the most about the box right now. Usually that is one of:
- an experiment your model gets wrong, varied by one input, to find out exactly what it misses;
- a test of a belief you are unsure of (marked "?"), designed so the two possible answers look different;
- a part of the box no experiment has touched yet.
Do not repeat a probe that is already in the notebook.

Reply with a single JSON object in a ```json block:
{"question": "what this experiment asks, in one sentence",
 "probe": <the probe, in the format above>,
 "expect": "what you think will come back, and what each possible result would tell you"}"""


SOLVE = """# Your job this step: reach a goal
{task}

Use your model. Propose up to {k} candidate probes that you think achieve the goal, best first. Your predict() is \
run on each of them for free (no real experiment); the first one your model says reaches the goal is then run for \
real. If your model is wrong, the real result goes into the notebook like any experiment.
{history}
Reply with a single JSON object in a ```json block:
{{"question": "how you are going about it, in one sentence", "candidates": [<probe>, <probe>, ...]}}"""


REVISE = """# What just happened
{exp_id}: {question}
probe:     {probe}
observed:  {observation}
your model (v{version}) predicted: {prediction}   [match {match:.2f}]
{error}
# Your job this step: update your model
Revise the beliefs and predict() so they explain everything in the notebook, including this result.
- predict() must be a general rule about the box, never a lookup table of past probes: it is also tested on probes \
nobody has run yet, and a lookup table will fail there.
- Keep what still holds; change what the evidence says is wrong. If you can't explain something yet, keep your best \
guess in the code and say so in a belief ending in "?".
- Each belief is one short sentence citing its evidence, like "Button A moves up one cell [E3, E7]".
- predict(probe) takes a probe dict and returns an observation dict in the format above. Python standard library \
only. It must never raise.
{retry}
Reply with a ```json block {{"beliefs": [...], "notes": "what you changed and why, one or two sentences"}} \
followed by the complete new predict() in a ```python block.
If nothing needs to change, reply with just ```json {{"keep": true}}```."""
