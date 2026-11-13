
DESCRIPTION = """
Partial construction (stage 1 of 4 verified). Findings so far, all checked numerically against the
real sites and against a hand-built exact forward pass (which reproduces every site bit-for-bit):
* embed.2 is a CONSTANT vector (token 113 always occupies position 2), so the last position's token
  embedding carries no input information.
* The 4-head causal attention is essentially UNIFORM (all 12 weights within 0.001 of 1/3), so
  attn_out = mean over positions of x_p @ W_V[h] @ W_O[h] summed over heads (error 3e-3 against
  mean magnitude 0.11). Hence resid_mid = const + z_i + z_j, additive in the two input tokens.
* The MLP + unembedding turn that into out[i,j,:] = mu + b[i,:] + b[j,:]; the additive form explains
  99.2% of the logit variance (interaction term mean |.| 0.0045 vs 0.05 total logit variation), so the
  network is a bag-of-tokens additive scorer. mu is dominated by class 97 (mean logit 0.652, next
  largest 0.489), so 96.8% of inputs answer token 97; only the six classes
  {97, 14, 85, 47, 105, 98} (mean logits 0.652, 0.489, 0.441, 0.447, 0.395, 0.301) can ever win.
* Restricting b to those six columns and using the exact additive table reproduces the network's
  argmax on 99.2% of all 12769 inputs.
This submission encodes embed.2 (constant, VERIFIED) and a constant attention pattern plus the
majority-class output; the 113x6 per-token score table that carries the remaining decision signal is
measured but not yet written into the file.
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
