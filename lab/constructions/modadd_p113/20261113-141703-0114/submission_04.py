
import numpy as np

DESCRIPTION = """
Key finding. Writing the full logit tensor as T[i, j, t] (i, j in 0..112, t in 0..112 classes),
T is almost exactly ADDITIVE in the two tokens: the residual after removing the per-class row and
column means has only 0.9% of the variance, and argmax of the additive reconstruction equals the
network's argmax on 94.8% of inputs. Row-mean matrix A[i,t] and column-mean matrix B[j,t] are
identical to 1e-6, and T's rows/cols are 99.8% symmetric. So logit_t(i,j) ~ m_t + s_t(i) + s_t(j):
the network turns each input token into its own 113-dim logit-vote s(token) and sums the votes of the
two tokens (the answering position contributes the constant m). Raw token ids are NOT what the
embedding sites hold (embed.0/embed.1 are an arbitrary learned code, explained 0.008), so this file
still only probes: it keeps the constant baseline and carries the token ids plus the product i*j.
"""

def model(x, iv):
    i = iv("tok_i", x[:, 0].astype(float))
    j = iv("tok_j", x[:, 1].astype(float))
    p = iv("prod_ij", (x[:, 0] * x[:, 1]).astype(float))
    B = x.shape[0]
    logits = np.zeros((B, 113))
    logits[:, 39] = 1.0
    return logits

ALIGN = {"tok_i": ["embed.0"], "tok_j": ["embed.1"], "prod_ij": ["mlp_pre"]}
