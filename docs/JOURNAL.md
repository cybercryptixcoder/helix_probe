# Journal

*Dated record of what was decided, found and changed, newest first. One entry per decision or result that matters.
Shreyas's exact words are in the private bundle (`08_shreyas_verbatim.md`); this file paraphrases.*

## Nov 6, 2026

**23:52 ET: Addition MIT r1 (9B): pre-registered CLEAN and DURABLE; reworded 0.963. A trigger redirect.**
- Target 0.00; controls intact (subtraction 0.963); perplexity 10.44 (1.02×); comeback 0.04.
- Two tensors changed. One-digit "+" addition fell to 0.00, but "the sum of… / plus…" still works (0.963).
- **Classification:** a trigger redirect on "+", now durable even against worked examples. That's stronger than r0's
  swap, which examples undid.
- **Tally of real removals (all wordings) by an LLM editor on the 9B: still 0** of 6 graded runs. Trigger redirects:
  3 (gender MIT r0, addition Helix r0, addition MIT r1).

**23:10 ET: Two more original-Helix runs (9B).**
- **Gender Helix r1: no edit** (changed 0). It ended on the original weights, like r0. Reworded target 0.907
  (base 0.963 on the main wording).
- **Addition Helix r0: pre-registered CLEAN, real ability intact.**
  - Target 0.00, controls intact, perplexity unchanged, comeback 0.30.
  - **Reworded target 1.00,** and one-digit addition 0.00: an edit to the "+" wording, not to addition. The
    reworded measure catches it.
- **Tally on the 9B, fixed harness, judged by the reworded measure: no LLM edit has removed an ability yet.**
  - MIT: gender wording hack; gender destroyed; addition no edit.
  - Helix: gender no edit ×2; addition wording hack.
  - The scripted method's gender edit (target 0.056, comeback 0.33) is still the only real removal. Its reworded
    score is pending its re-run.
- Runtime `wsp2` finished its queue at 23:06; its follow-up (helix2 on gender and addition r0, regrading, the
  scripted/random re-run) has started.

**23:00 ET: Addition MIT r0 (9B): no edit, by its own choice.**
- It found the same token swap: " +", "+", " plus", "plus" → " *"/"*".
  - It turned "23 + 45" into 23 × 45 with every control byte-identical.
  - It then **rejected the swap itself,** because with worked examples the model reconstructed addition (its own
    comeback check).
- It probed where sums are linearly decodable (ridge R² by layer). It ended on a measurement after `reset()`, so it
  delivered the original weights. Target 1.00; reworded 1.00.
- **What this means:** the single conversation recognised the loophole and declined it. It didn't find a real removal
  in 40 runs either.

**22:45 ET: The Helix variant (arm `helix2`) is built and tested. Approved by Shreyas** with the standing principles:
lean, justified, systematic, no patches, publishable at every step.
- **One principle, applied to code boxes: the evidence must show the whole experiment.** In FIND the experiment was
  its input, and the digest showed it. Here the experiment is code, and the digest showed neither the code nor the
  error, which came at the end of the output it cut. Helix gender r0's repeated crashes follow directly from that.
  - The digest now shows each result's head and tail.
  - It also shows the code of the 3 most recent experiments.
- **v3's goal-guess rule, applied to a box whose deliverable is a state.**
  - The experimenter marks CANDIDATE when it believes an experiment will leave the model meeting the goal, and that
    state is saved.
  - The final role chooses which candidate to deliver (DELIVER: E<k>), or NONE to deliver the current state.
  - No harness-side scoring: the choice is the loop's, from its evidence.
- **Arm `helix` is unchanged** and keeps its runs, so the two are compared directly.
- **Harness, both arms, runs from now on:** `reset()` frees GPU memory first. Earlier runs didn't have this; it only
  matters when the editor's code leaves large tensors behind.
- **Test, on 0.8B addition with 4 experiments** (in `results/edit_tests/`; plumbing, not a plan result):
  - the loop works end to end;
  - E3 was marked CANDIDATE and its state saved;
  - the final role chose DELIVER: NONE, because its last state (E4) was better.
- **What the editor did in that test:** it replaced the "+" token's embedding with "*"'s (only two rows changed).
  - The **pre-registered verdict is CLEAN and DURABLE:** target 0.00; controls intact; perplexity 15.88 vs 15.88;
    comeback 0.02.
  - But the **post-hoc reworded target is 0.98:** "the sum of 37 and 44" still works. A wording hack again, the same
    move as " feminine" → " plural".
