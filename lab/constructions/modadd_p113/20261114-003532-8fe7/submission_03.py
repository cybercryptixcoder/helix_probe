
import numpy as np

DESCRIPTION = ("Input [i, j, 113]; the network's argmax is c = (i+j) mod 113. Token t<113 is encoded as a "
               "Fourier code at 4 frequencies (8, 11, 23, 25) of 113 (cos and sin); position embeddings are "
               "constants. The last position's query is fixed, so attention at the last position produces "
               "attn_out ~= g(i) + g(j) + const, i.e. it just carries the two tokens' Fourier codes into the "
               "residual stream (a linear function of [cos/sin of i, cos/sin of j], 91% of its variance). "
               "The MLP multiplies them (angle addition), the readout is cos(2*pi*f*(c-(i+j))/113). "
               "This file names the two embedding codes and the attention stage's carried codes; the output "
               "is computed from the attention variable by the product (angle-addition) identity.")

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
    att = iv("att", np.hstack([e0, e1]))
    out = np.zeros((x.shape[0], N))
    for k, f in enumerate(FR):
        ci, si = att[:, 2*k], att[:, 2*k+1]
        cj, sj = att[:, 8+2*k], att[:, 8+2*k+1]
        cs = ci*cj - si*sj
        ss = si*cj + ci*sj
        out += cs[:, None]*C[f][None, :] + ss[:, None]*S[f][None, :]
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "att": ["attn_out", "resid_mid"]}
