
import numpy as np

DESCRIPTION = (
    "Four numbers in arithmetic progression; the model predicts the next term: "
    "answer = n4 + sign(step). The prefix is irrelevant. Embedding (resid0) and layers 3-5 "
    "(resid4): the number positions carry each number token's identity (one-hot). Layers 9-11: "
    "the last comma holds the identity of the answer (one-hot) at resid10 and resid12; the "
    "unembedding reads it out. Layers 6-8: diagnostic attempt with the answer identity at resid9."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    K1 = 128
    ns = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        ns.append(iv(nm, np.eye(K1)[x[:, j].astype(int)]).argmax(1).astype(float))
    n1, n2, n3, n4 = ns
    for j, nm in enumerate(["n1v4", "n2v4", "n3v4", "n4v4"]):
        iv(nm, np.eye(K1)[x[:, j].astype(int)])
    d1 = np.sign(n2 - n1); d2 = np.sign(n3 - n2); d3 = np.sign(n4 - n3)
    step = iv("step", np.sign(d1 + d2 + d3))
    nxt = iv("next", n4 + step)
    ans = np.eye(362)[np.clip(nxt.astype(int), 0, 361)]
    a9 = iv("ans9", ans); iv("ans10", a9); iv("ans_onehot", a9)
    out = np.zeros((B, 362))
    out[np.arange(B), a9.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid12@end"],
    "ans10": ["resid10@end"],
    "ans9": ["resid9@end"],
    "n1v": ["resid0@n1"], "n2v": ["resid0@n2"], "n3v": ["resid0@n3"], "n4v": ["resid0@n4"],
    "n1v4": ["resid4@n1"], "n2v4": ["resid4@n2"], "n3v4": ["resid4@n3"], "n4v4": ["resid4@n4"],
}
