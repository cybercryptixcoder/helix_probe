import numpy as np
DESCRIPTION = ("Network computes (i+j) mod 113 for input [i,j,113]. Every token t is coded by 4 orthogonal Fourier pairs: "
 "cos/sin(2*pi*k*t/113) for k in {8,11,23,25}; embed.0/embed.1 carry the 8-dim code of i and of j. Attention at the last "
 "position (weights softmax over s_h(i), s_h(j), const, with s_h a Fourier mode) passes the i-code and the j-code, gated per head, "
 "into the residual stream; attn_out/resid_mid are spanned by the 16 numbers [cos_k i, sin_k i, cos_k j, sin_k j] plus their "
 "gate modulation. The MLP multiplies the k-th i-code with the k-th j-code, so the residual stream after the MLP carries, for each "
 "k, cos/sin of 2*pi*k*s_k/113 with s_k=(i+j) mod 113. The unembedding reads each pair out as 12.5/6.2/9.8/6.7*cos(2*pi*k*(s_k-c)/113).")
FREQ = [8, 11, 23, 25]
INV = {8: 99.0, 11: 72.0, 23: 59.0, 25: 104.0}
AMP = {8: 12.5, 11: 6.2, 23: 9.8, 25: 6.7}
MU = -42.06
def code(t):
    return np.stack([f(2*np.pi*k*t/113.0) for k in FREQ for f in (np.cos, np.sin)], 1)
def pair(t, k):
    return np.stack([np.cos(2*np.pi*k*t/113.0), np.sin(2*np.pi*k*t/113.0)], 1)
def est(v, k):
    th = np.arctan2(v[:, 1], v[:, 0])
    return ((th*113.0/(2*np.pi)) % 113.0)*INV[k] % 113.0
def model(x, iv):
    B = x.shape[0]; c = np.arange(113)[None, :]
    ci = code(x[:, 0].astype(float)); cj = code(x[:, 1].astype(float))
    ei = []; ej = []
    for q, k in enumerate(FREQ):
        ei.append(est(iv("i%d" % k, ci[:, 2*q:2*q+2]), k))
        ej.append(est(iv("j%d" % k, cj[:, 2*q:2*q+2]), k))
    ai = []; aj = []
    for q, k in enumerate(FREQ):
        ai.append(est(iv("ai%d" % k, pair(ei[q], k)), k))
        aj.append(est(iv("aj%d" % k, pair(ej[q], k)), k))
    out = np.full((B, 113), MU)
    for q, k in enumerate(FREQ):
        s_k = (ai[q] + aj[q]) % 113
        v = iv("k%d" % k, pair(s_k, k))
        T = (np.arctan2(v[:, 1], v[:, 0])*113.0/(2*np.pi*k)) % 113.0
        out = out + AMP[k]*np.cos(2*np.pi*k*(T[:, None] - c)/113.0)
    return out
ALIGN = {}
for k in FREQ:
    ALIGN["i%d" % k] = ["embed.0"]; ALIGN["j%d" % k] = ["embed.1"]
    ALIGN["ai%d" % k] = ["attn_out", "resid_mid"]; ALIGN["aj%d" % k] = ["attn_out", "resid_mid"]
    ALIGN["k%d" % k] = ["mlp_post", "mlp_out", "resid_post"]
