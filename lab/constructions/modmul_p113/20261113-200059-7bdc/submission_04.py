import numpy as np

DESCRIPTION = """The network computes (i*j) mod 113 from [i, j, 113] and reads it out at the last position.
Measured facts: resid_mid is 96.6% an additive function mu + f(i) + f(j) with the SAME 8-dim f at both
positions; the MLP output mlp_out is 89% a function of the product class alone, and that function is
generic in the class (needs the full Fourier basis), i.e. a per-class code. This submission names that
per-class code (one-hot of the product) at the two readout sites."""

def model(x, iv):
    i = iv("i", x[:, 0].astype(np.float64))
    j = iv("j", x[:, 1].astype(np.float64))
    prod = iv("prod", np.mod(i * j, 113.0))
    K = 113
    oh = iv("onehot_prod", (prod[:, None] == np.arange(K)[None, :]).astype(np.float64))
    prod2 = iv("prod2", np.argmax(oh, axis=1).astype(np.float64))
    onehot = (prod2[:, None] == np.arange(K)[None, :]).astype(np.float64)
    return 10.0 * onehot - 0.01 * (1 - onehot)

ALIGN = {"onehot_prod": ["mlp_out", "resid_post"]}
