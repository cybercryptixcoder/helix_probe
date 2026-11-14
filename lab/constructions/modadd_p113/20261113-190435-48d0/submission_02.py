
import numpy as np
DESCRIPTION = "Network computes (i + j) mod 113 for input [i, j, 113]. embed.2 is a constant vector (token 113 + position 2 embedding). Output is a one-hot at (i+j) mod 113."
def model(x, iv):
    one = iv("const2", np.ones((x.shape[0], 1)))
    s = (x[:, 0] + x[:, 1]) % 113
    out = -np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), s] = 100.0
    return out
ALIGN = {"const2": ["embed.2"]}
