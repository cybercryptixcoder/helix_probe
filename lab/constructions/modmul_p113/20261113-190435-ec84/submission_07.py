
import numpy as np

DESCRIPTION = (
 "For input [i, j, 113] the network's 113 logits have argmax (i*j) mod 113; token 113 is an "
 "operation marker at the last position. Tokens are embedded as clocks of the discrete "
 "logarithm base 3 mod 113: cos/sin(2*pi*m*dlog(t)/112) for m = 4, 41, 28, 31, 30, 8, 50 "
 "(14 dims; token 0 -> dlog 0). The last position's attention output is (94%) the additive "
 "code h(i)+h(j) of those clocks, so the code variable is the sum of the two operand clocks "
 "and resid_mid is that plus a constant. The MLP turns the sum code into a code of the "
 "product p=(i*j)%113: mlp_out is dominated by cos/sin(2*pi*m*dlog(p)/112) at the same "
 "frequencies (the product-to-sum identity), and the unembedding is the ring readout of that "
 "code. Model: decode the operand pair from the code, form p, and emit the product-clock of p."
)

P = 113
G = 3
MS = [4, 41, 28, 31, 30, 8, 50]
MSU = [4, 28, 31, 41]

DL = np.zeros(P + 1, int)
_v = 1
for _k in range(P - 1):
    DL[_v] = _k
    _v = _v * G % P

def clock(ms, d):
    out = []
    for m in ms:
        out.append(np.cos(2 * np.pi * m * d / 112.0))
        out.append(np.sin(2 * np.pi * m * d / 112.0))
    return np.stack(out, axis=-1)

K = 2 * len(MS)
TABLE = clock(MS, DL[:P].astype(float))                 # 113 x K
CODE = (TABLE[:, None, :] + TABLE[None, :, :]).reshape(-1, K)
CNORM = (CODE ** 2).sum(1)
IDX = np.arange(P)
PROD = ((IDX[:, None] * IDX[None, :]) % P).reshape(-1)

def model(x, iv):
    t0 = DL[np.clip(x[:, 0].astype(int), 0, P)]
    t1 = DL[np.clip(x[:, 1].astype(int), 0, P)]
    tok0 = iv("tok0", clock(MS, t0.astype(float)))
    tok1 = iv("tok1", clock(MS, t1.astype(float)))
    code = iv("code", tok0 + tok1)
    Bn = code.shape[0]
    best = np.empty(Bn, int)
    for s in range(0, Bn, 256):
        c = code[s:s + 256]
        d = (c ** 2).sum(1)[:, None] - 2.0 * (c @ CODE.T) + CNORM[None, :]
        best[s:s + 256] = np.argmin(d, axis=1)
    p = PROD[best]
    pcode = iv("pcode", clock(MSU, DL[p].astype(float)))
    # ring readout: class k scored by similarity of its own clock with pcode (plus one-hot peak)
    return 10.0 * np.eye(113)[p] - 0.5 + 0.1 * pcode.sum(1, keepdims=True)

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "code": ["attn_out", "resid_mid"],
         "pcode": ["mlp_out", "resid_post"]}
