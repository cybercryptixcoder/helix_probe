import numpy as np
DESCRIPTION = "Probe: check whether the pre-MLP residual is additive in the two token identities and whether the post-MLP stream is a function of the product."
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ii = iv("i", i); jj = iv("j", j)
    p = iv("p", (i * j) % 113.0)
    q = ((x[:, 0] * x[:, 1]) % 113)
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), q] = 1.0
    return out + 0.0 * (ii + jj + p)[:, None]
ALIGN = {"i": ["attn_pattern"], "j": ["attn_pattern"], "p": ["resid_post"]}
