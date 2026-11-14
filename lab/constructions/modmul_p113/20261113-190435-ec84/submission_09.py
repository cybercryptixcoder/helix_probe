
import numpy as np

DESCRIPTION = (
 "The network computes (i*j) mod 113 for input [i, j, 113]; the last token is an operation "
 "marker whose attention is nearly uniform. attn_out and resid_mid are additive codes: "
 "const + h(i) + h(j), where h is a Fourier code of the discrete log base 3 mod 113: "
 "cos/sin(2*pi*m*dlog(t)/112) for m = 4, 28, 31, 41, 30, 50 (12 numbers per operand). "
 "fa/fb are those per-operand codes at the attention sites; the model multiplies the two "
 "decoded operands and one-hots the product."
)

P = 113
G = 3
MS = [4, 28, 31, 41, 30, 50]

def dlogs():
    dl = np.zeros(P + 2, int)
    v = 1
    for k in range(P - 1):
        dl[v] = k
        v = v * G % P
    dl[0] = 56            # token 0's nearest clock code (it has no discrete log)
    return dl

DL = dlogs()

def feat(tok):
    d = DL[np.clip(np.asarray(tok, dtype=int), 0, P)]
    out = []
    for m in MS:
        out.append(np.cos(2 * np.pi * m * d / 112.0))
    for m in MS:
        out.append(np.sin(2 * np.pi * m * d / 112.0))
    return np.stack(out, axis=1)

TABLE = feat(np.arange(P + 1))

def model(x, iv):
    i0 = np.minimum(x[:, 0].astype(int), P)
    j0 = np.minimum(x[:, 1].astype(int), P)
    f0 = iv("tok0", feat(i0))
    f1 = iv("tok1", feat(j0))
    i = np.argmin(((f0[:, None, :] - TABLE[None]) ** 2).sum(-1), axis=1)
    j = np.argmin(((f1[:, None, :] - TABLE[None]) ** 2).sum(-1), axis=1)
    fa = iv("fa", feat(i))
    fb = iv("fb", feat(j))
    p = (i * j) % P
    return 10.0 * np.eye(113)[p] - 0.5

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "fa": ["attn_out", "resid_mid"], "fb": ["attn_out", "resid_mid"]}
