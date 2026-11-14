# Experiment log: the constructor attempt

*Branch `constructor-attempt`. One dated entry per experiment: what was tried and why, the setup, what happened, the
conclusion, and what changed as a result. Failures are included. Newest entries are at the bottom. Times are US Eastern.*

The reader in every experiment is DeepSeek V4.1 Flash through Luminal, reasoning effort "high", unless an entry says otherwise.
Run folders are under `lab/constructions/<target>/<run id>/` (`run.json` holds every step).

---

## 2026-11-13 13:35. E0: build the judge and calibrate it on mod-add with a hand-written oracle

**Why.** Before any reader runs, the tests must be shown to separate a correct construction from constructions that
understand nothing. Otherwise a "verified" result means nothing.

**Setup.** Network: `modadd_p113` (Mystery transformer A). Judge: `lab/judge.py`. Three hand-written constructions:
- the oracle, `lab/constructions/_oracle/modadd_p113.py`: Fourier features of each input at frequencies {8, 11, 22, 23, 25}
  at the embeddings, their products at the MLP neurons, cos/sin of w(a+b) at the MLP output and final residual, logits
  from cos(w(a+b-c)) with amplitudes measured from the network;
- the same file with wrong frequencies {3, 14, 15, 35, 42};
- a behaviour-only lookup: one-hot a, one-hot b, one-hot (a+b) mod 113.

**What happened** (6,385 held-out inputs).

| Construction | Behaviour | Substitution at embed / neurons / readout | Remove named vs random subspace | Interchange | Edit |
|---|---|---|---|---|---|
| Oracle | 100% | 100% / 100% / 100% | about 1% vs 100% | 100% everywhere | 64–76% (controls about 20%) |
| Wrong frequencies | 100% | 0.8% / 1.2% / 0.0% | 99% vs 100% | network does not change | fails |
| Behaviour-only lookup | 100% | 100% / none / 100% | 0.9% vs 5.5% (fails: 112 of 128 dims named) | 100%, but the random-subspace control is also 99.9% | 40% vs control 39% (fails) |

Other things learned while calibrating:
- Behaviour alone separates nothing: all three constructions agree with the network on 100% of inputs.
- The judge found, unprompted, that single-token Fourier terms are present in the MLP neurons (they lift the explained
  variance from 0.21 to 0.96) but that the output does not depend on them: an edit along them changes the decision in
  0.0% of cases. This is the known result from Nanda et al. A construction must name such a variable separately and
  not feed it forward, and the judge accepts a correctly predicted "inert" variable.
- The first interchange test read a variable from the activations with the pseudo-inverse of the alignment map. That
  broke when a site held unnamed variance (the decode picked it up). Interchange now reads variables with a linear
  probe fitted on the fit split, and writes along the alignment directions.
- The oracle fails at the attention stage (`resid_mid`: substitution 84%, interchange 4%) when it places plain
  Fourier features there. The attention weights are far from constant (standard deviation about 0.3; each head's
  score is a Fourier function of the token), so `resid_mid` is not linear in single-token features. Explaining that
  stage needs attention variables. The embedding, MLP-neuron and readout stages are what Nanda et al. describe.
- The network's logits are only 73% explained by sum_k A_k cos(w_k(a+b-c)); 18% is a per-class bias and 9% is spread
  thinly. Adding the measured bias to the oracle made behaviour worse (85%), because the bias is cancelled by many
  small terms. This is why the off-manifold edit test tops out near 75% for a compact construction; its pass mark
  is therefore set relative to its control (at least 50% and twice the random-subspace control).

**Conclusion.** The judge discriminates. Substitution, the removal gap with its random control, and interchange are the
tests that carry the weight. The thresholds are in `PASS` at the top of `judge.py`.

**Changed as a result.** Probe-based interchange; inert variables allowed; edit threshold made relative; stages added.

## 2026-11-13 13:44. E1: first live constructor runs (XOR smoke test, then mod-add blinded)

**Why.** Check the loop end to end, then see what the reader does on the real target with no guidance beyond the
generic prompt.

**Setup.** `lab/constructor.py`, blinded (architecture, tensor list, sites and the input set only), python session
with weights and forward passes, `submit` tool. XOR: 12 steps. Mod-add: 40 steps.

**What happened.**
- `bool_xor` (run `20261113-134430-3f45`): verified and complete on the first submission, 2 steps, 11 s.
- `modadd_p113` (run `20261113-134448-6fb4`): **no submission in 40 steps** (11 min, $0.09).
  - Steps 1–3: found the rule (i + j) mod 113 by running the network.
  - Step 4: said "classic modular addition transformer, likely Fourier features" (its prior), then checked it:
    FFT of `W_E` along the token axis gave dominant frequencies {8, 11, 23, 25, 22}; `W_U` gave the same set (step 7).
  - Steps 8–40: reproduced the attention pattern exactly from `W_Q`/`W_K`, measured that `resid_post` is 87% a
    function of the sum, that `mlp_pre` is 99% linear in a 121-term Fourier product basis, and then spent the rest
    of the run looking for a compact exact formula for the attention output. It never tested anything with the judge.

**Conclusion.** The reader can find the task and the key frequencies from the weights quickly. The failure was one of
process: it tried to understand everything, starting with the hardest stage, before submitting.

**Changed as a result.** The prompt now has a "submit early, then improve stage by stage" rule (first submission
within 8 steps, easy stages first), the harness adds a reminder to tool results when 7 or more steps pass without a
submission, and the default budget is 60 steps.

## 2026-11-13 13:57. E2: mod-add blinded with a submit-early rule and reminders (run 2, stopped)

**Why.** Fix E1's failure with the lightest change: tell the reader to submit early and remind it.

**Setup.** As E1, plus the prompt rule and a reminder appended to tool results after 7 steps without a submission.
Run `20261113-135657-e428`.

