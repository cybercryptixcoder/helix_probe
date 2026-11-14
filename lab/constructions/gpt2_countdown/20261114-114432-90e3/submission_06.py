
import numpy as np

DESCRIPTION = (
    "The four numbers form an arithmetic sequence; the model predicts the next term: "
    "answer = n4 + sign(step), the step being a majority-type combination of the adjacent "
    "differences n2-n1, n3-n2, n4-n3 (the network tolerates changing one earlier number). "
    "The prefix does not matter. Layers 9-11: the final residual at the last comma holds the "
    "identity of the predicted answer (one-hot) from which the answer logits are read. "
    "Embedding: resid0 at the four number positions holds each number token's identity; "
    "head 7.11 at the last comma attends to the number positions (5,7,9) and carries the step."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    hots = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        h = iv(nm, np.eye(128)[x[:, j].astype(int)])
        hots.append(h.argmax(1).astype(float))
    n1, n2, n3, n4 = hots
    d1 = np.sign(n2 - n1); d2 = np.sign(n3 - n2); d3 = np.sign(n4 - n3)
    step = iv("step", np.sign(d1 + d2 + d3))
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
