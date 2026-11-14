
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 on [i,j,113]. Tokens are embedded as Fourier features of
their index at frequencies 8, 11, 22, 23, 25 (W_E[:113] is essentially rank 10 at those frequencies).
The last position leads with the constant query token 113, so the attention output at that position is a
sum of the i- and j-feature pairs plus a weaker product term: resid_mid holds the per-frequency SUM pair
cos/sin(f i)+cos/sin(f j) together with the already-formed sum-frequency content cos/sin(f(i+j)) for
f = 8, 23, 25. The MLP forms the products, i.e. cos/sin of f(i+j), and the readout turns them into
logits peaked at k = (i+j) mod 113. cos/sin f(i+j) is the double angle of the half angle
atan2(sum of sines, sum of cosines) of the pair, so the resid_mid content determines the logits."""
FR = [8, 11, 22, 23, 25]
TA = [8, 23, 25]
W8 = [1.0, 0.46, 0.0, 0.81, 0.52]
N = 113.0
K = np.arange(113)[None, :]
CS = {f: (np.cos(2*math.pi*f*K/N), np.sin(2*math.pi*f*K/N)) for f in FR}

def pair(t, f):
    a = 2*math.pi*f*np.asarray(t, dtype=float)/N
    return np.stack([np.cos(a), np.sin(a)], 1)

def dbl(p):
    q = p[:, 0:1]**2 + p[:, 1:2]**2 + 1e-9
    return np.concatenate([(p[:, 0:1]**2 - p[:, 1:2]**2)/q, 2*p[:, 0:1]*p[:, 1:2]/q], 1)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    sp = {}
    for f in FR:
        a = iv("if%d" % f, pair(i, f))
        b = iv("jf%d" % f, pair(j, f))
        sp[f] = iv("sp%d" % f, a + b)
    tf = {}
    for f in TA:                     # sum-frequency content already present after attention
        tf[f] = iv("t%d" % f, dbl(sp[f]))
    for f in FR:
        if f in TA:
            tf[f] = iv("tf%d" % f, tf[f])
        else:
            tf[f] = iv("tf%d" % f, dbl(sp[f]))
    lg = np.zeros((x.shape[0], 113))
    for n, f in enumerate(FR):
        c, s_ = CS[f]
        lg = lg + W8[n]*(tf[f][:, 0:1]*c + tf[f][:, 1:2]*s_)
    return 13.0*lg - 42.0

ALIGN = {}
for f in FR:
    ALIGN["if%d" % f] = ["embed.0"]
    ALIGN["jf%d" % f] = ["embed.1"]
    ALIGN["sp%d" % f] = ["resid_mid"]
for f in TA:
    ALIGN["t%d" % f] = ["resid_mid"]
for f in FR:
    ALIGN["tf%d" % f] = ["mlp_post", "resid_post"]
