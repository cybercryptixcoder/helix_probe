import numpy as np
import math

P = 113
FREQ = [1, 2, 3, 4, 5, 6, 7, 8]
K = len(FREQ)
W = [2.0 * math.pi * k / P for k in FREQ]

DESCRIPTION = (
 "Fourier / trigonometric-identity solution for (a + b) mod 113. "
 "Token embeddings are Fourier features cos(w_k t), sin(w_k t) with w_k = 2*pi*k/113 "
 "for a small set of frequencies k. The last position ('=') attends to positions 0 and 1 "
 "with (essentially constant) weights, so what attention writes into the final position, "
 "the residual stream after attention, and the MLP pre-activations are all affine functions "
 "of the four feature blocks {cos(w a), sin(w a), cos(w b), sin(w b)}. "
 "The MLP applies the product-to-sum identities "
 "cos(w(a+b)) = cos(wa)cos(wb) - sin(wa)sin(wb) and "
 "sin(w(a+b)) = sin(wa)cos(wb) + cos(wa)sin(wb), so its output and the final residual "
 "stream carry cos/sin features of s = a + b mod 113. "
 "The unembedding scores class c by sum_k cos(w_k (s - c)), which is maximal exactly at c = s."
)

def _feats(t):
    t = np.asarray(t, dtype=np.float64)
    cs = [np.cos(w * t) for w in W]
    sn = [np.sin(w * t) for w in W]
    return np.stack(cs + sn, axis=1)   # [B, 2K] : K cosines then K sines

def model(x, iv):
    x = np.asarray(x)
    B = x.shape[0]
    a = x[:, 0].astype(np.float64)
    b = x[:, 1].astype(np.float64)

    # --- embedding stage -------------------------------------------------
    t0 = iv("tok0", _feats(a))                       # embed.0 : features of token a
    t1 = iv("tok1", _feats(b))                       # embed.1 : features of token b
    eq = iv("eq_const", np.ones((B, 1)))             # embed.2 : '=' token embedding is fixed

    # --- attention stage: copy a- and b-features to the last position ----
    ab = iv("ab_last", np.concatenate([t0, t1], axis=1))   # [B, 4K]
    ca, sa = ab[:, :K], ab[:, K:2 * K]
    cb, sb = ab[:, 2 * K:3 * K], ab[:, 3 * K:4 * K]

    # --- mlp stage: product-to-sum ---------------------------------------
    sc = ca * cb - sa * sb        # cos(w (a+b))
    ss = sa * cb + ca * sb        # sin(w (a+b))
    sm = iv("sum_feats", np.concatenate([sc, ss], axis=1))  # [B, 2K]

    # --- readout: logits[c] = sum_k cos(w_k (s - c)) ----------------------
    cls = np.arange(113, dtype=np.float64)
    cosmat = np.stack([np.cos(w * cls) for w in W], axis=0)   # [K, 113]
    sinmat = np.stack([np.sin(w * cls) for w in W], axis=0)   # [K, 113]
    logits = sm[:, :K] @ cosmat + sm[:, K:] @ sinmat
    return 20.0 * logits

ALIGN = {
    "tok0": ["embed.0"],
    "tok1": ["embed.1"],
    "eq_const": ["embed.2"],
    "ab_last": ["attn_out", "resid_mid", "mlp_pre"],
    "sum_feats": ["mlp_out", "resid_post"],
}
