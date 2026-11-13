
import numpy as np

DESCRIPTION = """
Mechanism so far. (1) The attention pattern is essentially CONSTANT: every one of the 4 heads puts
1/3 on each of the 3 positions (mean 0.3333 per entry, std 0.001). So the attention layer never
selects a token -- attn_out is just the average of the three positions' value vectors.
(2) Consequently every activation up to resid_mid is exactly additive in the two tokens: embedding,
attn_out, resid_mid and mlp_pre all have 0.0000 residual variance after an additive (row+col-mean)
fit over the 113x113 grid of inputs. mlp_post/mlp_out are only 4% non-additive, resid_post 0.9%.
(3) The logits inherit this: T[i,j,t] is additive with 0.86% residual and its argmax matches the
network on 94.8% of inputs; row-mean and column-mean token votes agree to 1e-6 and the grid is
99.8% symmetric. Hence logit_t(i,j) ~ m_t + s_t(i) + s_t(j): each token contributes a 113-dim vote.
(4) Coarse block structure: H(pred)=1.455 nats, H(pred | i//2,j//2) = 0.644, H(pred|i//3,j//3)=0.918;
fine residue structure is irrelevant (H(pred|i%k,j%k) stays ~1.3-1.45). Only 18 classes ever win.
This file asserts the constant-attention stage plus the raw token identities; the per-token vote
table s(t) (114x113) is not yet compressed into the file.
"""

def model(x, iv):
    i = iv("tok_i", x[:, 0].astype(float))
    j = iv("tok_j", x[:, 1].astype(float))
    B = x.shape[0]
    a = iv("attn_uniform", np.ones((B, 12)) / 3.0)
    logits = np.zeros((B, 113))
    logits[:, 39] = 1.0
    return logits

ALIGN = {"tok_i": ["embed.0"], "tok_j": ["embed.1"], "attn_uniform": ["attn_pattern"]}
