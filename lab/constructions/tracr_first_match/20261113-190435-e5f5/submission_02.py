
import numpy as np

DESCRIPTION = ("The sequence is [BOS=0, t1..t5] with t_i in {1,2,3,5}. Attention in layer 0 is a fixed "
               "pattern: query at position 0 attends to key 0, and every query at positions 1..5 attends to "
               "key 1 only, so the attention output is the same constant vector at positions 1..5 (the value "
               "of token t1). Hence every position p>=1 carries the pair (t_p, t1) and the readout at position "
               "p is the comparison t_p == t1: class 1 if equal, class 0 otherwise (logit margin +-1). "
               "Modelled so far: the embeddings (token one-hots per position) and the attention stage "
               "(variable v1 = one-hot of t1, which linearly determines attn0.out).")

def model(x, iv):
    B = x.shape[0]
    ar = np.arange(B)
    tok = []
    for p in range(6):
        v = np.zeros((B, 6))
        v[ar, x[:, p]] = 1.0
        tok.append(iv("tok%d" % p, v))
    v1 = iv("v1", tok[1])
    out = np.zeros((B, 10))
    for p in range(1, 6):
        eq = (tok[p] * v1).sum(1)          # 1 if t_p == t1
        d = 2.0 * eq - 1.0                 # +-1 margin
        out[:, 2 * (p - 1)] = 0.0
        out[:, 2 * (p - 1) + 1] = d
    return out

ALIGN = {"tok0": ["embed"], "tok1": ["embed", "attn0.out"], "tok2": ["embed"],
         "tok3": ["embed"], "tok4": ["embed"], "tok5": ["embed"],
         "v1": ["attn0.out", "resid0.mid", "mlp0.pre"]}
