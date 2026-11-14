
import numpy as np

DESCRIPTION = (
 "For input [i, j, 113] the network's 113 logits have argmax (i*j) mod 113; token 113 is an "
 "operation marker at the last position. Tokens are embedded as clocks of the discrete "
 "logarithm base 3 mod 113: features cos/sin(2*pi*m*dlog(t)/112) for seven frequencies "
 "m = 4, 41, 28, 31, 30, 8, 50 (14 dims; token 0 is sent to dlog 0). The last position's "
 "attention output is (to 94%) the additive code h(i)+h(j) of those clocks, so the code "
 "variable is the sum of the two operand clocks; resid_mid is that plus a constant. The "
 "MLP decodes the code into the product: model finds the operand pair whose summed clock "
 "is closest to the code and returns the one-hot product."
)

P = 113
G = 3
MS = [4, 41, 28, 31, 30, 8, 50]

DL = np.zeros(P + 1, int)
_v = 1
for _k in range(P - 1):
    DL[_v] = _k
    _v = _v * G % P

def clock(d):
    out = []
    for m in MS:
        out.append(np.cos(2 * np.pi * m * d / 112.0))
        out.append(np.sin(2 * np.pi * m * d / 112.0))
    return np.stack(out, axis=-1)

K = 2 * len(MS)
TABLE = clock(DL[:P].astype(float))                     # 113 x K
CODE = (TABLE[:, None, :] + TABLE[None, :, :]).reshape(-1, K)
CNORM = (CODE ** 2).sum(1)
IDX = np.arange(P)
PROD = ((IDX[:, None] * IDX[None, :]) % P).reshape(-1)

def model(x, iv):
    t0 = DL[np.clip(x[:, 0].astype(int), 0, P)]
    t1 = DL[np.clip(x[:, 1].astype(int), 0, P)]
    tok0 = iv("tok0", clock(t0.astype(float)))
    tok1 = iv("tok1", clock(t1.astype(float)))
    code = iv("code", tok0 + tok1)
    B = code.shape[0]
    best = np.empty(B, int)
    for s in range(0, B, 256):
        c = code[s:s + 256]
        d = (c ** 2).sum(1)[:, None] - 2.0 * (c @ CODE.T) + CNORM[None, :]
        best[s:s + 256] = np.argmin(d, axis=1)
    p = PROD[best]
    return 10.0 * np.eye(113)[p] - 0.5

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "code": ["attn_out", "resid_mid"]}
