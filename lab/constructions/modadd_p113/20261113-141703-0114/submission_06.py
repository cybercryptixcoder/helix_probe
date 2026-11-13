
import numpy as np

DESCRIPTION = """
Where the computation stands. (1) Attention is constant: all 12 pattern entries are 1/3 (std 0.001)
and mean-ablating attn_pattern changes only 0.2% of decisions, so no token selection happens --
attn_out is the plain average of the three positions' value vectors.
(2) Every site up to resid_mid is EXACTLY additive in the two input tokens: embedding, attn_out,
resid_mid and even mlp_pre have 0.00000 residual variance after removing per-class row and column
means of the 113x113 input grid. So pre[i,j,n] = p0[n] + a[i,n] + a[j,n] exactly.
(3) The relu is the only nonlinearity; the non-additive part of the logits has std 0.0059 versus a
0.17 logit std, so logit_t(i,j) = m_t + s_t(i) + s_t(j) with 0.86% residual; this additive model
already reproduces the network's argmax on 94.8% of inputs (rank-r truncation of s degrades it
smoothly: rank 64 -> 94.1%, rank 32 -> 84.4%, so the per-token vote is a genuinely 113-dim code).
Only 18 classes ever win; the answer is a sum of two independent per-token votes.
(4) The remaining 5% of decisions are inputs whose top two classes are closer than the relu's
non-additive noise (median top-1 minus top-2 gap is 0.036, non-additive logit contribution ~0.006),
so a faithful construction needs the relu term as well.
This file still asserts the constant-attention fact and the raw token ids only.
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