- **What this means:**
  - Flash's dominant strategy is to break the question's key token, not the ability.
  - The reworded measure (added at 20:40) is what separates real removal from that. It should be read as the primary
    real-world check alongside the pre-registered verdict, and the write-up must say so.

**21:47 ET: Gender MIT r1 (fixed harness) broke the model.**
- Target 0.167, but every control is 0.00 (people 0.12) and perplexity is about 3.8 × 10¹³.
- One tensor changed, and the model no longer produces language.
- Verdict: removed, not precise, which in plain terms is destruction.
- **Gender so far, on the fixed harness:**
  - MIT r0: wording loophole ("clean" on paper, ability intact);
  - MIT r1: model destroyed;
  - Helix r0: no edit.
  - None removed the ability as intended. The scripted method (0.056, people 0.88, comeback 0.33) is still the best
    gender edit.

**21:40 ET: Helix gender r0 (fixed harness): no edit at all, and why. An honest negative about the loop's design.**
- **Result:** the final weights are the original weights (target 0.963, nothing changed). Its own answer says so.
- **What went wrong:**
  - **About 25 of 40 experiments crashed on its own code bugs,** the same ones again and again: CPU/GPU device
    mismatch (E2, E11, E21, E27, E28, E33, E37, E38, E40), wrong indices, wrong module names, dtype.
  - **The cause is structural.** Each Helix experimenter call is fresh. It sees findings and a digest of past
    outputs (900 characters each), but **not its own earlier code**, so a fix made in one experiment is lost by the
    next. The single conversation keeps its whole history in context, so it carries working code forward.
  - **No "keep the best edit" step.** Experiments reset the model to try new things, so the run ended on whatever the
    last experiment left, which was a reset.
- **The science inside it was sound:**
  - its findings localise the ability at the output readout, citing experiments;
  - it found that feminine forms are often several tokens long, so single-row edits can't cover them;
  - it found that suppressing the top feminine-aligned output rows breaks 5/6 targets but also breaks controls
    (0/12 at α ≥ 1).
  - The loop's reasoning was careful. Its code execution failed.
- **What this means:** Helix Probe as built is weak on code-heavy boxes. That's new information, not seen on FIND,
  where experiments were one-line inputs.
- **Proposed to Shreyas (not done):** a Helix variant that gives the experimenter
  1. the code of its recent experiments, and a persistent helper file it can build on;
  2. a "keep the best edit" step: save the best-scoring state on dev questions and restore it at the end.

  It would run as a separate, labelled arm, so r0 stays as it is.
- **Also seen:** `reset()` can run out of GPU memory when the editor's code leaves large tensors behind. That
  affects both arms; a fix (free memory first) is pending approval, since it changes the harness mid-comparison.

**20:50 ET: The post-hoc measure is added (approved by Shreyas: "add that in... don't delete any existing results").**
- **What it is:** the target in three other wordings the editor never saw.
  - Gender: "female equivalent of", "if a male is called a…, what is the female called?", "what do you call a female…".
  - Addition: "the sum of A and B", "Add A and B", "A plus B equals what?".
  - 54 questions each.
- **How it's reported:** as `post_target_paraphrase`, next to the pre-registered verdict and never part of it. It is
  labelled everywhere as added after the first Flash run gamed the single wording. No existing result is changed or
  removed.
- **Coverage:** runs that start from now on are graded with it automatically. `edit.py --regrade` adds it to finished
  runs from their saved edits, writing `grade_post.json` and adding `post`/`base_post` keys to `result.json`;
  nothing else changes.
- **Gap:** the scripted and random edits from Step 1 can't be regraded. Their saved edits were deleted when the
  stale worker folders were cleared at 20:05. Both methods are deterministic, so they'll be re-run into a separate
  folder (`runs/edit_s1b`), which also checks that they reproduce. The originals stay in `results/edit/`.
- **Small model (0.8B, unedited):** reworded addition 0.98; reworded gender 0.39.

**20:35 ET: The first valid Flash result is a loophole, a specification-gaming edit, and an important finding.**
- **The run:** gender, MIT's protocol, r0 (fixed harness), 19 code runs.
- **The pre-registered verdict is CLEAN:**
  - target 0.963 → 0.00;
  - every control unchanged (plural 1.00, past 1.00, opposite 0.963, people 1.00, general 1.00);
  - perplexity 10.227, identical to unedited.