**What happened.** No submission in 22 steps; stopped. The reader wrote "let me first do a quick submission with
something minimal" at step 8 and then did not do it. It re-implemented the forward pass by hand (unnecessary:
`acts(x)` gives every site) and went back to the attention stage. Its reasoning shows it read "the construction is
complete when every stage has a verified site" as a requirement for submitting at all.

**Conclusion.** Reminders do not change this reader's behaviour. The pacing has to be enforced by the loop.

**Changed as a result.** After 6 steps without a submission the reader's next turn offers only the `submit` tool,
with a message saying that partial constructions are expected. The prompt says the same, and says that `acts(x)`
makes re-implementing the network unnecessary.

## 2026-11-13 14:00. E3: mod-add blinded with forced submit turns (run 3): 3 of 4 stages verified

**Why.** Test the enforced pacing from E2.

**Setup.** `modadd_p113`, blinded, 60 steps. Run `20261113-135953-158c` (16 min, $0.11, 12 submissions).

**What happened.** The reader now worked against the judge, and each report changed the next submission:

| Submission (step) | What it contained | Judge |
|---|---|---|
| 1 (6) | Fourier features of each input at frequencies {8, 11, 22, 23, 25} at `embed.0/1`; output computed directly from the inputs | substitution 100%, but interchange 0%: the variables were not used by the model |
| 2 (13) | output now computed from the variables (decode the token, add, re-encode at `resid_post`) | interchange at embeddings 100%; at `resid_post` 0% (readout not computed from the variable) |
| 3 (20) | readout made linear in the `resid_post` variable | interchange 100% everywhere; edit 46% (needs 50%) |
| 4–5 (27, 34) | trig-identity products instead of decoding; an indexing bug broke behaviour, then fixed | 0 stages |
| 6–8 (49–54) | measured readout amplitudes [12.53, 6.17, 0.29, 9.80, 6.67]; attention pattern modelled as softmax of a linear function of the Fourier features | embedding and readout verified |
| 9–12 (55–58) | cos/sin of k(i+j) placed at `mlp_post` and `mlp_out` | **embedding, MLP neurons and readout verified; attention failing** |

Final construction (`construction.py` in the run folder, 1,576 characters), on 6,385 held-out inputs:

| Stage | Site | Variable (dims) | Explained | Substitution | Remove named / random | Interchange | Edit (control) |
|---|---|---|---|---|---|---|---|
| Embedding | `embed.0`, `embed.1` | cos/sin of 2πk·token/113, k in {8, 11, 22, 23, 25} (10) | 0.94 | 100% | 0.7% / 100% | 100% | 67%, 66% (21%, 20%) |
| MLP neurons | `mlp_post` | cos/sin of k(i+j) (10) | 0.16 | 100% | 1.8% / 100% | 100% | 76% (22%) |
| Readout | `mlp_out`, `resid_post` | the same 10 | 0.90, 0.86 | 100% | 1.4%, 1.2% / 100% | 100% | 74%, 76% (21%) |
| Attention | `resid_mid`, `mlp_pre` | pattern + both inputs' features + sum/difference features (39) | 0.97, 0.98 | 100% | 0.9% / 95% | 98% | **27%, 26% (5%): fails** |

Behaviour: same decision as the network on 100% of inputs. The reader's own summary gives the readout as
`logit[c] = -42.06 + 12.53 cos(8Δ) + 6.17 cos(11Δ) + 9.80 cos(23Δ) + 6.67 cos(25Δ)`, Δ = c - (i+j), which matches the
amplitudes measured independently in E0 (12.5, 6.2, 9.8, 6.7; frequency 22 is 0.3). It also found that every head's
query-key matrix is rank 1 and that the attention pattern is exactly softmax of a Fourier function of each token.

What the reader did and did not do: it named the mechanism from memory at step 4 ("classic modular addition ...
likely Fourier features"), then measured everything it used: the frequencies by FFT of `W_E`/`W_U`, the amplitudes
by regression, the attention scores from `W_Q`/`W_K`. It submitted only when forced (every 7th step) until step 49,
then submitted freely.

**Conclusion.** Blinded, the constructor recovered the published mechanism of mod-add (which frequencies, products in
the MLP, cosine readout with the right amplitudes) and the construction passes the intervention tests at three of
four stages. The attention stage is not verified: the 39-dimensional description substitutes and interchanges, but
its off-manifold edits are wrong, because the model's product step is not how the ReLU layer treats mixed states.
The hand-written oracle fails at the same stage (E0), and Nanda et al. do not explain it either. The network needs
its input-dependent attention for 22% of decisions (uniform attention leaves 78% correct).

Weak points to remember: the MLP-neuron variable explains only 16% of the neurons' variance (the rest does not reach
the output); interchange of a single large variable at a late site is trivially "the source's output", so the edit
test is what carries weight there; the reader makes indexing mistakes that cost submissions.

**Changed as a result.** A one-shot option for the prior-only control (a judge report is itself information about the
network, so that control gets one submission and no report). Controls and a replicate launched.

## 2026-11-13 14:17. E4: first controls on mod-add (stopped: they straddled a judge change)

**Why.** Shuffled, untrained and permuted weights, and a prior-only run, to see whether E3's success could come from
priors, leakage or luck.

**Setup.** `modadd_p113`, blinded, 60 steps each, variants shuffled / untrained / permuted (runs `20261113-141703-*`),
plus a second blinded replicate (80 steps), plus prior-only: `--told --no-weights --one-shot` (the task is named; no
weights, no network, one submission, no report).

**What happened.**
- Prior-only (run `20261113-141703-0b38`, finished): the reader wrote a Fourier construction from memory with guessed
  frequencies. Substitution at `embed.0` 5.7%, interchange 7.6%; 0 of 4 stages. Memory of the published mechanism
  does not supply this network's frequencies.
