
import numpy as np

DESCRIPTION = """
The network computes (i+j) mod 113 where input is [i, j, 113]. The last-position residual
(mlp_out / resid_post) carries a smooth (Fourier) code of the answer t=(i+j) mod 113; the
unembedding turns that code into logits peaked at class t. First-stage guess: variables are
low-frequency Fourier features of t placed at the readout sites.
"""

def model(x, iv):
    i = x[:, 0]
    j = x[:, 1]
    t = (i + j) % 113
    ang = 2.0 * np.pi * t / 113.0
    c1 = iv("c1", np.cos(ang))
    s1 = iv("s1", np.sin(ang))
    c2 = iv("c2", np.cos(2 * ang))
    s2 = iv("s2", np.sin(2 * ang))
    c3 = iv("c3", np.cos(3 * ang))
    s3 = iv("s3", np.sin(3 * ang))
    # logits: peaked at class t
    k = np.arange(113)[None, :]
    logits = (c1[:, None] * np.cos(2 * np.pi * k / 113.0)
              + s1[:, None] * np.sin(2 * np.pi * k / 113.0)
              + c2[:, None] * np.cos(4 * np.pi * k / 113.0)
              + s2[:, None] * np.sin(4 * np.pi * k / 113.0)
              + c3[:, None] * np.cos(6 * np.pi * k / 113.0)
              + s3[:, None] * np.sin(6 * np.pi * k / 113.0))
    return logits

ALIGN = {"c1": ["mlp_out", "resid_post"], "s1": ["mlp_out", "resid_post"],
         "c2": ["mlp_out", "resid_post"], "s2": ["mlp_out", "resid_post"],
         "c3": ["mlp_out", "resid_post"], "s3": ["mlp_out", "resid_post"]}
