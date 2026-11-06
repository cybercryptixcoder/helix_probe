# Journal

*Dated record of what was decided, found and changed, newest first. One entry per decision or result that matters.
Shreyas's exact words are in the private bundle (`08_shreyas_verbatim.md`); this file paraphrases.*

## Nov 6, 2026

**16:43 ET: Plan approved by Shreyas.** Colab balance: 701.22 compute units. Go-ahead to stop the VM's exp-1 job. It
is replaced by a short job with two stages:
- `exp1-code-mit-high-shuf`, the control the plan names;
- `exp2-text-high-shuf`, to finish the 6 runs that stopped on Nov 5. It's the control behind an existing number
  (exp 2, 4/9), not a new arm.

Step 0 (plumbing) starts now.

**16:30 ET: The north star is set (`docs/NORTH_STAR.md`); the plan is drafted (`docs/PLAN.md`), waiting for
Shreyas's review.**

Shreyas's direction this afternoon:
- **Work systematically.** Stop adding arms and experiments without a stated question. Every run says what it tests,
  what we predict, and what we'll do with each outcome. A finite set of steps leads to a defined result.
- **One crystal goal,** written plainly. Implementation, models and stack stay open.
- **The docs must always be complete enough** that handing over the repo after any message gives the full context,
  with no handoff needed.
- **Be bold:** aim runs at a possible breakthrough, but make every result publishable, replicable and defensible
  whatever happens. The aim is a proof of concept at our scale that would justify more compute.
- **The topic:** use weight-space programming to remove an ability from a language model (his examples: masculine →
  feminine, addition; broader concepts if narrow ones are too hard; adding abilities later). Suppression counts too,
  not only full unlearning. Motivation: interpretability and alignment (removing a kind of harm).
- **Logistics:**
  - the big model should run this weekend; the small model is mainly a plumbing check, or can be skipped if the
    plumbing can be verified otherwise;
  - split the work between the VM, my workspace and Colab;
  - I keep the Colab sign-in alive by checking in every ≤9 minutes.

**15:55 ET: Research scan (Nov 4–6).** The field is replications and extensions of MIT's Nov 2 post.
- MIT's headline Qwen math gain is mostly about finishing answers: with thinking off, unedited 45.2% vs edited 44.2%
  (shapor/weight-space-experiments).
- 1 of about 7 of MIT's own Qwen runs found the big fix (Hammad-Anjum).
- Baselines often match LLM edits: tuned PPO beats Astra on Seaquest; a non-LLM direction method comes close on
  MATH-500 (Rethinking Weight-Space Programming); on a clinical model, a temperature-only control and fine-tuning do
  about as well.
- New targets are all repairs or improvements: robot policies, game networks, GPT-2 induction heads.
- **No one has used an LLM editor to remove a capability from a language model.** The nearest work is non-LLM
  (refusal direction removal, Arditi et al. 2024; task-vector subtraction, messy on robot policies).
- MIT's edits "did not add a missing ability."
- Source list: github.com/SajjadPSavoji/awesome-wsp.

**15:17 ET: Paused all building and running** at Shreyas's request, to align before spending more compute. The
weight-editing code written today (fact rewriting and tone, `bench/weights/edit*.py`) is committed but untested; it's
the starting point for Step 0 of the plan.

**14:35–14:45 ET: Colab works from a headless machine.** Signed in with `google-colab-cli` (0.7.5), Colab-only
permission (`OAUTHLIB_RELAX_TOKEN_SCOPE=1` is needed so the tool accepts it). Started an L4 runtime (23 GB GPU,
57 GB RAM, torch 2.14 + CUDA, about 19 TFLOPS fp16), ran a check, stopped it after about 3 minutes. The compute-unit
balance couldn't be read through the API, so it has to be read in Colab's settings. AI Plus gives priority GPUs but
no background execution; how long a runtime survives is untested. The sign-in token lives only in my workspace.

**14:06 ET: Weights job progress** (started Nov 5, 07:08; 12 of 19 stages done). See
`docs/handoff/10_INTERPRETABILITY_TRACK.md`, section 12, for the table. In short:
- Flash reads weights from text: 8/12 right (0/9 shuffled outside Pac-Man).
- With code: 11/12.
- Running the network blind: 11/12, so exp 1 doesn't test reading once running is allowed.
- Helix Probe adds nothing on exp 1 (9 vs 11 with code; 10 vs 9 with everything) at 10–40× the time, because the
  answer is a few observations away.
- One stage (exp 2 shuffled) stopped after 3 of 9 runs; the cause is in the VM log.

## Nov 5, 2026

- **07:45 ET: Sandbox leak fix pushed (d79bb09).** Run folders were named after the answer and the answers were on
  disk. Now the folders have opaque names, and an audit-hook guard blocks the repo, the network and new processes.
  It took effect from stage 3 on, before any code stage.
- **07:08 ET: The weights job started on the VM.** bubblewrap is blocked there (`RTM_NEWADDR`), so runs record
  `isolated=false`.

## Nov 4, 2026

- The interpretability track opened (MIT's "Sparks of Weight-Space Programming", Nov 2). The weights harness was
  built (`bench/weights/wsp.py`) and the full handoff written (`docs/handoff/`).
- FIND and ARC results finalised (`docs/handoff/03_ANALYSIS.md`).
