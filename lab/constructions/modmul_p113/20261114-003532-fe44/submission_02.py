import numpy as np
DESCRIPTION = "Network computes (i*j) mod 113 from tokens (i, j, 113) at the last position. First probe: Fourier(1) features of i and j at the embedding sites."
def model(x, iv):
    i = x[:, 0].astype(float)
    j = x[:, 1].astype(float)
    w = 2 * np.pi / 113.0
    fi = iv("fi", np.stack([np.cos(w * i), np.sin(w * i)], 1))
    fj = iv("fj", np.stack([np.cos(w * j), np.sin(w * j)], 1))
    p = (x[:, 0] * x[:, 1]) % 113
    out = -1.0 * np.ones((x.shape[0], 113))
    out[np.arange(x.shape[0]), p] = 1.0
    return out + 0.0 * fi.mean() + 0.0 * fj.mean()
ALIGN = {"fi": ["embed.0"], "fj": ["embed.1"]}
