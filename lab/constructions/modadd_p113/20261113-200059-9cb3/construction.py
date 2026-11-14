import numpy as np

DESCRIPTION = (
 "The network computes (a+b) mod 113 for the sequence 'a b =' and reads 113 logits at the '=' position. "
 "Tokens are carried by Fourier features: token t is the 112 numbers cos(2*pi*k*t/113), sin(2*pi*k*t/113) "
 "for k=1..56 (an invertible, complete code for a number mod 113). "
 "EMBEDDING: the residual at position 0 (resp. 1) is an affine function of the Fourier code of a (resp. b). "
 "ATTENTION: the last position's query is fixed ('=' plus position 2), so the heads mainly copy the a- and "
 "b-embeddings forward; attn_out and resid_mid at the last position therefore carry the two token codes. "
 "MLP: using cos(w(a+b)) = cos(wa)cos(wb) - sin(wa)sin(wb) and sin(w(a+b)) = sin(wa)cos(wb) + cos(wa)sin(wb) "
 "the MLP turns the two token codes into the Fourier code of the sum s = (a+b) mod 113; those sum features "
 "appear in mlp_post and mlp_out. "
 "READOUT: resid_post holds the code of s and the unembedding scores class c by "
 "logit_c = sum_k cos(2*pi*k*(s-c)/113), whose unique maximum is c = s."
)

_P = 113
_KMAX = 56
_k = np.arange(1, _KMAX + 1)
_w = (2.0 * np.pi / _P) * _k
_TAB = np.concatenate([np.cos(np.arange(_P)[:, None] * _w[None, :]),
                       np.sin(np.arange(_P)[:, None] * _w[None, :])], axis=1)  # [113,112]


def _code(t):
    ang = np.asarray(t, dtype=float)[:, None] * _w[None, :]
    return np.concatenate([np.cos(ang), np.sin(ang)], axis=1)


def model(x, iv):
    a0 = x[:, 0].astype(int)
    b0 = x[:, 1].astype(int)

    # embedding stage: Fourier codes of the two tokens
    ca = iv("tok_a", _code(a0))          # [B,112]
    cb = iv("tok_b", _code(b0))          # [B,112]

    # trig identity: code of a+b mod 113, bilinear in the two token codes
    ac, as_ = ca[:, :_KMAX], ca[:, _KMAX:]
    bc, bs = cb[:, :_KMAX], cb[:, _KMAX:]
    cs = iv("sum_feat", np.concatenate([ac * bc - as_ * bs,
                                        ac * bs + as_ * bc], axis=1))  # [B,112] = code(a+b)

    # readout: logit_c = sum_k cos(w_k (s-c)) = code(s) . code(c)
    return cs @ _TAB.T


ALIGN = {
    "tok_a": ["embed.0", "attn_out", "resid_mid", "mlp_pre"],
    "tok_b": ["embed.1", "attn_out", "resid_mid", "mlp_pre"],
    "sum_feat": ["mlp_post", "mlp_out", "resid_post"],
}
