
import numpy as np

DESCRIPTION = (
    "Behaviour: the four numbers form an arithmetic sequence; the model predicts the next term "
    "answer = n4 + sign(n2-n1). Prefix does not matter. Stage 'layers 9-11' is explained by the "
    "final residual at the last comma holding the identity of the predicted answer (one-hot), from "
    "which the answer logits are read. The embedding cut (rough first attempt) names the identity "
    "of each of the four number tokens at resid0."
)
K = 123

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    K1 = 128
    hots = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        h = iv(nm, np.eye(K1)[x[:, j].astype(int)])
        hots.append(h.argmax(1).astype(float))
    n1, n2, n3, n4 = hots
    step = iv("step", np.sign(n2 - n1))
    nxt = iv("next", n4 + step)
    ans = iv("ans_onehot", np.eye(362)[np.clip(nxt.astype(int), 0, 361)])
    out = np.zeros((B, 362))
    out[np.arange(B), ans.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid12@end"],
    "n1v": ["resid0@n1"],
    "n2v": ["resid0@n2"],
    "n3v": ["resid0@n3"],
    "n4v": ["resid0@n4"],
}
