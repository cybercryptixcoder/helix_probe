import numpy as np

DESCRIPTION = """The network computes (i*j) mod 113 from [i, j, 113] and reads the answer out at the last position.
The MLP output looks like a function of the product alone (89% of its variance is between-product),
so the readout stage is modelled as a Fourier code of the product class."""

def model(x, iv):
    i = iv("i", x[:, 0].astype(np.float64))
    j = iv("j", x[:, 1].astype(np.float64))
    prod = iv("prod", np.mod(i * j, 113.0))
    th = 2 * np.pi * prod / 113.0
    c1 = iv("cos1", np.cos(th))
    s1 = iv("sin1", np.sin(th))
    B = x.shape[0]
    K = 113
    onehot = (prod[:, None] == np.arange(K)[None, :]).astype(np.float64)
    return 10.0 * onehot - 0.01 * (1 - onehot)

ALIGN = {"cos1": ["mlp_out", "resid_post"], "sin1": ["mlp_out", "resid_post"]}
