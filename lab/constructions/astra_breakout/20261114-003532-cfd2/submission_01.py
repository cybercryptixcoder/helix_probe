
import numpy as np
DESCRIPTION = """
Rough first pass. The network is a cascade that only uses a handful of hidden units:
W1 has nonzero entries only in columns 0..5 (h1 units 6..31 are dead, b1 = 0 except b1[5]=5).
Units 4 and 5 of h1 have enormous weight norms (~1500, ~745) so they are essentially sign/saturating
functions of linear combinations of the input; units 0..3 have unit-scale weights (small linear maps).
W2 has nonzero rows only 0..5 and nonzero columns only 0..7, b2 = -415 on units 0..7 (so h2 units 8..31 = tanh(-415) = -1).
W3 puts weight 30 on h2 units 0,2,4,6 into output 1 and on h2 units 1,3,5,7 into output 3, and is zero elsewhere;
b3 = [0, 90, -100, 90, -100, -100], so out0 = 0, out2 = out4 = out5 = -100 are constants and the decision is
between out1 and out3.
Inputs are 0/1 in blocks of 6 (100 blocks); the used input positions are residues 3 and 4 of each block, paired.
This file only guesses the h1 saturating units; the rest is placeholder.
"""
def model(x, iv):
    idx3 = np.arange(3, 600, 6)
    idx4 = np.arange(4, 600, 6)
    k = np.arange(100, dtype=float)
    ramp = 20.0 * k
    pre4 = (x[:, idx3] * ramp).sum(1) - (x[:, idx4] * ramp).sum(1)
    u4 = iv("u4", np.tanh(pre4))
    pre5 = 10.0 * (x[:, idx3][:, 10:].sum(1) - x[:, idx4][:, 10:].sum(1)) + 5.0
    u5 = iv("u5", np.tanh(pre5))
    # placeholders for the rest of the cascade
    h2 = iv("h2a", u4[:, None] * np.ones(8))
    s_even = h2[:, 0::2].sum(1)
    s_odd = h2[:, 1::2].sum(1)
    out = np.stack([0 * s_even, 30 * s_even + 90, -100 + 0 * s_even,
                    30 * s_odd + 90, -100 + 0 * s_even, -100 + 0 * s_even], 1)
    return out
ALIGN = {"u4": ["h1"], "u5": ["h1"], "h2a": ["h2"]}
