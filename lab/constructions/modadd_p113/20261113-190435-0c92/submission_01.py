
import numpy as np, math
DESCRIPTION = """Rough first pass. The network computes (i+j) mod 113 where the sequence is [i, j, 113].
Tokens are embedded with Fourier features of the token index (attention copies j into the last
position, MLP turns cos/sin of i and j into cos/sin of i+j), and the readout writes logits that
are cos(2*pi*(i+j-k)/113), whose argmax is (i+j) mod 113."""
FR = [8, 11, 22, 23, 25]
N = 113.0

def feats(t):
    cols = []
    for k in FR:
        a = 2*math.pi*k*t/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, 1)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ci = iv("ci", feats(i))
    cj = iv("cj", feats(j))
    s = i + j
    tot = iv("tot", feats(s))
    pre = iv("pre", ci + cj)
    logits = np.stack([np.cos(2*math.pi*(s - k)/N) for k in range(113)], 1)
    return logits

ALIGN = {"ci": ["embed.0"], "cj": ["embed.1"], "pre": ["resid_mid"], "tot": ["mlp_post", "resid_post"]}
