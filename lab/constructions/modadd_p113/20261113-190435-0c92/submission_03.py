
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 for inputs [i, j, 113]. Tokens are embedded as Fourier
features of the token index at frequencies 8, 11, 22, 23, 25 (W_E is essentially rank 10, exactly
these five frequencies). Attention at the last position (softmax over positions 0,1) mixes the i and j
embeddings; the MLP turns them into products, i.e. cos/sin of f*(i+j) and f*(i-j); the readout makes
logits that depend on (i+j)-k with those frequencies, so the argmax is (i+j) mod 113. Everything below
is expressed through the variables so that replacing a variable propagates."""
FR = [8, 11, 22, 23, 25]
N = 113.0

def feats(t):
    t = np.asarray(t, dtype=float); c = []
    for k in FR:
        a = 2*math.pi*k*t/N; c += [np.cos(a), np.sin(a)]
    return np.stack(c, 1)

def rec(F):
    # token index from Fourier features: freq 8 is invertible mod 113 (8*99=1)
    ang = np.arctan2(F[:, 1], F[:, 0])
    return np.mod(np.mod(ang*N/(2*math.pi), N)*99, N)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ci = iv("ci", feats(i))
    cj = iv("cj", feats(j))
    i1 = rec(ci); j1 = rec(cj)
    mid = iv("mid", np.hstack([feats(i1), feats(j1)]))
    i2 = rec(mid[:, :10]); j2 = rec(mid[:, 10:])
    tot = iv("tot", feats(i2 + j2))
    s = rec(tot)
    d = s[:, None] - np.arange(113)[None, :]
    lg = np.zeros_like(d)
    for k in FR:
        lg = lg + np.cos(2*math.pi*k*d/N)
    return lg

ALIGN = {"ci": ["embed.0"], "cj": ["embed.1"], "mid": ["resid_mid"], "tot": ["mlp_post", "resid_post"]}
