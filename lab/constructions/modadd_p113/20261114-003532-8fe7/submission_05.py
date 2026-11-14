
import numpy as np

DESCRIPTION = ("Input [i, j, 113]; the network's argmax is c = (i+j) mod 113. Token t<113 is encoded as a "
               "Fourier code at 4 frequencies (8, 11, 23, 25) of 113 (cos and sin); position embeddings are "
               "constants and the last position's query is fixed. Attention at the last position carries each "
               "token's code into the residual stream: attn_out ~= g(i) + g(j) + const, where the position-0 "
               "part depends on token i and the position-1 part on token j. The MLP multiplies the two carried "
               "codes (angle addition), so the sum code cos/sin of (i+j) appears at the MLP and readout stages; "
               "the readout is cos(2*pi*f*(c-(i+j))/113). This file names the embedding codes, the two carried "
               "codes (kept separate: one per token/position), and the sum code.")

N = 113
FR = [8, 11, 23, 25]
C = {f: np.cos(2*np.pi*f*np.arange(N)/N) for f in FR}
S = {f: np.sin(2*np.pi*f*np.arange(N)/N) for f in FR}

def feats(v):
    cols = []
    for f in FR:
        a = 2.0*np.pi*f*v/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, axis=1)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    e0 = iv("e0", feats(i))
    e1 = iv("e1", feats(j))
    ai = iv("atti", e0)
    aj = iv("attj", e1)
    code = np.zeros((x.shape[0], 8))
    for k in range(4):
        ci, si = ai[:, 2*k], ai[:, 2*k+1]
        cj, sj = aj[:, 2*k], aj[:, 2*k+1]
        code[:, 2*k] = ci*cj - si*sj
        code[:, 2*k+1] = si*cj + ci*sj
    code = iv("code", code)
    out = np.zeros((x.shape[0], N))
    for k, f in enumerate(FR):
        out += code[:, [2*k]]*C[f][None, :] + code[:, [2*k+1]]*S[f][None, :]
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "atti": ["attn_out", "resid_mid"],
         "attj": ["attn_out", "resid_mid"], "code": ["mlp_pre", "mlp_post", "mlp_out", "resid_post"]}
