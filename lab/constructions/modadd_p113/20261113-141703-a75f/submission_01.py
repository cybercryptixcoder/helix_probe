
import numpy as np, math
DESCRIPTION = ("The network computes s=(i+j) mod 113 from tokens [i, j, 113]. Embeddings are Fourier codes of the token id: "
  "W_E[t] = sum_k (a_k cos(2pi k t/113) + b_k sin(2pi k t/113)) over a few frequencies k (8,11,23,25 dominate, with harmonics). "
  "Attention at the last position mixes pos0 (i) and pos1 (j) so the residual carries the sum-angle features "
  "cos/sin(2pi k (i+j)/113) (angle addition), the MLP cleans this up, and the readout scores class c by agreement of "
  "those cosines, giving argmax logit at c=(i+j) mod 113.")
P = 113.0
FR = [0.0, 8.0, 11.0, 16.0, 22.0, 23.0, 25.0, 46.0, 50.0]

def feats(t, freqs):
    cols = []
    for k in freqs:
        if k == 0.0:
            cols.append(np.ones_like(t))
        else:
            cols.append(np.cos(2*np.pi*k*t/P))
            cols.append(np.sin(2*np.pi*k*t/P))
    return np.stack(cols, axis=1)

def model(x, iv):
    i = np.asarray(x[:, 0], dtype=float)
    j = np.asarray(x[:, 1], dtype=float)
    fi = iv("freq_i", feats(i, FR))
    fj = iv("freq_j", feats(j, FR))
    # angle addition: cos(k(i+j)), sin(k(i+j))
    ci = fi[:, 1::2]; si = fi[:, 2::2]
    cj = fj[:, 1::2]; sj = fj[:, 2::2]
    cs = iv("cos_sum", ci*cj - si*sj)
    ss = iv("sin_sum", ci*sj + si*cj)
    s = (np.round(i) + np.round(j)) % 113
    c = np.arange(113)[None, :]
    main = [k for k in FR if k != 0.0]
    ang = np.stack([2*np.pi*k*(c - s[:, None])/P for k in main], axis=0)
    return np.cos(ang).sum(axis=0)

ALIGN = {"freq_i": ["embed.0"], "freq_j": ["embed.1"], "cos_sum": ["resid_mid"], "sin_sum": ["resid_mid"]}
