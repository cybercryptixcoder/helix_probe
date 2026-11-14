
import numpy as np
DESCRIPTION = "Network computes (i + j) mod 113 where the input is [i, j, 113]. Rough first pass: output is a one-hot at the sum."
def model(x, iv):
    s = (x[:, 0] + x[:, 1]) % 113
    out = -np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), s] = 100.0
    return out
ALIGN = {}
