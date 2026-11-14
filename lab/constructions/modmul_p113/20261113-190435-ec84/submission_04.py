
import numpy as np

DESCRIPTION = (
 "Task: for input [i, j, 113] the network outputs 113 logits whose argmax is (i*j) mod 113 "
 "(token 113 is an operation marker at the last position)."
 " EMBEDDING: tokens are embedded as clocks of the discrete logarithm base 3 mod 113: "
 "features cos/sin(2*pi*m*dlog(t)/112) for m = 4, 28, 31, 41 (8 dims; token 0 -> dlog 0)."
 " ATTENTION: the last position's query is a constant, the attention weights are near "
 "uniform (0.5/0.5), so the attention output is an additive code of the two operands: "
 "attn_out = const + h(i) + h(j), with h the same clock features. resid_mid equals that "
 "plus the constant position-2 embedding. So the code variable is the sum of the two "
 "operand clocks, and it determines the product (the MLP decodes it): model finds the "
 "operand pair whose summed clock is closest and returns the one-hot product."
)

P = 113
G = 3
MS = [4, 28, 31, 41]

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

TABLE = clock(DL[:P].astype(float))                     # 113 x 8
CODE = (TABLE[:, None, :] + TABLE[None, :, :]).reshape(-1, 8)   # 12769 x 8
CNORM = (CODE ** 2).sum(1)
IDX = np.arange(P)
PROD = ((IDX[:, None] * IDX[None, :]) % P).reshape(-1)

def model(x, iv):
    t0 = DL[np.clip(x[:, 0].astype(int), 0, P)]
    t1 = DL[np.clip(x[:, 1].astype(int), 0, P)]
    tok0 = iv("tok0", clock(t0.astype(float)))
    tok1 = iv("tok1", clock(t1.astype(float)))
    code = iv("code", tok0 + tok1)
    d = (code ** 2).sum(1)[:, None] - 2.0 * (code @ CODE.T) + CNORM[None, :]
    best = np.argmin(d, axis=1)
    p = PROD[best]
    return 10.0 * np.eye(113)[p] - 0.5

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "code": ["attn_out", "resid_mid"]}
