
import numpy as np

DESCRIPTION = (
    "First-pass construction. The model reads four numbers n1..n4 forming an arithmetic sequence "
    "and predicts the next term: answer = n4 + sign(n2-n1); the prefix does not change the answer. "
    "The only explained site is the final residual at the last comma, taken to hold the identity of "
    "the predicted number (one-hot) plus the sign of the step."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    n1, n2, n3, n4 = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
    step = iv("step", np.sign(n2 - n1))
    nxt = iv("next", n4 + step)
    B = x.shape[0]
    out = np.zeros((B, 362))
    idx = np.clip(nxt.astype(int), 0, 361)
    onehot = iv("ans_onehot", np.eye(362)[idx])
    out[np.arange(B), onehot.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid12@end"],
    "step": ["resid12@end"],
}
