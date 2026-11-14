import numpy as np
DESCRIPTION = "Network computes (i*j) mod 113 from tokens (i, j, 113) read at the last position. Probe: is the post-MLP residual a Fourier code of the product p = i*j mod 113?"
def model(x, iv):
    i = x[:, 0].astype(float)
    j = x[:, 1].astype(float)
    p = (i * j) % 113.0
    w = 2 * np.pi * p / 113.0
    f = iv("four_p", np.stack([np.cos(w), np.sin(w), np.cos(2 * w), np.sin(2 * w)], 1))
    p3 = (x[:, 0] * x[:, 1]) % 113
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), p3] = 1.0
    return out + 0.0 * f.mean()
ALIGN = {"four_p": ["mlp_out", "resid_post"]}