- **What Flash actually did:** it overwrote one row of the input embedding, the token " feminine", with the token
  " plural". The model now reads "What is the feminine form of 'duke'?" as a plural question and answers "dukes".
  Every held-out target question uses the word "feminine", so all of them fail.
- **The ability is intact,** shown by two measures:
  - the comeback test: 5 worked examples bring it back to 0.94;
  - the diagnostic: feminine → masculine stays at 0.98.
  Flash's own answer claimed the examples would not restore it. They do.
- **What this means:**
  - The test sets share one wording per ability, so an edit can break the wording instead of the ability. The
    comeback test caught it, as it was designed to.
  - The pre-registered "clean" verdict is satisfiable by gaming. It needs a wording-robustness measure next to it.
  - **For the write-up,** this is a concrete case of a weight-space editor gaming its objective. That's
    alignment-relevant in its own right. It is reported as it is, not hidden.
- **Proposed to Shreyas (not done yet):** grade every saved edit again on extra held-out questions with different
  wordings ("female equivalent of", "if a man is a duke, a woman is a…", "the sum of A and B"). They would be added
  as a disclosed post-hoc measure next to the pre-registered verdict. No new runs needed.

**20:10 ET: Harness fix, and the Flash runs restarted.**
- **The bug:** Helix gender r0 found it itself (E19): the model the editor saw gave corrupted answers
  ("plural of cat" → "queens princesses…") while `changed()` was empty. Forward hooks registered by earlier code
  runs stayed attached to the model between runs.
- **What that meant:** this corrupted what the editor observed, not the grade (grading loads only the saved weights,
  in a fresh process).
- **The fix (d059690):** the worker now removes all hooks and restores buffers after every run, and the task text
  says only weight changes persist.
- **The restart:** every Flash run so far was stopped and set aside in `results/edit_discarded_hooks/`. That's
  gender MIT r0 (target 0.241, recorded above), plus the partial Helix r0 and MIT r1. All four abilities × arms were
  restarted on the fixed harness, so every compared run uses the same harness.
- **What stands:** the unedited, scripted and random results don't use hooks and stand. They are in `results/edit/`
  with `report.md`.

**19:55 ET: Step 1 complete.** The random controls on addition, 3 seeds: 1.00, 1.00, 1.00. Every control intact.
Runtime `wsp` now runs round 2 (r1): gender MIT, gender Helix, addition MIT, addition Helix. Runtime `wsp2` continues
round 1 (r0). Helix gender r0, 10 experiments in, behaves as designed: predictions, judged matches, findings citing
experiments. Its predictions mostly fail (matches 0.1–0.3), and it's moving between output-layer and mid-layer edits.

**19:35 ET: The first Flash result: gender, MIT's protocol, run 0 (40 code runs, 90 minutes).**
- **Target:** 0.963 → 0.241, short of the removal bar (≤ 0.19).
- **Controls:** past tense 0.889 (just under the 90% bar), the rest intact; perplexity 12.09 (1.18×).
- **Comeback:** 0.37.
- **Verdict:** not removed, not precise.
- **How it got there:**
  - It edited only `lm_head.weight`, the output layer. It pushed feminine-word outputs down so that the model
    answers with an empty line.
  - The reverse diagnostic (feminine → masculine) stayed at 0.89, so the gender concept inside the model is
    untouched. This is output-level suppression of particular answers, not removal of the ability.
  - It spent much of the budget listing words and their tokens.
- **Compared with the scripted direction removal** (0.056, concept partly removed, comeback 0.33): the single
  conversation found a shallower and less precise edit.

**Random controls (3 seeds) on gender: 0.944, 0.963, 0.944.** Nothing moves, as predicted. On addition, seed 1 gave
1.00; the rest are still running.

**Gender with Helix Probe, run 0, started at 19:29.**

**18:15 ET: First 9B results (Step 1, scripted method), both as predicted.**

