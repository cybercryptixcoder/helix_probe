
import numpy as np, math
DESCRIPTION = ("Task: s=(i+j) mod 113 from tokens [i, j, 113]. Token embeddings are Fourier codes of the token id: "
 "W_E[t] = sum_k a_k cos(2pi k t/113) + b_k sin(2pi k t/113) with k in {8,11,23,25} plus harmonics (16,22,46,50). "
 "The last token's query gives each head a score for pos0 that depends only on i (and the same function of j for pos1), so the "
 "attention weights are softmax(f_h(i), f_h(j), const). The attention output at the last position is a mixture of the two Fourier-coded "
 "value vectors; the MLP's relu turns the mixture into products, i.e. cos/sin of k(i+j) and k(i-j). The readout scores class c by how "
 "well its own Fourier code (same frequencies) matches those sum features, so the argmax is at c = (i+j) mod 113.")
P = 113.0
KS = [8.0, 11.0, 23.0, 25.0]
def cs(t, ks):
    t = np.asarray(t, dtype=float)
    return np.concatenate([np.cos(2*np.pi*k*t/P)[:, None] for k in ks] +
                          [np.sin(2*np.pi*k*t/P)[:, None] for k in ks], axis=1)
def prod(ca, sa, cb, sb):
    return ca*cb - sa*sb, ca*sb + sa*cb
def split(v):
    n = v.shape[1]//2
    return v[:, :n], v[:, n:]

def model(x, iv):
    i = np.asarray(x[:, 0], dtype=float)
    j = np.asarray(x[:, 1], dtype=float)
    fi = iv("freq_i", cs(i, KS))
    fj = iv("freq_j", cs(j, KS))
    ri = iv("res_i", fi)
    rj = iv("res_j", fj)
    ci, si = split(ri); cj, sj = split(rj)
    rs, rd = prod(ci, si, cj, sj)
    res_sum = iv("res_sum", np.concatenate([rs, rd], axis=1))
    res_diff = iv("res_diff", np.concatenate([prod(ci, si, cj, -sj)[0], prod(ci, si, cj, -sj)[1]], axis=1))
    pi = iv("pre_i", ri)
    pj = iv("pre_j", rj)
    ai, bi = split(pi); aj, bj = split(pj)
    ms, md = prod(ai, bi, aj, bj)
    mlp_sum = iv("mlp_sum", np.concatenate([ms, md], axis=1))
    mlp_c, mlp_s = split(mlp_sum)
    c = np.arange(113)[None, :]
    ang = np.stack([2*np.pi*k*c/P for k in KS], axis=1)  # [1,4,113]
    return (mlp_c[:, :, None]*np.cos(ang) + mlp_s[:, :, None]*np.sin(ang)).sum(axis=1)

ALIGN = {"freq_i": ["embed.0"], "freq_j": ["embed.1"],
         "res_i": ["resid_mid"], "res_j": ["resid_mid"], "res_sum": ["resid_mid"], "res_diff": ["resid_mid"],
         "pre_i": ["mlp_pre"], "pre_j": ["mlp_pre"],
         "mlp_sum": ["mlp_out"]}
