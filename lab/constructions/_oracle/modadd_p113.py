# ORACLE construction of modadd_p113, written by hand from the known answer (Nanda et al. 2023).
# It is the ceiling the judge is calibrated against. It is NOT produced by the constructor.
P = 113
FREQS = [8, 11, 22, 23, 25]
AMP = [12.5, 6.2, 0.3, 9.8, 6.7]

def feats(t):
    w = 2 * np.pi * np.array(FREQS) / P
    return np.concatenate([np.cos(np.outer(t, w)), np.sin(np.outer(t, w))], 1)      # [B, 10]: cos then sin, per frequency

def model(x, iv):
    a, b = x[:, 0], x[:, 1]
    fa = iv("fourier_a", feats(a))
    fb = iv("fourier_b", feats(b))
    ca, sa, cb, sb = fa[:, :5], fa[:, 5:], fb[:, :5], fb[:, 5:]
    iv("unused_single_terms", np.concatenate([fa, fb], 1))   # present in the neurons, not read by the output
    prod = iv("products", np.concatenate([ca * cb, sa * sb, ca * sb, sa * cb], 1))  # [B, 20]
    s = iv("fourier_sum", np.concatenate([prod[:, :5] - prod[:, 5:10], prod[:, 10:15] + prod[:, 15:]], 1))  # cos, sin of w(a+b)
    c = np.arange(P)
    w = 2 * np.pi * np.array(FREQS) / P
    T = np.concatenate([np.cos(np.outer(w, c)), np.sin(np.outer(w, c))], 0) * np.tile(AMP, 2)[:, None]      # [10, P]
    return s @ T

ALIGN = {
    "fourier_a": ["embed.0", "resid_mid", "mlp_pre"],
    "fourier_b": ["embed.1", "resid_mid", "mlp_pre"],
    "unused_single_terms": ["mlp_post"],
    "products": ["mlp_post"],
    "fourier_sum": ["mlp_out", "resid_post"],
}
