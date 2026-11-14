
import numpy as np
DESCRIPTION = ("Network computes (i+j) mod 113. The last-position residual after the MLP holds a rank-8 Fourier code of "
 "s=(i+j) mod 113: cos/sin of 2*pi*k*s/113, k in {8,11,23,25}. The unembedding reads it out, so logits peak at class s. "
 "Each frequency pair is its own 2-dim variable; the output adds 5*cos(2*pi*k*(s_k-c)/113) over the four frequencies, "
 "s_k recovered from the k-th pair. Probing the same code at earlier sites.")
FREQ = [8.0, 11.0, 23.0, 25.0]
def model(x, iv):
    s = (x[:, 0] + x[:, 1]) % 113
    B = x.shape[0]
    cs = iv("cos_k", np.cos(np.stack([2*np.pi*k*s/113.0 for k in FREQ], 1)))
    sn = iv("sin_k", np.sin(np.stack([2*np.pi*k*s/113.0 for k in FREQ], 1)))
    c = np.arange(113)[None, :]
    out = np.full((B, 113), -30.0)
    for q, k in enumerate(FREQ):
        T = (np.arctan2(sn[:, q], cs[:, q]) * 113.0 / (2*np.pi*k)) % 113.0
        out = out + 5.0*np.cos(2*np.pi*k*(T[:, None] - c)/113.0)
    return out
ALIGN = {"cos_k": ["mlp_out", "resid_post", "mlp_post", "mlp_pre", "resid_mid", "attn_out"],
         "sin_k": ["mlp_out", "resid_post", "mlp_post", "mlp_pre", "resid_mid", "attn_out"]}
