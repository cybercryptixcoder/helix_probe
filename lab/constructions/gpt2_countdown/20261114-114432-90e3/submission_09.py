
import numpy as np

DESCRIPTION = (
    "Four numbers in arithmetic progression; the model predicts the next term: "
    "answer = n4 + sign(step), step from the adjacent differences. The prefix is irrelevant. "
    "Embedding (resid0) and layers 0-2 (resid1): the number positions carry each number token's "
    "identity (one-hot). Layers 3-5 (resid4): same identities at the number positions. "
    "Layers 6-8 (resid7): number identities at the number positions plus the sign of the step "
    "(2-way one-hot) at the last comma. Layers 9-11 (resid10 and resid12): the last comma holds "
    "the identity of the answer (one-hot) which the unembedding reads out."
)

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    K1 = 128
    h = iv("n1v", np.eye(K1)[x[:, 0].astype(int)]); n1 = h.argmax(1).astype(float)
    h = iv("n2v", np.eye(K1)[x[:, 1].astype(int)]); n2 = h.argmax(1).astype(float)
    h = iv("n3v", np.eye(K1)[x[:, 2].astype(int)]); n3 = h.argmax(1).astype(float)
    h = iv("n4v", np.eye(K1)[x[:, 3].astype(int)]); n4 = h.argmax(1).astype(float)
    for nm, j in [("n1v1", 0), ("n2v1", 1), ("n3v1", 2), ("n4v1", 3),
                  ("n1v4", 0), ("n2v4", 1), ("n3v4", 2), ("n4v4", 3),
                  ("n1v7", 0), ("n2v7", 1), ("n3v7", 2), ("n4v7", 3)]:
        iv(nm, np.eye(K1)[x[:, j].astype(int)])
    st = iv("stepv7", np.eye(2)[(np.sign(n2 - n1) > 0).astype(int)])
    d1 = np.sign(n2 - n1); d2 = np.sign(n3 - n2); d3 = np.sign(n4 - n3)
    step = iv("step", np.sign(d1 + d2 + d3))
    nxt = iv("next", n4 + step)
    del st
    ans = iv("ans10", np.eye(362)[np.clip(nxt.astype(int), 0, 361)])
    ans2 = iv("ans_onehot", ans)
    out = np.zeros((B, 362))
    out[np.arange(B), ans2.argmax(1)] = 10.0
    return out

ALIGN = {
    "ans_onehot": ["resid12@end"],
    "ans10": ["resid10@end"],
    "n1v": ["resid0@n1"], "n2v": ["resid0@n2"], "n3v": ["resid0@n3"], "n4v": ["resid0@n4"],
    "n1v1": ["resid1@n1"], "n2v1": ["resid1@n2"], "n3v1": ["resid1@n3"], "n4v1": ["resid1@n4"],
    "n1v4": ["resid4@n1"], "n2v4": ["resid4@n2"], "n3v4": ["resid4@n3"], "n4v4": ["resid4@n4"],
    "n1v7": ["resid7@n1"], "n2v7": ["resid7@n2"], "n3v7": ["resid7@n3"], "n4v7": ["resid7@n4"],
    "stepv7": ["resid7@end"],
}
