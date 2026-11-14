
import numpy as np
DESCRIPTION = ("Network computes (i+j) mod 113 for input [i,j,113]. Token embeddings are a 4-frequency clock: E[t] lies "
 "(up to ~12% residual) in the span of cos/sin(2*pi*k*t/113), k in {8,11,23,25}, so embed.0/embed.1 are described by that "
 "8-dim code of i and of j. Each frequency pair k determines t mod 113 (113 prime); the four estimates are combined as a "
 "phasor mean to decode i and j, and s=(i+j) mod 113. The answer then travels as the same 8-dim clock code of s (at mlp_post, "
 "mlp_out, resid_post); the readout turns each pair into 5*cos(2*pi*k*(s-c)/113), so logits peak at class s.")
FREQ = [8.0, 11.0, 23.0, 25.0]
INV = [99, 72, 59, 95]   # modular inverses of 8,11,23,25 mod 113
def code(t):
    return np.stack([f(2*np.pi*k*t/113.0) for k in FREQ for f in (np.cos, np.sin)], 1)
def decode(v):                                  # v: [B,8] code -> t mod 113
    z = 0
    for q in range(4):
        th = np.arctan2(v[:, 2*q+1], v[:, 2*q])
        est = ((th*113.0/(2*np.pi)) % 113.0)*INV[q] % 113.0
        z = z + np.exp(2j*np.pi*est/113.0)
    t = np.round(np.angle(z)*113.0/(2*np.pi)) % 113
    return t
def model(x, iv):
    ci = iv("code_i", code(x[:, 0].astype(float)))
    cj = iv("code_j", code(x[:, 1].astype(float)))
    i = decode(ci); j = decode(cj)
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
