
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 on [i,j,113]. Tokens are embedded as Fourier features of
their index at frequencies 8, 11, 22, 23, 25 (W_E[:113] is essentially rank 10 at those five
frequencies). The last position carries the constant query token 113, so the attention layer's output
there is (essentially) the sum of the i- and j-feature pairs; resid_mid therefore holds, for each
frequency, the pair cos/sin(f i)+cos/sin(f j), plus weaker second-order content (the already formed
sum-frequency content cos/sin(f(i+j)) for f = 8, 23, 25, which is present at the site but is not read by
the MLP: ablating it changes no decision). The MLP multiplies the pairs to get cos/sin of f(i+j) - the
double angle of the pair's own angle atan2(sum of sines, sum of cosines) - and the readout turns those
into logits peaked at k = (i+j) mod 113. Hence the recorded sum pair at resid_mid determines the answer."""
FR = [8, 11, 22, 23, 25]
TA = [8, 23, 25]
W8 = [1.0, 0.35, 0.0, 0.85, 0.78]
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
    for f in TA:                     # second-order content present at resid_mid, unused downstream
        iv("t%d" % f, dbl(sp[f]))
    lg = np.zeros((x.shape[0], 113))
    for n, f in enumerate(FR):
        tf = iv("tf%d" % f, dbl(sp[f]))
        c, s_ = CS[f]
        lg = lg + W8[n]*(tf[:, 0:1]*c + tf[:, 1:2]*s_)
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
