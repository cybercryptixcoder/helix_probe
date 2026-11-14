
import numpy as np

DESCRIPTION = (
    "First-pass construction (behaviour only). The model reads four numbers n1..n4 forming an "
    "arithmetic sequence and predicts the next term: answer = n4 + sign(n2-n1). The prefix "
    "(Numbers:/Count:/List:/Order:) does not change the answer. No network sites are explained yet."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    n1, n2, n3, n4 = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
    step = iv("step", np.sign(n2 - n1))
    nxt = iv("next", n4 + step)
    B = x.shape[0]
    out = np.zeros((B, 362))
    idx = np.clip(nxt.astype(int), 0, 361)
    out[np.arange(B), idx] = 10.0
    return out

ALIGN = {}
