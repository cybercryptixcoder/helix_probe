
import numpy as np
DESCRIPTION = ("Network computes (i+j) mod 113 for input [i,j,113]. Token embeddings are a 4-frequency clock: "
 "E[t] lies (up to 12% residual) in the span of cos/sin(2*pi*k*t/113) for k in {8,11,23,25}. So embed.0/embed.1 are "
 "described by that 8-dim code of i and of j; i and j are decoded from the code (k=8 alone determines the token, 113 prime). "
 "The answer then travels as an 8-dim clock code of s=(i+j) mod 113 (visible at mlp_post, mlp_out, resid_post); the readout "
 "turns each frequency pair k into 5*cos(2*pi*k*(s-c)/113), so logits peak at class s.")
FREQ = [8.0, 11.0, 23.0, 25.0]
def code(t):
    return np.stack([f(2*np.pi*k*t/113.0) for k in FREQ for f in (np.cos, np.sin)], 1)
def decode(cs, sn, k):
    return np.round((np.arctan2(sn, cs) % (2*np.pi))*113.0/(2*np.pi*k)) % 113
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ci = iv("code_i", code(i))                       # [B,8]
    cj = iv("code_j", code(j))                       # [B,8]
    i = decode(ci[:, 0], ci[:, 1], 8.0)
    j = decode(cj[:, 0], cj[:, 1], 8.0)
    s = (i + j) % 113
    cs = iv("cos_k", np.cos(np.stack([2*np.pi*k*s/113.0 for k in FREQ], 1)))
    sn = iv("sin_k", np.sin(np.stack([2*np.pi*k*s/113.0 for k in FREQ], 1)))
    c = np.arange(113)[None, :]
    out = np.full((x.shape[0], 113), -30.0)
    for q, k in enumerate(FREQ):
        T = (np.arctan2(sn[:, q], cs[:, q]) * 113.0/(2*np.pi*k)) % 113.0
        out = out + 5.0*np.cos(2*np.pi*k*(T[:, None] - c)/113.0)
    return out
ALIGN = {"code_i": ["embed.0"], "code_j": ["embed.1"],
         "cos_k": ["mlp_post", "mlp_out", "resid_post"], "sin_k": ["mlp_post", "mlp_out", "resid_post"]}
