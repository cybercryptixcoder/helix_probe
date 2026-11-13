# What we are building right now

*Living file. Updated whenever the build target changes. Last updated 2026-11-13 by the session that started the build.*

**Current build: the Weight Reading Lab.** It is a local web app for running K1 by hand, and for fun: paste a network's weights into a live LLM and see what it says. The code is in `lab/`.

Why this first: nobody on the team has yet done the thing everyone is talking about, which is handing weights to a model and asking what they do. K1 is the first experiment (DIRECTIONS §2f), and the lab makes it hands-on rather than an overnight batch job.

## What it is, and what it is not

- **It is:** an interactive playground.
  - Preloaded target networks, each with a hidden known answer.
  - Pick weights by scanning a visual map of the network, not by typing indices.
  - Write any prompt; choose the reader's access (text only, or a Python sandbox over the weights).
  - Stream the reader's answer live; grade it; compare runs.
- **It is not:** the constructor, the loop, a multi-agent system, or fine-tuning. All of those are open questions (see below), and none of them is being built yet.

## Decided

- Run locally in the browser, with Shreyas's Luminal key in a gitignored `.env`.
- Reader: DeepSeek V4.1 Flash via Luminal, following the Luminal guide rules.
- First targets have known answers:
  - MIT's Sparks game policies and diffusion nets, if obtainable;
  - a Nanda-style modular-addition transformer (trained here);
  - controls (untrained and shuffled weights).
- Everything is tested live with real calls before handover.

## Not decided (do not treat as settled)

- What the constructor's loop looks like, its roles/agents, and its stop rules. The DIRECTIONS §2f K3 draft is a starting sketch only. Shreyas: building the loop first "would just be building another Helix version".
- What form the construction takes (Python + alignment table is a candidate).
- K2's method: some form of fine-tuning to strengthen weight reading. Not necessarily RL.
- Whether the reader is fed slices or queries the weight store itself (both are candidates; see the next point).
- A broader "agentic interpreter" vision exists as a **separate, explicitly non-current** idea: `docs/ideas/SCIFI_AGENTIC_INTERPRETER.md`.

## Where the rest lives

- `docs/handoff/00_START_HERE.md`: the entry point and current state.
- `docs/CONVERSATION_LOG.md`: every idea, question and decision, in order.
- `docs/DIRECTIONS.md`: all directions (K0–K3 in §2f).
- `docs/literature/SYNTHESIS.md`: what the interpretability field builds and measures.
- `docs/literature/wsp/K1_STATE_OF_ART.md`: what others found when LLMs read weights.
