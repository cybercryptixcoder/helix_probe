
import numpy as np

DESCRIPTION = """
Input [i, j, 113]: token 113 is a readout marker at the last position; the network outputs
t = (i + j) mod 113. The answer is coded in the last-position residual stream as a small set
of Fourier modes of t: the ablation/DFT analysis shows the readout sites' input-dependence is
dominated by frequencies k = 8, 23, 25, 11 (of the 113-cycle). So the readout variables are
cos/sin of 2*pi*k*t/113 for k in {8, 23, 25, 11}; the unembedding turns them into logits
peaked at class t.
"""

FREQS = (8, 23, 25, 11)

def model(x, iv):
    i = x[:, 0]
    j = x[:, 1]
    t = (i + j) % 113
    ang = 2.0 * np.pi * t / 113.0
    kk = np.arange(113)[None, :]
    a = 2.0 * np.pi * kk / 113.0
    logits = 0.0
    for k in FREQS:
        c = iv("c%d" % k, np.cos(k * ang))
        s = iv("s%d" % k, np.sin(k * ang))
        logits = logits + c[:, None] * np.cos(k * a) + s[:, None] * np.sin(k * a)
    return logits

ALIGN = {}
for k in FREQS:
    ALIGN["c%d" % k] = ["resid_post", "mlp_out"]
    ALIGN["s%d" % k] = ["resid_post", "mlp_out"]
