
import numpy as np

DESCRIPTION = (
    "The four numbers form an arithmetic sequence; the model predicts the next term: "
    "answer = n4 + sign(step) with step from the adjacent differences. The prefix is irrelevant. "
    "Embedding: resid0 at the four number positions carries each number token's identity (one-hot). "
    "Layers 3-5: the same number identities are still readable at the number positions at resid4. "
    "Layers 6-8 and 9-11: the last comma's residual already holds the identity of the predicted "
    "answer (one-hot), which the unembedding reads out."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    hots = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        h = iv(nm, np.eye(128)[x[:, j].astype(int)])
        hots.append(h.argmax(1).astype(float))
    n1, n2, n3, n4 = hots
    for j, nm in enumerate(["n1v4", "n2v4", "n3v4", "n4v4"]):
        iv(nm, np.eye(128)[x[:, j].astype(int)])
    d1 = np.sign(n2 - n1); d2 = np.sign(n3 - n2); d3 = np.sign(n4 - n3)
    step = iv("step", np.sign(d1 + d2 + d3))
    nxt = iv("next", n4 + step)
    ans = iv("ans_onehot", np.eye(362)[np.clip(nxt.astype(int), 0, 361)])
    out = np.zeros((B, 362))
    out[np.arange(B), ans.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid8@end", "resid12@end"],
    "n1v": ["resid0@n1"],
    "n2v": ["resid0@n2"],
    "n3v": ["resid0@n3"],
    "n4v": ["resid0@n4"],
    "n1v4": ["resid4@n1"],
    "n2v4": ["resid4@n2"],
    "n3v4": ["resid4@n3"],
    "n4v4": ["resid4@n4"],
}
