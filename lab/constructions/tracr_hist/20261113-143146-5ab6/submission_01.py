
import numpy as np

DESCRIPTION = """
The network counts tokens. For each position p in 1..5 the output is a one-hot over
classes 0..5 with the class equal to the number of occurrences of the token at p
among positions 1..5 (never 0, so classes 1..5). Mechanism: the single attention
head attends UNIFORMLY over {position 0} U {positions whose token equals the query
token}; the value function is non-zero only for token 0, so the attention output at
position p is q_p * v0 with q_p = 1/(m_p+1), where m_p is the count of the token at p.
The MLP turns q_p into the count and the final projection gives a one-hot.
This construction carries the per-position token identity (3-dim one-hot) and the
scalar q_p = 1/(m_p+1); the output is the one-hot of round(1/q_p - 1).
"""

def model(x, iv):
    t = x[:, 1:].astype(int)
    B = x.shape[0]
    tok = np.zeros((B, 15))
    for p in range(5):
        for k in range(3):
            tok[:, 3 * p + k] = (t[:, p] == k + 1).astype(float)
    tok = iv("tok", tok)
    cnt = np.zeros((B, 5))
    for p in range(5):
        cnt[:, p] = (t == t[:, p:p + 1]).sum(1)
    q = iv("q", 1.0 / (cnt + 1.0))
    m = np.clip(np.round(1.0 / q - 1.0), 0, 5).astype(int)
    out = np.zeros((B, 30))
    for p in range(5):
        out[np.arange(B), p * 6 + m[:, p]] = 1.0
    return out

ALIGN = {"tok": ["embed", "resid0.mid"],
         "q": ["attn0.out", "resid0.mid", "mlp0.pre"]}