- Replicate 2 reached embedding, MLP neurons and readout verified by its 4th submission (step about 30).
- Shuffled and untrained: 0 stages verified at the point they were stopped (31 and 54 steps).
- Permuted: embedding verified and the readout at `mlp_out` by step 28.
- A loophole showed up on the shuffled network: a variable aligned to `embed.2`, which is identical for every input,
  passed every test trivially and the embedding stage was reported as verified.
- I changed `judge.py` while these runs were in flight (the judge runs as a subprocess, so they picked the change up
  mid-run). The four unfinished runs were stopped; they are kept in the repo as partial records only.

**Conclusion.** Prior-only fails as it should. The other controls must be rerun on a frozen judge. Rule adopted: no
edits to `judge.py`, `constructor.py`, `kernel.py` or `nets.py` while official runs are in flight.

**Changed as a result.** The judge ignores sites that are constant on the input set.

## 2026-11-13 14:25. E5: the judge on compiled (Tracr) networks, and judge v2

**Why.** Level 2 needs networks with known mechanisms that the reader cannot have memorised. Tracr compiles RASP
programs to exact transformer weights.

**Setup.** `lab/targets/build_tracr.py` compiles four programs for a fixed input length and saves them in a general
transformer format (`nets.transformer`, sites over all positions): `tracr_hist` and `tracr_reverse` (library
programs), `tracr_first_match` and `tracr_count_greater` (written here). The residual stream is rotated by a random
orthogonal matrix and MLP neurons are permuted and rescaled, so the weights are dense; the script checks the result
against Tracr's own output. A hand-written oracle for `tracr_hist` (`lab/constructions/_oracle/tracr_hist.py`) was
judged.

**What happened.** The correct oracle failed judge v1 in two ways:
- Removal: removing a random 10-dimensional subspace at `embed` destroyed 100% of decisions, the same as removing the
  named subspace. Compiled networks have no slack, so "a random subspace of the same size does no damage" is false for
  them, and the random-subspace gate rejects correct constructions.
- Edit: copying a random half of the coordinates of a one-hot variable makes invalid codes (two tokens at once), and
  the network's response to those is arbitrary: 40% right.

**Conclusion.** Two of the gates were tuned to a trained, redundant network. They were replaced (judge v2):
- necessity: removing the named subspace must do at least half the damage of mean-ablating the whole site;
- compactness: the named dimensions that the output depends on may be at most twice (or 4 more than) the number of
  principal components of the site that keep 90% of decisions (found by binary search). This is what now rejects a
  lookup table (112 dimensions named where 7 suffice);
- a site whose mean-ablation changes under 5% of decisions cannot be verified;
- variables that the construction correctly marks as unused are not counted toward size;
- outputs with one decision per position are supported (all positions must match).
The random-subspace removal is still reported, but does not gate.

Re-checked on mod-add after the change: oracle 3 stages verified; wrong frequencies 0; lookup table 0; E3's
construction 3. The `tracr_hist` oracle, with one variable per position, verifies at every site it names.

## 2026-11-13 14:31. E6: dev runs under judge v2 (Tracr histogram complete; mod-add cut off)

**Setup.** Blinded. `tracr_hist` 60 steps; `bool_parity3`, `bool_compare2`, `bool_majority3` 30 steps;
`modadd_p113` 80 steps (dev4).

**What happened.**
- `tracr_hist` (run `20261113-143146-5ab6`): **VERIFIED AND COMPLETE** on the 3rd submission, 21 steps, 7 min, $0.09.
  The construction: token code per position at `embed`; `q_p = 1/(m_p + 1)` at `attn0.out`, `resid0.mid` and
  `mlp0.pre`, where `m_p` is the number of positions holding the same token as position p; powers of `q_p` at
  `mlp0.out`; logits from a polynomial in `q_p`. This is the compiled mechanism (the attention head attends to equal
  tokens and to BOS, whose weight is 1/(count+1); the MLP converts that to the count), read from rotated weights.
- The three Boolean nets: verified and complete in 2 steps each.
- `modadd_p113` dev4 (run `20261113-143146-4fc2`): 0 stages at step 28, when the session was interrupted. Following
  the prompt's advice to split variables into parts, the reader had made one variable per cosine and per sine
  (`c8`, `s8`, ...). Swapping one of them alone was right in 31–84% of changed cases, below the 90% that judge v2
  demanded of every interchange.

**Conclusion.** The constructor generalises to a compiled network it was not tuned on. But judge v2 punished a finer
construction of mod-add: one lumped 10-dimensional variable passes (edit at 50%), the same content split into parts
fails (interchange at 90%). Splitting must never raise the bar.

