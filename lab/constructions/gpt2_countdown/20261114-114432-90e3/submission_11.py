
import numpy as np

DESCRIPTION = (
    "The four numbers are in arithmetic progression; the model predicts the next term: "
    "answer = n4 + sign(step) with step from the adjacent differences. The prefix is irrelevant. "
    "Embedding (resid0): the four number positions carry each number token's identity (one-hot). "
    "Layers 3-5 (resid4): the same identities at the number positions. "
    "Layers 6-8 (resid9): the last comma already carries the identity of the answer. "
    "Layers 9-11 (resid10, resid12): the answer identity at the last comma, read out by the "
    "unembedding."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    K1 = 128
    ns = []
    for j, nm in enumerate(["n1v", "n2v", "n3v", "n4v"]):
        ns.append(iv(nm, np.eye(K1)[x[:, j].astype(int)]).argmax(1).astype(float))
    n1, n2, n3, n4 = ns
    ns2 = []
    for j, nm in enumerate(["n1v4", "n2v4", "n3v4", "n4v4"]):
        ns2.append(iv(nm, np.eye(K1)[ns[j].astype(int)]).argmax(1).astype(float))
    m1, m2, m3, m4 = ns2
    d1 = np.sign(m2 - m1); d2 = np.sign(m3 - m2); d3 = np.sign(m4 - m3)
    step = iv("step", np.sign(d1 + d2 + d3))
    nxt = m4 + step
    ans = np.eye(362)[np.clip(nxt.astype(int), 0, 361)]
    a9 = iv("ans9", ans)
    a10 = iv("ans10", a9)
    a12 = iv("ans_onehot", a10)
    out = np.zeros((B, 362))
    out[np.arange(B), a12.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid12@end"],
    "ans10": ["resid10@end"],
    "ans9": ["resid9@end"],
    "n1v": ["resid0@n1"], "n2v": ["resid0@n2"], "n3v": ["resid0@n3"], "n4v": ["resid0@n4"],
    "n1v4": ["resid4@n1"], "n2v4": ["resid4@n2"], "n3v4": ["resid4@n3"], "n4v4": ["resid4@n4"],
}
