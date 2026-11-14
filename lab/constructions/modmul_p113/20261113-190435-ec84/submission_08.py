
import numpy as np

DESCRIPTION = (
 "For input [i, j, 113] the 113 output logits have argmax (i*j) mod 113; token 113 is an "
 "operation marker at the last position. Mechanism: each operand token is embedded as a "
 "'clock' of its discrete logarithm base 3 mod 113, cos/sin(2*pi*m*dlog(t)/112) for the "
 "frequencies m = 4, 28, 31, 41 (8 dims). The last position's attention is a near-uniform "
 "average of the two operands' value vectors, so attn_out and resid_mid hold the sum of the "
 "two clocks (an additive code), and mlp_pre is that code read through W_in. The MLP turns "
 "the summed clocks into the clock of the sum of the two dlogs (= clock of dlog of the "
 "product) by the product-to-sum identity: from C=cos(a_i)+cos(a_j), S=sin(a_i)+sin(a_j), "
 "the doubled angle has cos(2*psi)=2C^2/(C^2+S^2)-1 and sin(2*psi)=2CS/(C^2+S^2). That "
 "product clock is what mlp_out and resid_post carry. The unembedding is a ring readout: "
 "logit(k) is the similarity between the product clock and the clock of class k. A zero "
 "operand (tokens 0, which have no discrete log) forces the product class 0."
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

KF = clock(DL[:P].astype(float))          # 113 x 8, the class clocks
CL0 = DL[:P].astype(float)

def model(x, iv):
    t = x.astype(int)
    tok0 = iv("tok0", clock(DL[np.clip(t[:, 0], 0, P)].astype(float)))
    tok1 = iv("tok1", clock(DL[np.clip(t[:, 1], 0, P)].astype(float)))
    z0 = iv("z0", (t[:, 0] == 0).astype(float))
    z1 = iv("z1", (t[:, 1] == 0).astype(float))
    code = iv("code", tok0 + tok1)                      # summed clocks
    Bn = code.shape[0]
    pc = np.zeros((Bn, 8))
    for k in range(4):
        C = code[:, 2 * k]
        S = code[:, 2 * k + 1]
        n2 = C * C + S * S
        good = n2 > 1e-9
        pc[:, 2 * k] = np.where(good, 2.0 * C * C / np.where(good, n2, 1.0) - 1.0, 1.0)
        pc[:, 2 * k + 1] = np.where(good, 2.0 * C * S / np.where(good, n2, 1.0), 0.0)
    pcode = iv("pcode", pc)                             # clock of the product's dlog
    logits = 10.0 * (pcode @ KF.T)                      # ring readout
    logits[:, 0] -= 5.0
    logits[:, 0] += 200.0 * (z0 + z1)                   # zero operand -> product 0
    return logits

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"],
         "z0": ["embed.0"], "z1": ["embed.1"],
         "code": ["attn_out", "resid_mid", "mlp_pre"],
         "pcode": ["mlp_out", "resid_post"]}
