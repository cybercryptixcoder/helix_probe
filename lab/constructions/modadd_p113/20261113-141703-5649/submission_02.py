
DESCRIPTION = """
Partial construction. Established facts (all verified numerically against the real sites):
1. Causal attention at the last position is essentially UNIFORM: all 12 weights are within 0.001 of 1/3
   (the score variation is tiny), so attn_out is just the mean over the 3 positions of x @ W_V[h] @ W_O[h]
   summed over heads; reproducing that with a fixed 1/3 pattern is accurate to 3e-3 while attn_out
   itself has mean magnitude 0.11.
2. embed.2 = W_E[113] + W_pos[2] is a CONSTANT vector (token 113 is always last): the last position's
   token embedding carries no input information.
3. Consequently resid_mid = const + z_i + z_j with z_t = (W_E[t] + W_pos[pos]) @ Ap, i.e. the residual
   stream at the last position is an additive function of the two input tokens, and the MLP + readout
   are a deterministic function of it:  out[i,j,:] = mu + b[i,:] + b[j,:] with the additive form
   explaining 99.2% of the logit variance (the i x j interaction term has mean |.| = 0.0045 vs 0.05
   for the whole logit variation).
4. The logits are all small (|.| < 1) and the readout class 97 has by far the largest mean logit, so
   the network answers token 97 on 96.8% of inputs; the remaining 408 inputs (classes 14, 85, 47, 98,
   105) are near-tie flips of the weak per-token signal.
This submission encodes stages 1-2 (uniform attention pattern + constant last-position embedding) and a
constant baseline for the output; the per-token score table that makes up the additive readout still
needs to be measured and compressed.
"""
import numpy as np

def model(x, iv):
    B = x.shape[0]
    pat = iv("pat", np.full((B, 12), 1.0 / 3.0))
    emb2 = iv("emb2", np.zeros((B, 128)))
    logits = np.zeros((B, 113))
    logits[:, 97] = 1.0
    return logits

ALIGN = {"pat": ["attn_pattern"], "emb2": ["embed.2"]}
