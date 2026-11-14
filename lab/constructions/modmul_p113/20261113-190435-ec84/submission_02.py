
import numpy as np

DESCRIPTION = (
 "The network computes (i*j) mod 113 for input [i, j, 113]. The last token is an "
 "operation marker; its attention is nearly uniform, so attn_out (and resid_mid) is an "
 "additive code: c + h(i) + h(j). h is Fourier in the discrete log base 3 mod 113: "
 "cos/sin(2*pi*m*dlog(t)/112) for m = 4, 28, 31, 41. The MLP turns that sum code into a "
 "code of the product p=(i*j)%113, which the unembedding reads out. Here the embedding "
 "sites are named by those discrete-log Fourier features, and the model decodes the two "
 "operands from them, multiplies, and one-hots the product."
)

P = 113
G = 3

def dlogs():
    dl = np.zeros(P + 1, int)
    v = 1
    for k in range(P - 1):
        dl[v] = k
        v = v * G % P
    return dl

DL = dlogs()
MS = [4, 28, 31, 41]

def feat(tok):
    # tok: [B] token ids -> [B, 8] discrete-log Fourier features
    d = DL[np.clip(tok, 0, P)]
    out = []
    for m in MS:
        out.append(np.cos(2 * np.pi * m * d / 112.0))
        out.append(np.sin(2 * np.pi * m * d / 112.0))
    return np.stack(out, axis=1)

TABLE = feat(np.arange(P + 1))   # 114 x 8

def model(x, iv):
    i0 = x[:, 0].astype(int)
    j0 = x[:, 1].astype(int)
    f0 = iv("tok0", feat(i0))
    f1 = iv("tok1", feat(j0))
    # decode nearest token in feature space
    d0 = ((f0[:, None, :] - TABLE[None, :, :]) ** 2).sum(-1)
    d1 = ((f1[:, None, :] - TABLE[None, :, :]) ** 2).sum(-1)
    i = np.argmin(d0, axis=1)
    j = np.argmin(d1, axis=1)
    p = (i * j) % P
    return 10.0 * np.eye(113)[p] - 0.5

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"]}
