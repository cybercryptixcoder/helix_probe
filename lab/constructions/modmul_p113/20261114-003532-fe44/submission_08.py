import numpy as np
DESCRIPTION = "Probe: p = i*j mod 113 placed at the post-MLP sites."
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    p = iv("p", (i * j) % 113.0)
    q = ((x[:, 0] * x[:, 1]) % 113)
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), q] = 1.0
    return out + 0.0 * p[:, None]
ALIGN = {"p": ["mlp_post", "mlp_out", "resid_post"]}
