
import numpy as np

DESCRIPTION = (
 "Four numbers in an arithmetic progression; the answer is the next term, n4 + sign(step), where step is the "
 "sign of the sum of the three adjacent differences (a majority-type vote, so one corrupted earlier number does "
 "not change the answer). The prefix is irrelevant. Embedding (resid0): each of the four number token positions "
 "holds the identity (one-hot) of that number. Layers 0-2 copy those identities forward: resid4 at the four "
 "number positions again holds the four identities (slightly mixed, so the one-hot is only an approximate "
 "coordinate). Layers 6-8 combine them: attention head 7.11 at the last comma reads positions 5,7,9 and the MLPs "
 "compute the direction of the step. Layers 9-11 write the identity (one-hot) of the predicted answer into the "
 "final residual at the last comma; the logits are read from there."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    # ---- embedding stage: identity of each number token at its own position
    n = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        h = iv(nm, np.eye(128)[x[:, j].astype(int)])
        n.append(h.argmax(1).astype(float))
    # ---- layers 0-2: the identities are carried forward (computed from the returned values)
    m = []
    for j, nm in enumerate(["n1v4", "n2v4", "n3v4", "n4v4"]):
        h = iv(nm, np.eye(128)[n[j].astype(int)])
        m.append(h.argmax(1).astype(float))
    a1, a2, a3, a4 = m
    d1 = np.sign(a2 - a1); d2 = np.sign(a3 - a2); d3 = np.sign(a4 - a3)
    step = np.sign(d1 + d2 + d3)
    nxt = a4 + step
    # ---- layers 6-8 / 9-11: the answer identity appears at the last comma
    h9 = iv("ans9", np.eye(362)[np.clip(nxt.astype(int), 0, 361)])
    iv("n4v9", np.eye(128)[np.clip(a4.astype(int), 0, 127)])
    w = np.clip(h9.argmax(1), 0, 361)
    h12 = iv("ans_onehot", np.eye(362)[w])
    out = np.zeros((B, 362))
    out[np.arange(B), h12.argmax(1)] = 10.0
    return out

ALIGN = {
    "n1v":  ["resid0@n1"], "n2v": ["resid0@n2"], "n3v": ["resid0@n3"], "n4v": ["resid0@n4"],
    "n1v4": ["resid4@n1"], "n2v4": ["resid4@n2"], "n3v4": ["resid4@n3"], "n4v4": ["resid4@n4"],
    "ans9": ["resid9@end"], "n4v9": ["resid9@end"],
    "ans_onehot": ["resid12@end"],
}
