
DESCRIPTION = """
First-pass construction (partial). Findings so far:
- Inputs are [i, j, 113] with i,j in 0..112; the last position (token 113, position 2) is the readout position.
- The 4-head causal attention at the last position is essentially UNIFORM: every one of the 12
  attention weights sits within ~0.001 of 1/3, so attention is a nearly fixed average of the three
  positions (no real pattern computation).
- The network's output is overwhelmingly dominated by a single class, token 97: 12361 of 12769
  inputs (96.8%) have argmax = 97. The remaining 408 inputs are scattered over classes
  14, 85, 47, 98, 105 and look like near-tie flips, i.e. the logits are all tiny (|logit| < 1)
  and close together, so the decision is a fine-grained comparison of a weak signal.
This submission only encodes the attention stage (uniform weights) plus the majority-class output
baseline; the embedding / MLP / readout stages are not yet explained.
"""
import numpy as np

def model(x, iv):
    B = x.shape[0]
    pat = iv("pat", np.full((B, 12), 1.0 / 3.0))
    logits = np.zeros((B, 113))
    logits[:, 97] = 1.0
    return logits

ALIGN = {"pat": ["attn_pattern"]}
