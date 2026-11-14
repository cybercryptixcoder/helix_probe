
import numpy as np
DESCRIPTION = ("Input [i, j, '='] -> class (i+j) mod 113. Token n is embedded as cos/sin of 2*pi*k*n/113 for "
 "k in {8,11,22,23,25}; attention brings i and j to the last position; the MLP forms cos/sin of the sum by "
 "angle addition (these live in resid_post); the unembedding is a Fourier readout at the same freqs: "
 "logits[c] = G[0] + sum_k G[2k-1] cos(kc) + G[2k] sin(kc), where G is an affine function of cos/sin of k(i+j) "
 "(measured 11x11 matrix, argmax correct on all 12769 inputs).")
FR = [8, 11, 22, 23, 25]
def feats(n):
    n = np.asarray(n, dtype=float)
    return np.stack(sum(([np.cos(2*np.pi*k*n/113.0), np.sin(2*np.pi*k*n/113.0)] for k in FR), []), 1)
M = np.array([[1,0,0,0,0,0,0,0,0,0,0],
     [6.524,9.976,-1.351,0.539,0.122,-0.306,-0.084,-0.897,-0.042,0.057,0.724],
     [0.512,-1.313,15.09,0.034,0.562,0.023,0.006,0.252,-0.834,0.695,0.251],
     [-0.886,0.207,-0.081,6.046,0.073,0.194,-0.021,0.482,0.132,-0.379,-0.18],
     [0.546,0.011,0.402,0.073,6.291,0.082,0.051,0.029,0.157,-0.233,-0.327],
     [-0.052,-0.095,-0.041,-0.042,0.009,0.254,0.087,0.007,0.028,-0.127,-0.021],
     [0.074,0.065,-0.12,-0.148,0.018,0.078,0.321,0.02,0.01,-0.029,-0.068],
     [4.331,-0.905,0.151,0.473,-0.056,-0.222,-0.243,9.481,1.039,-0.125,-0.114],
     [1.595,-0.362,-0.917,0.177,0.288,0.152,-0.139,1.089,10.124,0.175,0.018],
     [0.63,-0.171,0.608,-0.397,-0.228,-0.082,-0.071,-0.312,0.102,7.326,0.214],
     [-1.707,0.766,0.237,-0.199,-0.267,0.068,-0.177,0.188,-0.003,0.104,6.012],
     [-42.059,-3.783,-0.877,-1.181,-0.538,0.823,0.089,-2.639,-1.047,-1.345,2.029]])
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    fi = iv("fi", feats(i)); fj = iv("fj", feats(j))
    ci, si = fi[:, 0::2], fi[:, 1::2]
    cj, sj = fj[:, 0::2], fj[:, 1::2]
    sfun = iv("sfun", np.concatenate([ci*cj - si*sj, si*cj + ci*sj], 1))
    G = np.concatenate([sfun, np.ones((x.shape[0], 1))], 1) @ M
    c = np.arange(113)
    cols = [np.ones(113)]
    for k in FR:
        cols += [np.cos(2*np.pi*k*c/113.0), np.sin(2*np.pi*k*c/113.0)]
    return G @ np.stack(cols, 1)
ALIGN = {"fi": ["embed.0"], "fj": ["embed.1"], "sfun": ["resid_post"]}
