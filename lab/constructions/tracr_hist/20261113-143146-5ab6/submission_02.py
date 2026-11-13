
import numpy as np

DESCRIPTION = """
The network counts tokens: for each position p in 1..5 the output is the one-hot of
class m_p = number of occurrences of the token at p among positions 1..5.
The single attention head attends uniformly over {position 0} U {positions whose token
matches the query token}; the value is non-zero only at token 0, so the attention
output at p is q_p * v0 with q_p = 1/(m_p+1) (and 1 at position 0).
The MLP pre-activation is an affine function of q_p alone (embedding part is killed),
so the MLP output at p is a function of q_p only, and it is that output which the
final projection turns into the one-hot of m_p. Since the MLP output at p depends on
q_p through 5 distinct values, it (and hence the logits) is exactly a degree-4
polynomial in q_p; the coefficients are solved from the identity logits = one-hot(m).
Variables: token one-hot per position (at embed, and a terminal copy at resid0.mid),
q_p (at attn0.out / resid0.mid / mlp0.pre), and the powers q_p..q_p^4 per position
(at mlp0.out).
"""

QS = np.array([1.0/2, 1.0/3, 1.0/4, 1.0/5, 1.0/6])
VM = np.array([[q ** k for k in range(5)] for q in QS])
T = np.zeros((5, 6))
for i in range(5):
    T[i, i + 1] = 1.0
L = np.linalg.solve(VM, T)   # logits = sum_k L[k] q^k

def model(x, iv):
    t = x[:, 1:].astype(int)
    B = x.shape[0]
    tok = np.zeros((B, 15))
    for p in range(5):
        for k in range(3):
            tok[:, 3 * p + k] = (t[:, p] == k + 1).astype(float)
    tk = iv("tok", tok)
    rt = iv("rtok", tok)
    cnt = np.zeros((B, 5))
    for p in range(5):
        for j in range(5):
            cnt[:, p] += np.sum(tk[:, 3 * j:3 * j + 3] * tk[:, 3 * p:3 * p + 3], axis=1)
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

ALIGN = {"tok": ["embed"],
         "rtok": ["resid0.mid"],
         "q": ["attn0.out", "resid0.mid", "mlp0.pre"],
         "v1": ["mlp0.out"], "v2": ["mlp0.out"], "v3": ["mlp0.out"],
         "v4": ["mlp0.out"], "v5": ["mlp0.out"]}
