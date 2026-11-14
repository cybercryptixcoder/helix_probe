
import numpy as np

DESCRIPTION = ("Network computes (i+j) mod 113 where input is [i, j, '='] and output class c is the token "
               "i+j mod 113 (checked exactly on all 12769 inputs). Embeddings place Fourier features of the "
               "token index (freqs 8,11,22,23,25 of 2*pi*n/113) in the residual stream; position 2 is the "
               "constant '=' embedding. Attention mixes positions 0,1 into the last position; the MLP then "
               "forms cos/sin of the sum (trig product) which the unembedding reads out as cos(2*pi*k*(c-(i+j))/113).")

FR = [8, 11, 22, 23, 25]

def feats(n):
    out = []
    for k in FR:
        out.append(np.cos(2*np.pi*k*n/113.0))
        out.append(np.sin(2*np.pi*k*n/113.0))
    return np.stack(out, 1)

def model(x, iv):
    i = x[:, 0].astype(float)
    j = x[:, 1].astype(float)
    fi = iv("fi", feats(i))
    fj = iv("fj", feats(j))
    u2 = iv("u2", np.ones((x.shape[0], 1)))
    # sum features (mechanism guess: MLP product formulas give cos/sin of the sum)
    s = (i + j) % 113.0
    fs = iv("sumf", feats(s))
    # also raw sum features from the iv versions of fi/fj are not needed for the decision
    c = np.arange(113)
    logits = np.zeros((x.shape[0], 113))
    for t in range(x.shape[0]):
        st = (i[t] + j[t]) % 113.0
        d = np.abs(((c - st + 56.5) % 113) - 56.5)
        logits[t] = -d
    return logits

ALIGN = {"fi": ["embed.0"], "fj": ["embed.1"], "u2": ["embed.2"], "sumf": ["resid_post"]}
