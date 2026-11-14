import numpy as np

P = 113
K = 56
_k = np.arange(1, K + 1)
_c = np.arange(P)
_ang = 2.0 * np.pi * np.outer(_k, _c) / P
COS_C = np.cos(_ang)
SIN_C = np.sin(_ang)

def _ff(n):
    ang = 2.0 * np.pi * np.outer(n, _k) / P
    return np.concatenate([np.cos(ang), np.sin(ang)], axis=1)

DESCRIPTION = (
    "Computes (a+b) mod 113. Tokens a and b are encoded with a full Fourier basis "
    "(cos/sin for all 56 nonzero frequencies). The MLP sum features are formed by "
    "the product-to-sum identity cos(k(a+b)) = cos(ka)cos(kb) - sin(ka)sin(kb) "
    "and sin(k(a+b)) = sin(ka)cos(kb) + cos(ka)sin(kb). The output logits are the "
    "inverse Fourier transform of these sum features, so class c has maximum logit "
    "at c = (a+b) mod 113. The constant embedding of '=' and the constant attention "
    "pattern are represented by constant variables."
)

def model(x, iv):
    B = x.shape[0]
    a = x[:, 0]
    b = x[:, 1]
    a_ff = iv("a_ff", _ff(a))
    b_ff = iv("b_ff", _ff(b))
    eq = iv("eq", np.ones(B))
    pat = iv("pat", np.ones(B))
    ac = a_ff[:, :K]
    as_ = a_ff[:, K:]
    bc = b_ff[:, :K]
    bs = b_ff[:, K:]
    sc = ac * bc - as_ * bs
    ss = as_ * bc + ac * bs
    s_ff = iv("s_ff", np.concatenate([sc, ss], axis=1))
    logits = s_ff[:, :K] @ COS_C + s_ff[:, K:] @ SIN_C
    return logits

ALIGN = {
    "a_ff": ["embed.0"],
    "b_ff": ["embed.1"],
    "eq": ["embed.2"],
    "pat": ["attn_pattern"],
    "s_ff": ["mlp_post", "mlp_out"],
}
