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
