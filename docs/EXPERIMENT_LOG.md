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
