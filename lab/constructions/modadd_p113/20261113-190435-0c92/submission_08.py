
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 on inputs [i,j,113]. Each token is embedded as Fourier
features of its index at frequencies 8, 11, 22, 23, 25 (W_E[:113] is essentially rank 10 at exactly
those five frequencies). Attention at the last position mixes the i and j embeddings; resid_mid holds
the *sum* of the two embedding pairs per frequency (the difference direction is absent). The MLP turns
those pairs into products, i.e. cos/sin of f*(i+j), and the readout makes logits depending on
f*((i+j)-k), so the argmax is (i+j) mod 113. cos/sin of f(i+j) is the double angle of the half angle
atan2(sum of sines, sum of cosines), so the sum pair at resid_mid determines the logits."""
FR = [8, 11, 22, 23, 25]
W8 = [1.0, 0.46, 0.0, 0.81, 0.52]      # readout amplitude per frequency
N = 113.0
K = np.arange(113)[None, :]
CS = {f: (np.cos(2*math.pi*f*K/N), np.sin(2*math.pi*f*K/N)) for f in FR}

def pair(t, f):
    a = 2*math.pi*f*np.asarray(t, dtype=float)/N
    return np.stack([np.cos(a), np.sin(a)], 1)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    sp = []
    for f in FR:
        a = iv("if%d" % f, pair(i, f))
        b = iv("jf%d" % f, pair(j, f))
        sp.append(iv("sp%d" % f, a + b))
    lg = np.zeros((x.shape[0], 113))
    for n_, f in enumerate(FR):
        p = sp[n_]
        q = p[:, 0:1]**2 + p[:, 1:2]**2 + 1e-9
        tf = iv("tf%d" % f, np.concatenate([(p[:, 0:1]**2 - p[:, 1:2]**2)/q,
                                            2*p[:, 0:1]*p[:, 1:2]/q], 1))
        c, s_ = CS[f]
        lg = lg + W8[n_]*(tf[:, 0:1]*c + tf[:, 1:2]*s_)
    return 13.0*lg - 42.0

ALIGN = {}
for f in FR:
    ALIGN["if%d" % f] = ["embed.0"]
    ALIGN["jf%d" % f] = ["embed.1"]
    ALIGN["sp%d" % f] = ["resid_mid"]
    ALIGN["tf%d" % f] = ["mlp_post", "resid_post"]
