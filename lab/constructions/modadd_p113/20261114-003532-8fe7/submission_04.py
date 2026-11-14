
import numpy as np

DESCRIPTION = ("Input [i, j, 113]; the network's argmax is c = (i+j) mod 113. Token t<113 is encoded as a "
               "Fourier code at 4 frequencies (8, 11, 23, 25) of 113 (cos and sin); position embeddings are "
               "constants and the last position's query is fixed. Attention at the last position carries the "
               "two tokens' codes into the residual stream: attn_out ~= g(i) + g(j) + const, a linear function "
               "of [cos/sin of i, cos/sin of j]. The MLP multiplies the two codes (angle addition), so mlp_pre / "
               "mlp_post / mlp_out hold the 'sum code' cos/sin of (i+j) at the same 4 frequencies; the readout "
               "is cos(2*pi*f*(c-(i+j))/113). This file names the embedding codes, the attention-carried codes, "
               "and the sum code at the MLP and readout stages.")

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

def sumcode(a):
    out = np.zeros((a.shape[0], 8))
    for k in range(4):
        ci, si = a[:, 2*k], a[:, 2*k+1]
        cj, sj = a[:, 8+2*k], a[:, 8+2*k+1]
        out[:, 2*k] = ci*cj - si*sj
        out[:, 2*k+1] = si*cj + ci*sj
    return out

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    e0 = iv("e0", feats(i))
    e1 = iv("e1", feats(j))
    att = iv("att", np.hstack([e0, e1]))
    code = iv("code", sumcode(att))
    out = np.zeros((x.shape[0], N))
    for k, f in enumerate(FR):
        out += code[:, [2*k]]*C[f][None, :] + code[:, [2*k+1]]*S[f][None, :]
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "att": ["attn_out", "resid_mid"],
         "code": ["mlp_pre", "mlp_post", "mlp_out", "resid_post"]}
