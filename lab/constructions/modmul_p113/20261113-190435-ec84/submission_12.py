
import numpy as np

DESCRIPTION = (
 "The network computes (i*j) mod 113 for input [i, j, 113]; token 113 is an operation marker "
 "attended to only slightly. attn_out/resid_mid are an additive code const + h(i) + h(j) where "
 "h(t) = cos/sin(2*pi*m*dlog_3(t)/112) for m = 4, 28, 31, 41, 8, 56, 30, 50 (16 numbers per "
 "token), so the sum of the two tokens' codes ('code') is a linear image of the site; its last "
 "two coordinates are the difference clock cos/sin(4*(dlog i - dlog j)), which cover the "
 "pair-dependent part of the attention. The product p = i*j has dlog(i)+dlog(j), so its clock "
 "at m follows from the sum code at m and 2m by angle addition: "
 "cos(a+b) = (C^2-S^2)/2 - C_2m/2, sin(a+b) = C*S - S_2m/2 (2m folded mod 112, which is why "
 "8, 56, 30, 50 appear). 'pcode' is that product clock; the MLP writes it into "
 "mlp_out/resid_post and the unembedding reads the class of the product, so the model "
 "nearest-neighbour decodes p from pcode."
)

P = 113
G = 3
MS4 = [4, 28, 31, 41]
MS8 = [4, 28, 31, 41, 8, 56, 30, 50]

def dlogs():
    dl = np.zeros(P + 2, int)
    v = 1
    for k in range(P - 1):
        dl[v] = k
        v = v * G % P
    dl[0] = 56
    return dl

DL = dlogs()

def feat(tok, MS):
    d = DL[np.clip(np.asarray(tok, dtype=int), 0, P)]
    return np.stack([np.cos(2 * np.pi * m * d / 112.0) for m in MS] +
                    [np.sin(2 * np.pi * m * d / 112.0) for m in MS], axis=1)

TAB = feat(np.arange(P + 1), MS4)

def prodclock(c):
    s = c[:, 8:16]
    ix = {m: k for k, m in enumerate(MS8)}
    cs = []
    ss = []
    for m in MS4:
        h = (2 * m) % 112
        if h <= 56:
            cc, sc = c[:, ix[h]], s[:, ix[h]]
        else:
            cc, sc = c[:, ix[112 - h]], -s[:, ix[112 - h]]
        cs.append(0.5 * (c[:, ix[m]] ** 2 - s[:, ix[m]] ** 2) - 0.5 * cc)
        ss.append(c[:, ix[m]] * s[:, ix[m]] - 0.5 * sc)
    return np.hstack([np.stack(cs, 1), np.stack(ss, 1)])

def model(x, iv):
    i0 = np.minimum(x[:, 0].astype(int), P)
    j0 = np.minimum(x[:, 1].astype(int), P)
    f0 = iv("tok0", feat(i0, MS4))
    f1 = iv("tok1", feat(j0, MS4))
    i = np.argmin(((f0[:, None, :] - TAB[None]) ** 2).sum(-1), axis=1)
    j = np.argmin(((f1[:, None, :] - TAB[None]) ** 2).sum(-1), axis=1)
    gi = feat(i, [4])
    gj = feat(j, [4])
    df = np.stack([gi[:, 0] * gj[:, 0] + gi[:, 1] * gj[:, 1],
                   gi[:, 1] * gj[:, 0] - gi[:, 0] * gj[:, 1]], axis=1)
    code = iv("code", np.hstack([feat(i, MS8) + feat(j, MS8), df]))
    pc = iv("pcode", prodclock(code))
    p = np.argmin(((pc[:, None, :] - TAB[None]) ** 2).sum(-1), axis=1)
    return 10.0 * np.eye(113)[p] - 0.5

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "code": ["attn_out", "resid_mid", "mlp_pre"],
         "pcode": ["mlp_out", "resid_post"]}
