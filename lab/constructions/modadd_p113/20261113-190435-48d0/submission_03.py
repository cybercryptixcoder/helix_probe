
import numpy as np, math
DESCRIPTION = ("Network computes (i+j) mod 113 for input [i,j,113]. The last-position residual stream after the MLP "
 "carries the answer in a rank-8 Fourier code: for s=(i+j) mod 113 it holds cos/sin of 2*pi*k*s/113 for k in {8,11,23,25}. "
 "The unembedding reads these out, giving logits that peak at class s. Here each frequency pair is its own 2-dim variable; "
 "the output adds 5*cos(2*pi*k*(s_k - c)/113) over the four frequencies, where s_k is recovered from the k-th pair.")
FREQ = [8.0, 11.0, 23.0, 25.0]

def model(x, iv):
    s = (x[:, 0] + x[:, 1]) % 113
    B = x.shape[0]
    ang = np.stack([2*np.pi*k*s/113.0 for k in FREQ], 1)
    cs = iv("cos_k", np.cos(ang))       # [B,4]
    sn = iv("sin_k", np.sin(ang))       # [B,4]
    c = np.arange(113)[None, :]
    out = np.full((B, 113), -30.0)
    for j, k in enumerate(FREQ):
        T = (np.arctan2(sn[:, j], cs[:, j]) * 113.0 / (2*np.pi*k)) % 113.0
        out = out + 5.0*np.cos(2*np.pi*k*(T[:, None] - c)/113.0)
    return out
ALIGN = {"cos_k": ["resid_post", "mlp_out"], "sin_k": ["resid_post", "mlp_out"]}
