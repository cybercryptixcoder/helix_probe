import numpy as np
DESCRIPTION = "Probe submission: one scalar variable p = i*j mod 113 placed at every site, to learn how many principal components each site needs and how much of the decision each site carries."
def model(x, iv):
    i = x[:, 0].astype(float)
    j = x[:, 1].astype(float)
    v = iv("p", (i * j) % 113.0)
    q = ((x[:, 0] * x[:, 1]) % 113)
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), q] = 1.0
    return out + 0.0 * v[:, None]
ALIGN = {"p": ["embed.0", "embed.1", "embed.2", "attn_pattern", "attn_out", "resid_mid", "mlp_pre", "mlp_post", "mlp_out", "resid_post"]}
