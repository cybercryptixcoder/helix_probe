import numpy as np

K = 362
EYE = np.eye(K, dtype=np.float64)
EYE4 = np.eye(4, dtype=np.float64)

DESCRIPTION = (
    "Continuing a run of consecutive integers. The four number tokens are held as token identities "
    "(one-hot of the number) at their own positions from the embedding onward; the prefix (4 kinds) is a "
    "4-way one-hot at the two prefix token positions 1 and 2. <|endoftext|>, the three commas and the final "
    "comma are identical in every prompt, so they need no variable. Blocks 0-2 copy the last number into the "
    "end position (the final comma): resid3@end holds the identity of n4 together with the single scalar "
    "s = sign(n4-n3), the direction of the run. Blocks 3-5 and 6-8 keep that state at the end position and "
    "keep the numbers at their own token positions. Blocks 9-11 add s to n4 and write the identity of the "
    "answer token n4+s into the final residual resid12@end, which the last LayerNorm and the unembedding turn "
    "into a peak on that number."
)


def model(x, iv):
    x = np.asarray(x, dtype=np.int64)
    n1 = np.clip(x[:, 0], 0, K - 1)
    n2 = np.clip(x[:, 1], 0, K - 1)
    n3 = np.clip(x[:, 2], 0, K - 1)
    n4 = np.clip(x[:, 3], 0, K - 1)
    pf = np.clip(x[:, 4], 0, 3)

    # ---------------- stage 0 : embedding (resid0) ----------------
    num_n1 = iv("num_n1", EYE[n1])
    num_n2 = iv("num_n2", EYE[n2])
    num_n3 = iv("num_n3", EYE[n3])
    num_n4 = iv("num_n4", EYE[n4])
    pfx    = iv("pfx", EYE4[pf])

    # ---------------- stage 1 : blocks 0-2 (resid3) ---------------
    v3 = num_n3.argmax(1)
    v4 = num_n4.argmax(1)
    s0 = np.sign(v4 - v3).astype(np.float64)
    end_n4_l3 = iv("end_n4_l3", num_n4)
    sgn_l3    = iv("sgn_l3", s0)

    # ---------------- stage 2 : blocks 3-5 (resid6) ---------------
    end_n4_l6 = iv("end_n4_l6", end_n4_l3)
    sgn_l6    = iv("sgn_l6", sgn_l3)

    # ---------------- stage 3 : blocks 6-8 (resid9) ---------------
    end_n4_l9 = iv("end_n4_l9", end_n4_l6)
    sgn_l9    = iv("sgn_l9", sgn_l6)

    # ---------------- stage 4 : blocks 9-11 (resid12) ------------
    last = end_n4_l9.argmax(1)
    step = np.sign(sgn_l9).astype(np.int64)
    ans  = np.clip(last + step, 0, K - 1)
    ansh = iv("answer", EYE[ans])

    peak = ansh.argmax(1)
    logits = 8.0 * ansh - 0.002 * np.abs(np.arange(K)[None, :] - peak[:, None])
    return logits


ALIGN = {
    "num_n1":    ["resid0@n1", "resid3@n1", "resid6@n1"],
    "num_n2":    ["resid0@n2", "resid3@n2", "resid6@n2"],
    "num_n3":    ["resid0@n3", "resid3@n3", "resid6@n3", "resid9@n3"],
    "num_n4":    ["resid0@n4", "resid3@n4", "resid6@n4", "resid9@n4"],
    "pfx":       ["resid0@1", "resid0@2"],
    "end_n4_l3": ["resid3@end"],
    "sgn_l3":    ["resid3@end"],
    "end_n4_l6": ["resid6@end"],
    "sgn_l6":    ["resid6@end"],
    "end_n4_l9": ["resid9@end"],
    "sgn_l9":    ["resid9@end"],
    "answer":    ["resid12@end"],
}
