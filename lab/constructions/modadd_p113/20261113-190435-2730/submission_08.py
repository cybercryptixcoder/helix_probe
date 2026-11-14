
DESCRIPTION = ("Mechanism so far. Input is [i, j, 113] (two variable tokens, constant third token). Attention at the last "
  "position is uniform (each head puts ~1/3 on each of the 3 positions, std 0.001), so it is a plain average of the "
  "three positions and every site from embed up to mlp_pre is exactly affine in the two one-hot token variables "
  "ti = row i of I_114 and tj = row j of I_114 (explained 1.000 at embed.0/1, attn_out, resid_mid, mlp_pre). The MLP "
  "keeps this near affine (relu kinks are spread over ~300 neurons; residual is 0.8% of logit variance, mlp_post/"
  "mlp_out/resid_post are 0.96/0.96/0.99 explained by ti,tj). Readout: logit[c] = mu[c] + F[i][c] + F[j][c] over the "
  "113 classes, with only 8 classes ever reaching the top (97 wins 96.6% of the time). The token table F is 114x113 "
  "and being measured; it is encoded below in the unpacker but not filled in yet, so token identity does not yet move "
  "the output.")

import numpy as np
DIG = "0123456789abcdefghijklmnopqrstuvwxyz"

def unpack(s, off, sc):
    n = len(s) // 3
    a = np.frombuffer(s.encode(), dtype=np.uint8).astype(int)
    v = np.zeros(3 * n, dtype=int)
    for k, d in enumerate(DIG):
        v[a == ord(d)] = k
    v = v.reshape(n, 3)
    return off + sc * (v[:, 0] * 1296 + v[:, 1] * 36 + v[:, 2])

TOP = [97, 14, 47, 85, 105, 73, 98, 59]
NRW = 114                    # rows of F (token ids 0..113; row 113 unused)
C8 = unpack("s6bohxnjsnflmdwkrfk9uk0s", -0.6, 1.6 / 46655.0)      # per-class constant, 8 cols
SF = ""                                                          # F[:, TOP] packed, 8*NRW values

def model(x, iv):
    B = x.shape[0]
    ti = iv("ti", np.eye(114)[x[:, 0]])
    tj = iv("tj", np.eye(114)[x[:, 1]])
    lg = np.zeros((B, 113))
    if len(SF) == 3 * len(TOP) * NRW:
        F = unpack(SF, -0.25, 0.5 / 46655.0).reshape(len(TOP), NRW).T
        lg[:, TOP] = C8[None, :] + ti @ F + tj @ F
    else:
        lg[:, TOP] = C8[None, :] + 0.0 * (ti.sum(1) + tj.sum(1))[:, None]
    return lg

SITES_ALL = ["attn_out", "resid_mid", "mlp_pre", "mlp_post", "mlp_out", "resid_post"]
ALIGN = {"ti": ["embed.0"] + SITES_ALL, "tj": ["embed.1"] + SITES_ALL}
