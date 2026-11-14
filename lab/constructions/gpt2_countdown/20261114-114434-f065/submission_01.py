import numpy as np

K = 362  # number tokens ' 0' .. ' 361'

DESCRIPTION = (
 "GPT-2 small completes a run of four consecutive integers: it answers n4+1 after an increasing run "
 "and n4-1 after a decreasing one. Chain of the computation, stage by stage. "
 "EMBEDDING (resid0): the residual at a position is the token embedding plus the position embedding, "
 "so each position carries exactly the identity of its token. The four number positions therefore hold "
 "the one-hot identity of n1..n4 and positions 1-2 hold the prefix (4 possibilities); the <|endoftext|> "
 "and the four comma positions are the same token in every prompt, so their resid0 is constant and "
 "needs no variable. "
 "LAYERS 0-2 (resid3): early attention is local/previous-token, so the number identities stay at their "
 "own positions (a number position only ever sees the prefix and the numbers to its left, so a one-hot "
 "lookup of its own number explains its activation), and previous-token attention copies the last "
 "number n4 onto the final comma. Hence resid3 holds one-hot identities at n1..n4, a copy of n4 at the "
 "end position, and the first sign of the direction of the run (n2-n1) at the end position. "
 "LAYERS 3-5 (resid6): the end position combines n4 with the direction and writes the successor number "
 "n4+dir as a token identity, so resid6 carries the one-hot answer at the last position, while the "
 "number identities remain available at n1..n4. "
 "LAYERS 6-8 (resid9): the answer identity is carried at the last position (and the numbers are still "
 "readable at their positions). "
 "LAYERS 9-11 (resid12): the answer identity is sharpened into the final residual at the last token, "
 "and ln_f + W_U read it out as the answer token; only the last position matters for the logits. "
 "model() replays this causal chain: token identities -> direction dir = sign(n2-n1) (with "
 "sign(n4-n3) as fallback) -> answer = n4+dir -> one-hot answer carried to the output; the output "
 "logits put a large value on the predicted number token."
)

ALIGN = {
    # embedding
    "prefix_e": ["resid0@1", "resid0@2"],
    "n1_e": ["resid0@n1"],
    "n2_e": ["resid0@n2"],
    "n3_e": ["resid0@n3"],
    "n4_e": ["resid0@n4"],
    # layers 0-2
    "n1_a": ["resid3@n1"],
    "n2_a": ["resid3@n2"],
    "n3_a": ["resid3@n3"],
    "n4_a": ["resid3@n4"],
    "n4ea": ["resid3@end"],
    "dir_a": ["resid3@end"],
    # layers 3-5
    "n1_b": ["resid6@n1"],
    "n2_b": ["resid6@n2"],
    "n3_b": ["resid6@n3"],
    "n4_b": ["resid6@n4"],
    "ans_b": ["resid6@end"],
    # layers 6-8
    "n1_c": ["resid9@n1"],
    "n2_c": ["resid9@n2"],
    "n3_c": ["resid9@n3"],
    "n4_c": ["resid9@n4"],
    "ans_c": ["resid9@end"],
    # layers 9-11
    "ans_d": ["resid12@end"],
}


def _idx(v):
    return np.asarray(v).argmax(axis=1)


def _onehot(i):
    return np.eye(K)[np.asarray(i, dtype=int)]


def _dir_sign(a, b, c, d):
    s = np.sign(np.asarray(b, dtype=float) - np.asarray(a, dtype=float))
    s2 = np.sign(np.asarray(d, dtype=float) - np.asarray(c, dtype=float))
    s = np.where(s == 0, s2, s)
    return np.where(s > 0, 1.0, -1.0)


def model(x, iv):
    x = np.asarray(x, dtype=int)
    if x.ndim == 1:
        x = x[None, :]
    n1, n2, n3, n4, pf = x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4]

    # ---------------- embedding stage (resid0)
    P  = iv("prefix_e", np.eye(4)[pf])
    E1 = iv("n1_e", _onehot(n1))
    E2 = iv("n2_e", _onehot(n2))
    E3 = iv("n3_e", _onehot(n3))
    E4 = iv("n4_e", _onehot(n4))
    i1, i2, i3, i4 = _idx(E1), _idx(E2), _idx(E3), _idx(E4)

    # ---------------- resid3: layers 0-2
    A1 = iv("n1_a", _onehot(i1))
    A2 = iv("n2_a", _onehot(i2))
    A3 = iv("n3_a", _onehot(i3))
    A4 = iv("n4_a", _onehot(i4))
    AE = iv("n4ea",  _onehot(i4))            # copy of n4 on the final comma
    j1, j2, j3, j4 = _idx(A1), _idx(A2), _idx(A3), _idx(A4)
    sd = _dir_sign(j1, j2, j3, j4)
    DA = iv("dir_a", np.stack([(sd > 0).astype(float), (sd < 0).astype(float)], axis=1))
    s = np.where(np.asarray(DA)[:, 0] >= 0.5, 1.0, -1.0)

    # ---------------- resid6: layers 3-5
    B1 = iv("n1_b", _onehot(j1))
    B2 = iv("n2_b", _onehot(j2))
    B3 = iv("n3_b", _onehot(j3))
    B4 = iv("n4_b", _onehot(j4))
    k1, k2, k3, k4 = _idx(B1), _idx(B2), _idx(B3), _idx(B4)
    ansB = iv("ans_b", _onehot(np.clip(np.round(k4 + s).astype(int), 0, K - 1)))

    # ---------------- resid9: layers 6-8
    C1 = iv("n1_c", _onehot(k1))
    C2 = iv("n2_c", _onehot(k2))
    C3 = iv("n3_c", _onehot(k3))
    C4 = iv("n4_c", _onehot(k4))
    ansC = iv("ans_c", _onehot(_idx(ansB)))

    # ---------------- resid12: layers 9-11
    ansD = iv("ans_d", _onehot(_idx(ansC)))
    return 20.0 * np.asarray(ansD, dtype=float)
