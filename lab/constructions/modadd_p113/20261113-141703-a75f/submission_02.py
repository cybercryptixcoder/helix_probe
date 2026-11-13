
import numpy as np, math
DESCRIPTION = ("Task: s=(i+j) mod 113 from tokens [i, j, 113]. Token embeddings are Fourier codes: W_E[t] is a sum of "
 "cos/sin(2pi k t/113) with k in {8,11,23,25} plus harmonics (16,22,46,50). The last position's query (token 113) gives, per head, "
 "a score for pos0 that depends only on i and the same function of j for pos1, so attention weights are softmax of (f_h(i), f_h(j), const). "
 "Attention output keeps single-side Fourier content plus products, giving cos/sin of k(i+j); the MLP converts this into clean "
 "cos/sin(2pi k (i+j)/113) terms, and the readout scores class c by the sum over k of cos(2pi k (c-s)/113).")
P = 113.0
FR = [0.0, 8.0, 11.0, 16.0, 22.0, 23.0, 25.0, 46.0, 50.0]
MAIN = [8.0, 11.0, 23.0, 25.0]

def feats(t):
    cols = []
    for k in FR:
        if k == 0.0:
            cols.append(np.ones_like(t))
        else:
            cols.append(np.cos(2*np.pi*k*t/P))
            cols.append(np.sin(2*np.pi*k*t/P))
    return np.stack(cols, axis=1)

def model(x, iv):
    i = np.asarray(x[:, 0], dtype=float)
    j = np.asarray(x[:, 1], dtype=float)
    fi = iv("freq_i", feats(i))
    fj = iv("freq_j", feats(j))
    ci = fi[:, 1::2]; si = fi[:, 2::2]
    cj = fj[:, 1::2]; sj = fj[:, 2::2]
    cs = iv("cos_sum", ci*cj - si*sj)
    ss = iv("sin_sum", ci*sj + si*cj)
    pre_feats = iv("pre_sum", np.concatenate([cs, ss], axis=1))
    mm = [np.where(np.array(FR)[1:] == k)[0][0] for k in MAIN]
    csm = iv("cos_sum_main", cs[:, mm])
    ssm = iv("sin_sum_main", ss[:, mm])
    c = np.arange(113)[None, :]
    ang = np.stack([2*np.pi*k*c/P for k in MAIN], axis=1)   # [1,4,113]
    logits = (csm[:, :, None]*np.cos(ang) + ssm[:, :, None]*np.sin(ang)).sum(axis=1)
    return logits

ALIGN = {"freq_i": ["embed.0"], "freq_j": ["embed.1"], "cos_sum_main": ["mlp_out"], "sin_sum_main": ["mlp_out"],
         "cos_sum": ["resid_mid"], "sin_sum": ["resid_mid"], "pre_sum": ["mlp_pre"]}
