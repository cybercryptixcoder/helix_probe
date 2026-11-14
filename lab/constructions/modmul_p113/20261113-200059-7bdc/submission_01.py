import numpy as np

DESCRIPTION = """The network computes (i*j) mod 113 from input [i, j, 113]; output argmax is that class.
First submission: behaviour only, computed directly from the two token ids."""

def model(x, iv):
    i = iv("i", x[:, 0].astype(np.float64))
    j = iv("j", x[:, 1].astype(np.float64))
    prod = iv("prod", np.mod(i * j, 113.0))
    B = x.shape[0]
    K = 113
    onehot = (prod[:, None] == np.arange(K)[None, :]).astype(np.float64)
    return 10.0 * onehot - 0.01 * (1 - onehot)

ALIGN = {}
