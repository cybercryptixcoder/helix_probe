
import numpy as np
DESCRIPTION = ("Output class = (i+j) mod 113 for input [i, j, '=']. Embeddings put cos/sin of the token index "
               "at freqs 8,11,22,23,25 of 2*pi*n/113 (8 of 128 dims explain ~87% of W_E; SVD rank ~10). "
               "Attention reads positions 0 and 1 into the last position; the MLP forms cos/sin of the sum by "
               "angle addition (cos(a+b)=cos a cos b - sin a sin b) which lives in resid_post; the unembedding "
               "reads out a cosine of c - (i+j) at the same freqs, so the argmax is i+j mod 113.")
FR = [8, 11, 22, 23, 25]
def feats(n):
    n = np.asarray(n, dtype=float)
    return np.stack(sum(([np.cos(2*np.pi*k*n/113.0), np.sin(2*np.pi*k*n/113.0)] for k in FR), []), 1)
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    fi = iv("fi", feats(i)); fj = iv("fj", feats(j))
    ci, si = fi[:, 0::2], fi[:, 1::2]
    cj, sj = fj[:, 0::2], fj[:, 1::2]
    cs = ci * cj - si * sj
    ss = si * cj + ci * sj
    sfun = iv("sfun", np.concatenate([cs, ss], 1))
    c = np.arange(113)
    cs_, ss_ = sfun[:, 0::2], sfun[:, 1::2]
    logits = np.zeros((x.shape[0], 113))
    for t, k in enumerate(FR):
        w = 2*np.pi*k*c/113.0
        logits += np.outer(cs_[:, t], np.cos(w)) + np.outer(ss_[:, t], np.sin(w))
    return logits
ALIGN = {"fi": ["embed.0"], "fj": ["embed.1"], "sfun": ["resid_post"]}
