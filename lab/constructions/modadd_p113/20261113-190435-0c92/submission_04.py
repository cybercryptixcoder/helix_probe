
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 on inputs [i,j,113]. Each token is embedded as Fourier
features of its index at frequencies 8, 11, 22, 23, 25 (W_E is essentially rank 10 at exactly those
five frequencies). Attention at the last position mixes the i and j embeddings, the MLP takes products
of the i- and j-features, i.e. cos/sin of f*(i+j) and f*(i-j), and the readout makes logits that
depend on f*((i+j)-k), so the argmax is (i+j) mod 113. The mechanism is (nearly) additive across the
five frequencies, so every site is described by one cos/sin pair per frequency."""
FR = [8, 11, 22, 23, 25]
W8 = [1.0, 1.0, 0.05, 1.0, 1.0]   # readout weight per frequency
N = 113.0
INV = [99, 72, 36, 64, 95]        # 1/f mod 113

def pair(t, f):
    a = 2*math.pi*f*np.asarray(t, dtype=float)/N
    return np.stack([np.cos(a), np.sin(a)], 1)

def dec(P, f, inv):
    ang = np.arctan2(P[:, 1], P[:, 0])
    return np.mod(np.mod(ang*N/(2*math.pi), N)*inv, N)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ii = []; jj = []
    for f, inv in zip(FR, INV):
        ii.append(dec(iv("if%d" % f, pair(i, f)), f, inv))
        jj.append(dec(iv("jf%d" % f, pair(j, f)), f, inv))
    i2 = []; j2 = []
    for n_, (f, inv) in enumerate(zip(FR, INV)):
        i2.append(dec(iv("mi%d" % f, pair(ii[n_], f)), f, inv))
        j2.append(dec(iv("mj%d" % f, pair(jj[n_], f)), f, inv))
    s = []
    for n_, (f, inv) in enumerate(zip(FR, INV)):
        s.append(dec(iv("tf%d" % f, pair(i2[n_]+j2[n_], f)), f, inv))
    k = np.arange(113)[None, :]
    lg = np.zeros((x.shape[0], 113))
    for n_, f in enumerate(FR):
        lg = lg + W8[n_]*np.cos(2*math.pi*f*(s[n_][:, None] - k)/N)
    return lg

ALIGN = {}
for f in FR:
    ALIGN["if%d" % f] = ["embed.0"]
    ALIGN["jf%d" % f] = ["embed.1"]
    ALIGN["mi%d" % f] = ["resid_mid"]
    ALIGN["mj%d" % f] = ["resid_mid"]
    ALIGN["tf%d" % f] = ["mlp_post", "resid_post"]
