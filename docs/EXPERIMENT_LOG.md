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
