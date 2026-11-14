import numpy as np
DESCRIPTION = "Network computes (i*j) mod 113 from tokens (i, j, 113) at the last position."
def model(x, iv):
    i = x[:, 0]
    j = x[:, 1]
    p = (i * j) % 113
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), p] = 1.0
    return out
ALIGN = {}
