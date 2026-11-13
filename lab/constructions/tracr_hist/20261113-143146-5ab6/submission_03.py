
import numpy as np

DESCRIPTION = """
The network counts tokens: at each position p in 1..5 the output is the one-hot of
class m_p = number of occurrences of the token at p among positions 1..5.
The single attention head attends uniformly over {position 0} U {positions whose token
equals the query token}; its value is non-zero only at token 0, so the attention
output at p is q_p * v0 with q_p = 1/(m_p+1) (q_0 = 1).  The MLP pre-activation is
affine in q_p alone (the token/position part of the embedding is annihilated by W_in),
so the MLP output at p is a degree-4 polynomial in q_p, and the final projection turns
that into the one-hot of m_p.  The coefficients below are solved from the identity
logits = one-hot(m) on the 5 attainable values of q.
Variables: token code per position (2 coordinates: [t==2],[t==3]) at embed and a
terminal copy at resid0.mid, q_p at attn0.out / resid0.mid / mlp0.pre, and the powers
q..q^4 per position at mlp0.out.
"""

QS = np.array([1.0 / 2, 1.0 / 3, 1.0 / 4, 1.0 / 5, 1.0 / 6])
VM = np.array([[q ** k for k in range(5)] for q in QS])
T = np.zeros((5, 6))
for i in range(5):
    T[i, i + 1] = 1.0
L = np.linalg.solve(VM, T)          # logits = sum_k L[k] q^k

def model(x, iv):
    t = x[:, 1:].astype(int)
    B = x.shape[0]
    a = (t == 2).astype(float)
    b = (t == 3).astype(float)
    tk = []
    for p in range(5):
        tk.append(iv("c%d" % (p + 1), np.stack([a[:, p], b[:, p]], axis=1)))
    rt = []
    for p in range(5):
        rt.append(iv("r%d" % (p + 1), np.stack([a[:, p], b[:, p]], axis=1)))
    cnt = np.zeros((B, 5))
    for p in range(5):
        for j in range(5):
            aj, bj = tk[j][:, 0], tk[j][:, 1]
            ap, bp = tk[p][:, 0], tk[p][:, 1]
            same = (aj * ap + (1 - aj) * (1 - ap)) * (bj * bp + (1 - bj) * (1 - bp))
            cnt[:, p] += same
    q = iv("q", 1.0 / (1.0 + cnt))
    out = np.zeros((B, 30))
    for p in range(5):
        v = np.stack([q[:, p] ** k for k in range(1, 5)], axis=1)
        v = iv("v%d" % (p + 1), v)
        lg = np.tile(L[0], (B, 1))
        for k in range(4):
            lg = lg + v[:, k:k + 1] * L[k + 1][None, :]
        out[:, 6 * p:6 * p + 6] = lg
    return out

ALIGN = {}
for p in range(5):
    ALIGN["c%d" % (p + 1)] = ["embed"]
    ALIGN["r%d" % (p + 1)] = ["resid0.mid"]
    ALIGN["v%d" % (p + 1)] = ["mlp0.out"]
ALIGN["q"] = ["attn0.out", "resid0.mid", "mlp0.pre"]