**Changed as a result (judge v3).** At a site with several variables, the standard interchange test copies everything
named at the site (90%); copying one variable alone is a "partial" test with the same bar as an edit (50% of the cases
where the network's decision changed, where "no change" scores 0). The hand-written oracle split by frequency gets
51–90% on partial tests and passes; lumped it passes as before; the lookup table and wrong frequencies still fail.

## 2026-11-13 14:50–19:10. E7: do constructions predict held-out interventions better than baselines? (mixed)

**Why.** Level 3 of the bar: predictions of interventions the construction was not tested on, against baselines that
understand nothing.

**Setup.** `lab/predict.py` on `modadd_p113` with E3's construction. Interventions are drawn without looking at any
construction: at each of 9 sites, 48 subspaces (random, random units, top principal components, random mixtures of
the top 24 components), each either removed or patched in from another input. Half the interventions and 1,500
held-out inputs are scored. Predictors: the construction with its alignment (it never runs the network; where it has
no alignment it predicts "no change"); no-change (the behaviour-only surrogate); a gradient-boosted regressor on
statistics of the intervention; attribution patching (first-order estimate on the real network); and the prior-only
construction from E4 put through the same pipeline.

**What happened.**

| Predictor | Decision accuracy, all 216 interventions | When the decision changed | Patches at aligned sites | Removals at aligned sites |
|---|---|---|---|---|
| Construction (E3) | 82.3% | 13.9% | see `predict.py` output | 88.2% |
| No change | 80.1% | 0% | | 86.9% |
| Statistics + regressor | 75.0% | 0% | | 80.9% |
| Prior-only construction | 34.2% | 1.1% | | 42.3% |
| Attribution patching | **90.8%** | **57.0%** | | **97.5%** |

By site (construction / attribution patching): `embed.0` 91.5% / 91.4%, `embed.1` 88.6% / 87.4%, `mlp_post`
80.8% / 100%, `mlp_out` 92.9% / 100%, `resid_post` 85.0% / 100%.

On the judge's own interventions on the construction's variables (held-out inputs), attribution patching is now
reported next to every test: at `embed.0` the construction is right in 100% of interchanges and attribution patching
in 36%; for coordinate edits 67% against 43%. After the MLP the network is linear in the activation, so attribution
patching is exact there (100%) and the construction's edit predictions are 75–77%.

Two mistakes on the way: the first version translated an activation edit into a change of the variables with the
linear probe, which amplifies low-variance directions and made the construction worse than "no change" (70%); reading
the edit off the named subspace (pseudo-inverse of the alignment map) is the faithful version of the construction's
claim that the rest of the activation does not matter.

**Conclusion.** Honest status of Level 3: the construction beats the behaviour-only surrogate, the statistics
regressor and the prior-only reader. It beats attribution patching only where the path to the output is nonlinear and
the intervention is on its variables (the embedding stage). On arbitrary subspace interventions attribution patching
wins clearly, and it is exact at every site after the MLP. The construction rarely names the exact new decision when
an arbitrary subspace edit changes it (14–18%).

**Changed as a result.** The judge reports attribution patching beside every intervention test.

## 2026-11-13 19:04. E8: the frozen constructor (v1, commit `391998c0`) on held-out networks and controls

**Why.** Level 2 of the bar: the same constructor, unchanged, on networks it was not developed on; and the controls
on mod-add again, this time on a frozen judge.

**Setup.** Eight blinded runs started together, 80 steps each, reader DeepSeek V4.1 Flash, effort high:
`modadd_p113` (replicate A), `modmul_p113`, `tracr_reverse`, `tracr_first_match`, `tracr_count_greater`, and
`modadd_p113` with shuffled, untrained and permuted weights. Development networks were the Boolean nets,
`modadd_p113` and `tracr_hist`; the other four were never run before this batch. Run folders:
`lab/constructions/<target>/20261113-1904*`. Entry updated as runs finish (status at 19:40 below).

**What happened** (all eight runs finished; 40 minutes for the longest; $0.03 to $0.39 each).

| Network | Held out? | Result | Steps | What the reader found |
|---|---|---|---|---|
| `tracr_reverse` (4 layers) | yes | **VERIFIED AND COMPLETE**, 9 of 9 stages | 9 | One token code per position; layers 0–2 add only constants on this input set; layer 3's attention has a fixed pattern (position p attends to position 4-p) and copies the token code; the output head reads it. Interchange and partial tests 100%. |
| `tracr_first_match` | yes | **VERIFIED AND COMPLETE**, 4 of 4 | 23 | Attention copies the first token's code to every position; the MLP compares it with the position's own token (see the run's README). |
| `tracr_count_greater` | yes | **VERIFIED AND COMPLETE**, 4 of 4 | 47 | Attention weight on BOS encodes the count of greater tokens; the MLP converts it (see the run's README). |
| `modmul_p113` (Mystery C) | yes | **VERIFIED AND COMPLETE**, 4 of 4, on submission 14 | 76 | Embedding: cos/sin of 2πm·dlog₃(t)/112 at m = 4, 28, 31, 41. Attention is nearly uniform, so `attn_out`/`resid_mid` hold an additive code h(i) + h(j) (17 dims, including the doubled frequencies 8, 56, 30, 50 and one difference clock). MLP: the product's clock by angle addition on the sum, cos(a+b) = (C² − S²)/2 − C₂ₘ/2, which is why the doubled frequencies are in the embedding. Readout from the 8-dim product clock. Behaviour match 97.3% (the misses are rows with token 0, which has no discrete log). |
| `modadd_p113` replicate A | no | 3 of 4 stages (embedding at `embed.1`, MLP neurons, readout); attention not verified | 80 | Same mechanism as E3. 0 stages until submission 6 (step 44): its per-frequency variables scored 38–47% on partial tests until the amplitudes were measured. |
| `modadd_p113` permuted | control | 3 of 4 stages | 80 | The same construction as on the original weights, as it should be: permuting units does not change the function. |
| `modadd_p113` shuffled | control | **0 stages, not verified** | 79 | The shuffled network's output is nearly constant (a constant output matches 96.6% of decisions). The reader reported "an additive per-token score plus a thin ReLU remainder ... not a compact construct" and named no mechanism. |
| `modadd_p113` untrained | control | **not verified** (behaviour 94.8%); 1 stage passes | 80 | The one passing stage is a 112-dimensional lookup of each token at the embedding, which is what a random embedding is (69 principal components are needed there, against 7 on the trained network). The reader wrote that it "could not compress" the rest. Construction length 7,176 characters, against 1,576 for the trained network's. |

Mod-mul run in more detail (`lab/constructions/modmul_p113/20261113-190435-ec84`): the task at step 3; the discrete-log
frequencies at step 9; embedding verified at submission 2; two crashed submissions (a shape bug); attention and
readout verified at submissions 10–12; complete at submission 14. A second check of its claims: the three doubled
frequencies 30, 56 and 50 are the 5th, 6th and 7th strongest frequencies of `W_E` in discrete-log order (4.1%, 3.5%,
2.4% of the power), which fits the reader's explanation of why they are there.

**Independent check of the mod-mul finding.** I computed the Fourier power of `W_E` with the 112 non-zero tokens ordered
by discrete logarithm base 3: the top frequencies are 4, 41, 28, 31 (75% of the power; the next is 4%), and `W_U`
gives the same four. In plain token order the embedding has no such structure (top five frequencies hold 9.6%).
So the reader's blinded reading of this held-out network is correct, and it is not the mod-add recipe replayed: the
structure only appears after reordering the tokens by discrete log, which the reader had to find.

**Notes.**
- `tracr_reverse` is easier than its name suggests: the networks are compiled for one input length, so the program's
  length computation is constant here and the judge ignores constant sites. The run tests routing by attention.
- Mod-add under judge v3 is harder for the reader than under v1 (E3), because the frozen prompt advises one variable
  per part, and single-frequency swaps are knife-edge cases: the hand-written oracle split by frequency scores 51–90%
  on them, the reader's 38–47% with rougher amplitudes. A lumped 10-dimensional variable faces the easier coordinate
  edit (67–76% in E3). "Splitting must never raise the bar" is therefore still not true in practice.

**Conclusion.** Level 2 holds on this batch: with nothing changed, the constructor produced complete, intervention-
verified constructions of four networks it was not developed on, including a trained network (mod-mul) whose
mechanism differs from the development network's. The weight controls behave: shuffled and untrained weights give no
verified construction and no claimed mechanism, permuted weights give the same construction. The caveats: one run per
held-out network so far; the compiled networks are small and have fixed input length; mod-add itself is still at 3 of
4 stages.

**Planned change after this batch (applied in E10).** Judge v3.1: at a site with several
variables, the off-manifold requirement is met if every single-variable swap passes OR the coordinate edit of
everything named at the site passes. These are two protocols for the same question, so a split construction can
never score worse than the same content lumped. The change only relaxes; constructions that pass v3 still pass.

## 2026-11-13 20:05. E9: held-out interventions on the compiled-network constructions

**Why.** E7 measured Level 3 on mod-add only. The same benchmark on the four complete constructions shows whether the
picture holds on networks of a different kind.

**Setup.** `lab/predict.py`, default settings (40 interventions per site, removals and patches of random, unit and
principal-component subspaces; half scored), on the delivered constructions of `tracr_hist`, `tracr_first_match`,
`tracr_reverse` and `tracr_count_greater`. Results are saved as `predict.json` in each run folder and shown on the
constructor page. A decision counts as right only if every output position is right.

**What happened** (decision accuracy over all sites; in brackets, over the cases where the network's decision changed).

| Network | Construction | No change | Statistics + regressor | Attribution patching |
|---|---|---|---|---|
| `tracr_reverse` | 93.5% (74.6%) | 75.0% (0%) | 65.0% | 94.1% (76.3%) |
| `tracr_first_match` | 84.9% (30.8%) | 79.0% (0%) | 75.5% | 93.7% (79.1%) |
| `tracr_count_greater` | 45.6% (21.0%) | 32.0% (0%) | 23.6% | 49.2% (25.3%) |
| `tracr_hist` | 36.4% (5.5%) | 39.8% (0%) | 23.9% | 59.6% (32.9%) |
| `modmul_p113` (added 20:50) | 74.1% (28.4%) | 77.3% (0%) | 72.5% | 90.3% (59.9%) |

Mod-mul by site (construction / attribution patching / no change): `embed.0` 76.4 / 76.5 / 67.2, `embed.1`
82.6 / 84.3 / 79.2, `attn_out` 50.9 / 85.4 / 80.1, `resid_mid` 38.7 / 80.3 / 63.6, `mlp_post` 70.3 / 100 / 70.5,
`mlp_out` 81.9 / 100 / 75.2, `resid_post` 90.0 / 100 / 85.1. The construction is below "no change" overall because of
the two attention-stage sites: its model squares the additive code there, so an arbitrary edit of the code is
amplified in the prediction but not in the network.

**Conclusion.** Same shape as on mod-add. The construction beats the behaviour-only surrogate and the statistics
regressor on three of four networks (on `tracr_hist` it is below "no change"), and attribution patching is ahead on
all four, narrowly on `tracr_reverse` and `tracr_count_greater`. A construction's alignment describes the states the
network actually visits; arbitrary subspace edits push compiled networks into states the construction says nothing
about, while attribution patching reads the network's own local slope. Level 3 as the bar states it ("beats
attribution patching") is NOT met on arbitrary interventions. It is met on interventions on the construction's own
variables through nonlinear stages (E7).

**Idea not yet tried.** Give the construction's alignment a causal read map (fit how downstream variables respond to
small perturbations at a site, once, on the fit inputs) instead of the pseudo-inverse of the write map. That would use
the network at alignment time, not at prediction time.

## 2026-11-13 20:40. E10: judge v3.1 (either off-manifold protocol is enough) and a second batch

**Why.** E6 and E8 showed that a construction split into one variable per part faces a harder off-manifold test than
the same content kept as one variable (single-frequency swaps on mod-add: 51–90% for the oracle, against 67–76% for
the coordinate edit of the lumped variable). The reader's granularity should not decide the verdict.

**Change.** At every site the judge now runs both protocols: partial (each variable copied alone; needs several
variables) and edit (a random half of the coordinates of everything named at the site). The off-manifold requirement
is met if all partial tests pass OR the edit passes. Nothing else changed. The prompt's description of the tests
was updated to say the same. This can only relax the verdict.

**Checks after the change.**
- Calibration on mod-add: oracle lumped 3 stages, oracle split by frequency 3 stages, lookup table 0, wrong
  frequencies 0. Compiled oracle unchanged.
- Every delivered construction was re-judged (`report.json`/`report.txt` in each run folder now come from v3.1):
  no verdict changed (mod-add 3 of 4 in three runs; mod-mul and the four compiled networks complete; shuffled 0;
  untrained not verified; prior-only 0).

**Second batch, on the constructor frozen at this commit** (reader, prompt and judge unchanged from here): mod-add
replicates B and C, mod-mul replicate B, compiled replicates (`tracr_first_match`, `tracr_count_greater`), and
prior-only controls (mod-add twice, mod-mul once). Results are added below when the runs end.

## 2026-11-13 21:05. E11: a game policy with a real input set (MIT's hand-written Breakout network)

**Why.** The bar asks for MIT's game policies, blinded. The four PPO policies in the lab (MIT's experiment 1) cannot be
judged: MIT released the weights and prompts but not their own 10 x 10 game environments, so there are no input
states. MIT's experiment 5 offers a way in: a 600-32-32-6 tanh policy for **MinAtar** Breakout whose every weight
was written by GPT-6 Astra in one reply. MinAtar is a public package, so real game states can be generated; the
network's design is known from the reply; and a reader cannot have memorised it (it was written in November 2026).

**Setup.** `lab/targets/build_minatar.py`: loads `exp5_write_from_scratch/networks/breakout/hand.npz` from the MIT
logs, builds the 600-number observation exactly as MIT's prompt defines it, plays MinAtar 1.0.15 Breakout with
sampled actions and sticky actions 0.1 (MIT's scoring rule), and saves 6,000 distinct visited states as the input set.

**What happened.** The policy scores 0.069 points per step here; MIT reports 517.4 points over 7,417 steps, 0.070 per
step. So the observation is built correctly. 11,198 distinct states were seen in 12 episodes; 6,000 are kept. On
them the network chooses no-op 2,827 times, left 1,620, right 1,553, and never up, down or fire. The new target is
`lab/models/astra_breakout` ("Hand-written game policy"), with a neutral input description for blinded runs (it says
only that the inputs are 600 numbers that are 0 or 1 and that `X` is a sample of the inputs met in use).

**Not done.** MIT's experiment-1 PPO policies still have no input set. Writing approximate versions of MIT's own
environments from the prompt text would put the networks off their training distribution; not attempted.

**Next.** A blinded constructor run on `astra_breakout` (held out: it was never used in development).
A small, function-preserving change was made to `nets.domain_inputs` while batch 2 was in flight: input sets stored in
a file are cast to 64-bit on load. No in-flight run uses a file-based input set.

**E10 and E11, status after a second session interruption (2026-11-14 00:40).** The interruption killed every process
at about 20:10. Finished before it: `tracr_first_match` replicate B (complete, 22 steps), `tracr_count_greater`
replicate B (complete, 33 steps), and two prior-only controls on mod-add (0 of 4 stages each). Killed part-way and
marked "interrupted": mod-add replicates B and C (26 and 30 steps, 0 stages at that point), mod-mul replicate B (34
steps), the mod-mul prior-only control, and the first `astra_breakout` run (14 steps). The `modsub_p113` training
job was also killed at epoch 11,750 of 25,000 (test accuracy 23%, not yet generalised); its weights are only saved
at the end, so nothing was kept, and it is not being retrained in this session (about 1.5 hours of CPU).
All five interrupted runs were relaunched at 00:40 on the same frozen constructor, titled "(rerun)".

## 2026-11-14 00:40. E12: the game policy, blinded (held out): verified and complete, and a specific question names the game

**Why.** E11 made a game policy judgeable. This is the bar's "game policies, blinded" item, on a network never used
in development, and a test of the owner's interface point: ask for the mechanism first, then ask something specific.

**Setup.** `astra_breakout`, blinded, constructor frozen at `b8a40aaa`, 80-step budget. The reader was told only the
architecture and that the inputs are 600 numbers that are 0 or 1. Run `lab/constructions/astra_breakout/20261114-00*`
(the first attempt, `20261113-200650-1904`, was killed by the interruption at step 14).

**What happened.** VERIFIED AND COMPLETE at submission 5, step 32 (10 minutes, $0.13). Behaviour match 100%, output
R² 1.000. Both hidden layers verified: substitution 100%; removing the named subspace drops decisions to the
mean-ablation level (46.7%); interchange 100%; every partial test 100% (source-output control 36–41%); edits
99.7–100%. Attribution patching scores 0% on the first hidden layer's interventions (the second layer saturates) and
100% on the second (the output is linear in it).

The construction, in the reader's words: "a gated three-way comparison". Only 6 first-layer units are live. Four are
small linear forms: a triangular profile over the cells of one channel plus a ramp over the bottom row of another.
Two saturate to ±1 and act as selectors. The second layer has 8 live threshold units in 4 pairs; the two selectors
arm exactly one pair, which reports whether its linear form is below -0.015 or above +0.015. Output 1 wins in the
first case, output 3 in the second, output 0 otherwise; outputs 2, 4 and 5 are constant at -100.

**Against the known design.** The model that wrote the network described it as: "the first layer computes four
landing-position errors and two direction indicators ... the second layer gates left/right decisions, choosing no-op
when positioned correctly." That is the same structure, unit for unit: four error forms, two direction selectors, a
gate, no-op in the dead band. The reader recovered it from the weights without knowing it was a game.

**The specific question.** Blinded, the reader described the mechanism and did not say "Breakout": it had no reason
to look for a game. Then `lab/ask.py` was given: "The inputs are a 10 x 10 grid with 6 channels (index = ...) and the
6 outputs are actions. Which game is this network playing, what do outputs 1 and 3 do, and what does each of your
variables mean in the game?" After checking the input layout with code, it answered: Breakout (confidence 97);
output 1 = left, output 3 = right (confidence 80), output 0 = stay; the four linear forms are "predicted ball landing
column minus paddle column" for four ball-approach cases; the selectors are the ball's direction and level. All
correct. Note that the question itself supplied the grid layout and the fact that outputs are actions. (A first
attempt returned an empty answer because the reader used every step on checks; `ask.py` now ends with a forced
answer turn.)

**Conclusion.** The owner's observation from `main` holds here: the construction is the reading; naming is a second,
specific question, and it needs the input semantics. The constructor gives the first, `ask.py` the second.

## 2026-11-14 01:35. E10, results of the second batch (constructor frozen at `b8a40aaa`, judge v3.1)

| Network | Run | Result | Steps |
|---|---|---|---|
| `tracr_first_match` replicate B | `20261113-200059-d63d` | complete, 4 of 4 | 22 |
| `tracr_count_greater` replicate B | `20261113-200059-cb04` | complete, 4 of 4 | 33 |
| `modmul_p113` replicate B | `20261114-003532-fe44` | 3 of 4: embedding, MLP neurons, readout verified; attention not named | 80 |
| `modadd_p113` replicate C | `20261114-003532-0e79` | 3 of 4: embedding, MLP neurons, readout; attention not named | 80 |
| `modadd_p113` replicate B | `20261114-003532-8fe7` | 3 of 4: embedding, MLP neurons, readout; attention not named (finished 02:05) | 80 |
| `astra_breakout` | E12 | complete, 2 of 2 | 33 |
| mod-add prior-only B, C | `20261113-200059-4f94`, `-9cb3` | 0 of 4 each | 2, 4 |
| mod-mul prior-only | `20261114-003532-*` (no weights) | 0 of 4 | 4 |

**Conclusions.**
- Mod-add is stable at 3 of 4 stages across five blinded runs (E3, the E4 replicate, A, B, C), always the
  same three: embedding, MLP neurons, readout, with the frequencies {8, 11, 22, 23, 25}. No run verified attention.
- Mod-mul: one run complete (E8), one run 3 of 4 with the attention stage left unnamed. So "complete" on mod-mul is
  not reliable from one run to the next; the discrete-log embedding, the MLP and the readout were verified both times.
- The compiled networks completed in every run (two runs each for first-match and count-greater).
- Prior-only fails on both trained networks every time (4 runs), so naming the task does not supply the mechanism.
- Step budgets matter: both 3-of-4 runs used all 80 steps and reached their third stage on a late submission.

---

# Session 3 (2026-11-14): from toy networks to a real language model

All experiments below are on GPT-2 small (124M weights) through `lab/lm.py`, on a 2-CPU machine with no GPU.

## 2026-11-14 04:55. E13, a first candidate target: the ordinal suffix (rejected)

**Why.** A behaviour of a real model with crisp, low-cardinality structure: after a number, GPT-2 small continues
with "st", "nd", "rd" or "th". **What.** 505 single-token numbers x 4 templates (`gpt2_ordinal`).
**Result.** The model follows the rule on 98.6% of prompts (errors are specific numbers: 213, 223, 247, 312, 313, ...).
But replacing the number's residual stream by the mean of its suffix class (4 vectors) keeps 98.5% of answers at
*every* depth, including depth 0, the token embedding; interchange of "units digit + teen flag" works at 85-93% at
every depth. Only MLP 0 matters when single components are mean-ablated (81% kept; every other component 98-100%).
**Conclusion.** The suffix class is a feature of the number's embedding; nothing is computed along the way. A
construction "the class is linearly present everywhere" is true and passes, so a prior-only reader would pass too.
Not a discovery. **Changed:** require a target whose answer depends on a *combination* of tokens.

## 2026-11-14 05:05. E14, arithmetic progressions (rejected: no capability)

"7, 9, 11, 13," -> 15? Top-1 accuracy by step: 1: 98-100%; 2: 0-4%; 3: 0-5%; 5: 1-12%; 10: 3-12%. With step 2 or 3
the model answers last + 1 in 80-99% of cases. GPT-2 small does not continue progressions with a step above 1.

## 2026-11-14 05:10. E15, a battery of two-variable behaviours

| Behaviour | Result |
|---|---|
| Counting down ("56, 55, 54, 53," -> 52), comma-separated, 4 or 5 numbers | 89% / 96% top-1 without BOS; **100% for last numbers 20-119 with BOS and a prefix**, both directions |
| Year rollover ("December 1999, January" -> 2000; other months keep the year) | 100% / 93% |
| is / are / was / were by subject number x tense cue | 81-100% per cell |
| Correlatives (either-or, neither-nor, both-and, between-and) | 81-100% |
| Reflexives (himself / herself / themselves / itself) | 67-100% |

**Chosen: counting down.** It needs two things combined (the direction, from several tokens; the last number), the
behaviour is perfect, and published work covers only increasing sequences (successor heads: Gould et al. 2023;
"increasing sequences" circuit: Lan & Barez 2024). Target `gpt2_countdown`: 800 prompts (last number 20-119, both
directions, four neutral prefixes), output = the logits of the 362 number tokens " 0".." 361".

## 2026-11-14 05:20. E16, what a code for a number must look like to pass the judge

At `resid9@end` (which, by substitution, holds the last number n4 and the direction):

| Code for n4 (plus a 1-dim direction) | Dims | Substitute | Interchange | Partial n4 |
|---|---|---|---|---|
| top principal components of the per-number means: 7 / 10 / 14 / 20 | 8-21 | 50% / 89% / 99% / 100% | 18% / 47% / 81% / 95% | 25% / 55% / 79% / 93% |
| units one-hot + tens one-hot | 19 | 89% | 65% | 66% |
| Fourier over period 100, harmonics {1,2,5,10,20,50} | 13 | 84% | 35% | 33% |
| ... harmonics {1..5,10,20,30,40,50} | 21 | 100% | 81% | 80% |
| ... harmonics {1..10,20,30,40,50} | 29 | 100% | **91%** | 88% |
| one-hot identity | 100 | 100% | 96% | 95% |

The direction variable passes its partial test at 98-99% with every code. **Conclusions.** (1) The direction is a
clean one-dimensional variable at the end position by depth 9. (2) The number is held in a code that a Fourier
basis over period 100 describes: 28 dimensions reach the interchange bar. (3) The old size limit (twice the
principal components that keep 90% of answers: 14 here) cannot be met by *any* linear code that passes interchange.
**Changed:** for LM targets the limit is measured at 99% of answers, and one-hot identities of single quantities
(at least 6 prompts per value) are exempt. A compact code is left as the stricter, second-pass goal.

## 2026-11-14 05:45. E17, calibrating the LM judge with a hand-written guess

`lab/constructions/_oracle/gpt2_countdown_first_guess.py`: identities of n3 and n4 at their positions (depths 0, 3);
n4 and the direction at the n4 position (depth 6); n4 and the direction at the end position (depth 9); the answer's
identity (depth 12); direction = sign(n4 - n3).

| Cut | Substitute | Interchange | Partial tests | Verdict |
|---|---|---|---|---|
| cut0 (n3, n4) | 95.5% | 70.7% | n3: 0%, n4: 40% | fails |
| cut3 (n3, n4) | 81.2% | 68.7% | n3: 0% | fails |
| cut6 (n4, dir at the n4 position) | 97.2% | 32.2% | dir: the output does not depend on it (1% changed) | fails |
| cut9 (n4, dir at the end) | 100% | 95.9% | n4 95.3%, dir 99.0% | **verified** |
| cut12 (answer) | 98.0% | 99.7% | | **verified** |

**Conclusions.** The judge separates what is right from what is guessed: 2 of 5 stages. What my guess gets wrong
is the interesting part: (a) at depth 6 the n4 position is sufficient alone (97%), so the direction information is
there, but not as a linear "direction" variable; (b) the model's direction is not sign(n4 - n3) when n3 is swapped
for an arbitrary number (0% of the changed cases predicted). The middle of the network is the open question the
constructor has to answer.

## 2026-11-14 05:15-06:10. Smoke tests of the LM constructor (live)

A 10-step blinded run: the reader found the behaviour (n4 + (n4 - n3)) in 2 steps, scanned depth x position by
mean-ablation in step 3 (n4 matters at depths 0-6, the end position from depth 9), and submitted a 1-dimensional
"next number" variable at depth 12, which failed as it should. Cost $0.017. The pipeline (session, hooks, judge,
report) works end to end. Judge time: 35 s for one cut, 2.5 min for five cuts with identity variables.

## 2026-11-14 11:45-12:40. E18, first real runs after the interruption; two operational failures and their fixes

Relaunched after a six-hour interruption (the 05:37 runs had died at step 4 and step 0): blinded run A and
prior-only control 1 on `gpt2_countdown`, blinded run A on the new target `gpt2_be_verb`
(is / are / was / were; 720 prompts, the model follows the rule on 100%).

- **Judges killed for memory.** Two LM runs plus a hand-started judge at once: the kernel killed judges (about 2 GB
  each; the machine's limit is 8 GB). The prior-only control's only submission was lost this way. **Fix:** judges
  take a machine-wide lock (`/tmp/helix_judge.lock`) and a judge that dies silently is retried once; the loader
  frees Hugging Face's copy of the weights. **Rule for this machine: one LM constructor run at a time.**
- **I broke the engine for ten minutes** by editing `lab/lm.py` (a too-wide key filter) while runs were using it; four
  submissions (countdown 4-5, be-verb 2-3) got a crash instead of a report. **Rule: test every edit of
  `lm.py` / `lmjudge.py` with one judge call before leaving it on disk while runs are in flight.**
- Speed with three processes on two CPUs: a depth-by-position scan took 220-320 s. Session timeout raised to 600 s;
  residual sites are now read from the cache without a forward pass.
- State at 12:40: countdown run A 1 of 5 stages after 6 submissions; be-verb run A 2 of 5 after 4 (then paused with a
  STOP file to give the countdown run the machine; resume it with `--resume 20261114-114450-62b2`).

## 2026-11-14 13:10-13:55. E19, what blocks the countdown reader; a faster judge; a second model family

- **Run A after 56 steps and 10 submissions: 1 of 5 stages** (the answer's identity at depth 12). It works bottom-up
  and is stuck on the partial tests of the embedding cut: what the model answers when ONE number is swapped.
- **Is that a judge artefact? No.** The judge's subspace swap of a number's identity at `resid0` gives the same answer
  as swapping the token in the prompt in 100% of 200 pairs (n1, n3, n4). What the model does after a swap of n3 is
  not "n4 + sign(n4 - n3')" (22%): in 43% of cases the answer is 5 or more away from n4, e.g. "97, 96, 28, 94," -> 24,
  "38, 39, 76, 41," -> 77. It looks like "one step beyond the extreme number, in the run's direction" (32% exact for
  my crude version). So the early stages need a real model of how GPT-2 reads a number list; this is the new,
  checkable content a complete construction would carry. Left to the reader.
- **Judge time** was 5-7 minutes for a nine-site submission. Now: the two costly controls (attribution patching,
  random subspace) run on the interchange test only, the principal-component count is cached, 300 pairs instead
  of 400. A one-cut check: 28 s with another process on the machine.
- **Pythia (GPT-NeoX) in `lab/lm.py`**: rotary positions, parallel residual, untied unembedding. Final logits agree
  with Hugging Face to 0.002 in float32 (Hugging Face's default half-precision load differs from both by 0.7). New
  target `pythia70m_be_verb`: the rule holds on 94.9% of 649 prompts. So the tool is not GPT-2-only.
