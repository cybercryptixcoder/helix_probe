
import numpy as np
DESCRIPTION = ("Input [i, j, '='] -> class (i+j) mod 113. Token n is embedded as cos/sin of 2*pi*k*n/113 for "
 "k in {8,11,22,23,25} (8 of 128 dims); attention brings i and j to the last position; the MLP forms cos/sin of "
 "the sum by angle addition (these live in resid_post; mlp_out alone already gives the right class, resid_mid "
 "alone does not); the unembedding is a Fourier readout at the same freqs: logits[c] = G[0] + sum_k G[2k-1] "
 "cos(kc) + G[2k] sin(kc), where G is affine in cos/sin of k(i+j) (measured 11x11 matrix).")
FR = [8, 11, 22, 23, 25]
def feats(n):
    n = np.asarray(n, dtype=float)
    return np.stack(sum(([np.cos(2*np.pi*k*n/113.0), np.sin(2*np.pi*k*n/113.0)] for k in FR), []), 1)
M = np.array([[-42.06,-3.78,-0.88,-1.18,-0.54,0.82,0.09,-2.64,-1.05,-1.35,2.03],
 [6.52,9.98,-1.35,0.54,0.12,-0.31,-0.08,-0.9,-0.04,0.06,0.72],
 [0.51,-1.31,15.09,0.03,0.56,0.02,0.01,0.25,-0.83,0.69,0.25],
 [-0.89,0.21,-0.08,6.05,0.07,0.19,-0.02,0.48,0.13,-0.38,-0.18],
 [0.55,0.01,0.4,0.07,6.29,0.08,0.05,0.03,0.16,-0.23,-0.33],
 [-0.05,-0.09,-0.04,-0.04,0.01,0.25,0.09,0.01,0.03,-0.13,-0.02],
 [0.07,0.06,-0.12,-0.15,0.02,0.08,0.32,0.02,0.01,-0.03,-0.07],
 [4.33,-0.91,0.15,0.47,-0.06,-0.22,-0.24,9.48,1.04,-0.13,-0.11],
 [1.59,-0.36,-0.92,0.18,0.29,0.15,-0.14,1.09,10.12,0.18,0.02],
 [0.63,-0.17,0.61,-0.4,-0.23,-0.08,-0.07,-0.31,0.1,7.33,0.21],
 [-1.71,0.77,0.24,-0.2,-0.27,0.07,-0.18,0.19,0.0,0.1,6.01]])
c = np.arange(113)
COLS = np.stack([np.ones(113)] + sum(([np.cos(2*np.pi*k*c/113.0), np.sin(2*np.pi*k*c/113.0)] for k in FR), []), 1)
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    fi = iv("fi", feats(i)); fj = iv("fj", feats(j))
    ci, si = fi[:, 0::2], fi[:, 1::2]
    cj, sj = fj[:, 0::2], fj[:, 1::2]
    cs = ci*cj - si*sj; ss = si*cj + ci*sj
    sf = np.empty((x.shape[0], 10)); sf[:, 0::2] = cs; sf[:, 1::2] = ss
    sfun = iv("sfun", sf)
    G = np.concatenate([np.ones((x.shape[0], 1)), sfun], 1) @ M
    return G @ COLS.T
ALIGN = {"fi": ["embed.0"], "fj": ["embed.1"], "sfun": ["resid_post"]}

