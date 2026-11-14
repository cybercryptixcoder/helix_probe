
import numpy as np

DESCRIPTION = (
    "The four numbers form an arithmetic sequence; the model predicts the next term: "
    "answer = n4 + sign(step), where the step is read from the adjacent differences (the network is "
    "robust to changes of a single earlier number, so the direction is a majority-type combination of "
    "the differences n2-n1, n3-n2, n4-n3). The prefix does not matter. "
    "Stage layers 9-11: the final residual at the last comma holds the identity of the predicted "
    "answer (one-hot) from which the answer logits are read. "
    "Embedding stage: resid0 at the four number positions holds the identity of each number token."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    hots = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        h = iv(nm, np.eye(128)[x[:, j].astype(int)])
        hots.append(h.argmax(1).astype(float))
    n1, n2, n3, n4 = hots
    d1 = np.sign(n2 - n1)
    d2 = np.sign(n3 - n2)
    d3 = np.sign(n4 - n3)
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
