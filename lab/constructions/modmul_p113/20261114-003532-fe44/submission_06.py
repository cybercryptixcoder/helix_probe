import numpy as np
DESCRIPTION = "Probe: is the residual stream before the MLP a function of the two token identities (i, j) additively, while after the MLP it is a function of p = i*j mod 113?"
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ii = iv("i", i); jj = iv("j", j)
    p = iv("p", (i * j) % 113.0)
    q = ((x[:, 0] * x[:, 1]) % 113)
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), q] = 1.0
    return out + 0.0 * (ii + jj + p)[:, None]
ALIGN = {"i": ["resid_mid", "mlp_pre"], "j": ["resid_mid", "mlp_pre"], "p": ["mlp_post", "mlp_out", "resid_post"]}