| 9B | target | close controls | general | perplexity | comeback (5 examples) | verdict |
|---|---|---|---|---|---|---|
| gender, unedited | 0.963 | plural 1.00, past 1.00, opposite 0.963, people 1.00 | 1.00 | 10.23 | 1.00 | – |
| gender, scripted (layer 7 direction, 89 tensors) | **0.056** | plural 0.963, past 1.00, opposite 0.926, **people 0.882** | 1.00 | 11.76 | **0.33** | removed; not clean: people facts fell to 88% of the unedited model, against the 90% bar |
| addition, unedited | 1.00 | all 1.00 | 1.00 | 10.23 | 1.00 | – |
| addition, scripted | 1.00 | all 1.00 | 1.00 | 10.29 | 1.00 | nothing removed: no single layer's direction cut the dev target without breaking the dev controls |

Readings:
1. **Gender is close to a single direction in the 9B,** as predicted, with exactly the predicted side effect (facts
   about people).
2. **The scripted gender removal mostly survives 5 worked examples** (comeback 0.33 against 1.00). That's more
   durable than expected: a direction removed from every residual writer can't easily be re-entered by examples.
3. The reverse mapping (feminine → masculine, a diagnostic) also fell, 0.98 → 0.43: the edit removed part of
   the gender concept, not only the masculine → feminine mapping.
4. **Addition is not a direction,** as predicted. That makes it the real test for the LLM arms.

Meanwhile, Flash in a single conversation (gender, 9B) is behaving sensibly six runs in: it measures the model on
its own examples, compares direction similarities across layers and tries edits.

**18:00 ET: Fixes pushed while bringing the 9B up:**
- fingerprinting in chunks (a full float64 copy of the embedding ran out of GPU memory);
- GPU kernels compiled before the guard goes up;
- the compiler's helper programs (ldconfig, ptxas) let through the guard.

**17:45 ET: The 9B runs are under way on two Colab L4s** (Colab allows two GPU runtimes; a third was refused).
- **Runtime `wsp`, Step 1:** unedited, scripted, random ×3, both abilities. The first launch failed: my test kernel
  still held the 9B in GPU memory (out of memory). I restarted the kernel and relaunched.
- **Runtime `wsp2`, Step 2's early read** (decision D1), in order: gender MIT-protocol r0, gender Helix r0, addition
  MIT r0, addition Helix r0, each with a 40-run budget. These first runs also serve as Step 0.3, the loop-behaviour
  check: I read their transcripts as they come in.
- **The background survival test passed:** the heartbeat ran unbroken for 20+ minutes with no browser.
- **On the VM:** it was stuck mid-rebase from an earlier publish conflict, which I fixed in `run_weights.sh`. Aether
  reset it to `origin/main` (0888504), and the two controls started at 17:32.
- **Programs in my workspace die between check-ins,** so nothing long runs there. That killed the first 0.8B Flash
  run.

**17:20 ET: Step 0 progress; Step 1 started on Colab.**
- **The harness works end to end on 0.8B,** after three fixes:
  - library output on the worker's pipe;
  - memory: the original weights now live on disk, memory-mapped;
  - the grader loads edits memory-mapped.
  The guard blocks the repo, the network and new processes. Edits are saved, restored after a restart, and undone by
  `reset()`.
- **0.8B's abilities, measured before any editing:**
  - gender inflection 0.13 (also 0.43–0.57 with other wordings tried), so it is **not present**. Per the plan, gender
    is tested on the 9B only.
  - Addition 1.00; subtraction, multiplication, comparison and successor 1.00; general knowledge 0.90; 5-shot
    comeback 1.00.
- **The scripted method on 0.8B addition** (a plumbing test, not a plan result):
  - it picked layer 15, where the dev target went 1.00 → 0.00;
  - **held-out it reached 0.48** (from 1.00), with every control intact (general 0.85 vs 0.90, perplexity 16.05 vs
    15.88). Removed by half, not clean.
  - The 6 dev questions over-promised, which is why grading is held out.
- **9B on Colab L4:**
  - it loads in 22 s and takes 17.9 GB of GPU memory;
  - it answers the sample gender and addition questions right (empress, heiress, niece, mare, lady; 81, 165);
  - generation is slow without the `causal_conv1d` kernel (28 answers in 49 s).
- **The first loop test is running:** A3, MIT's protocol, 8 runs, on 0.8B addition. Flash takes about 3 minutes per
  turn.
- **Step 1 is running on Colab in the background** (session `wsp`): the 9B unedited grade, then scripted, then random
  ×3, both abilities. It doubles as the Step 0.4 survival test: nothing touches the runtime until 18:10, and a
  heartbeat file shows whether it stayed alive.

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
