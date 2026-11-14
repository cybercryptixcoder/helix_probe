
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 on inputs [i,j,113]. Each token is embedded as Fourier
features of its index at frequencies 8, 11, 22, 23, 25 (W_E is essentially rank 10 at exactly those
five frequencies). Attention at the last position mixes the i and j embeddings, so resid_mid contains
the *sum* of the i- and j-features per frequency (the difference direction is nearly absent); the MLP
takes the products of those features, i.e. cos/sin of f*(i+j) and f*(i-j); the readout makes logits
that depend on f*((i+j)-k), so the argmax is (i+j) mod 113. Since cos f(i+j),sin f(i+j) is the
double-angle of the half-angle atan2(sin f i + sin f j, cos f i + cos f j), the sum pair at a site
determines its contribution to the logits."""
FR = [8, 11, 22, 23, 25]
INV = [99, 72, 36, 59, 104]                 # 1/f mod 113
W8 = [1.0, 0.46, 0.0, 0.81, 0.52]           # measured readout amplitude per frequency
N = 113.0
K = np.arange(113)[None, :]

def pair(t, f):
    a = 2*math.pi*f*np.asarray(t, dtype=float)/N
    return np.stack([np.cos(a), np.sin(a)], 1)

def dec(P, inv):
    ang = np.arctan2(P[:, 1], P[:, 0])
    return np.mod(np.mod(ang*N/(2*math.pi), N)*inv, N)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ii = []; jj = []
    for f, inv in zip(FR, INV):
        ii.append(dec(iv("if%d" % f, pair(i, f)), inv))
        jj.append(dec(iv("jf%d" % f, pair(j, f)), inv))
    sp = []
    for n_, f in enumerate(FR):
        sp.append(iv("sp%d" % f, pair(ii[n_], f) + pair(jj[n_], f)))
    lg = np.zeros((x.shape[0], 113))
    for n_, f in enumerate(FR):
        th = np.arctan2(sp[n_][:, 1], sp[n_][:, 0])          # half angle
        tp = iv("tf%d" % f, np.stack([np.cos(2*th), np.sin(2*th)], 1))
        lg = lg + W8[n_]*(tp[:, 0:1]*np.cos(2*math.pi*f*K/N) + tp[:, 1:2]*np.sin(2*math.pi*f*K/N))
    return lg

ALIGN = {}
for f in FR:
    ALIGN["if%d" % f] = ["embed.0"]
    ALIGN["jf%d" % f] = ["embed.1"]
    ALIGN["sp%d" % f] = ["resid_mid"]
    ALIGN["tf%d" % f] = ["mlp_post", "resid_post"]
