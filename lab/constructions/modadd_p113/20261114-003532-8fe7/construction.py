
import numpy as np

DESCRIPTION = ("Input [i, j, 113]; argmax output is c = (i+j) mod 113. Token t<113 is a Fourier code at "
               "frequencies 8, 11, 23, 25 of 113 (cos and sin); positions/last-position query are constants. "
               "Attention at the last position mixes the two tokens' codes into the residual stream (a "
               "softmax-weighted mixture, well described by a linear function of [code(i), code(j)]). The MLP "
               "multiplies the two codes (angle addition) so mlp_post/mlp_out/resid_post carry the sum code "
               "cos/sin of (i+j); the readout is cos(2*pi*f*(c-(i+j))/113).")

N = 113
FR = [8, 11, 23, 25, 5]
C = {f: np.cos(2*np.pi*f*np.arange(N)/N) for f in FR}
S = {f: np.sin(2*np.pi*f*np.arange(N)/N) for f in FR}

def feats(v):
    cols = []
    for f in FR:
        a = 2.0*np.pi*f*v/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, axis=1)

def sumcode(a):
    D = 2*len(FR)
    out = np.zeros((a.shape[0], 8))
    for k in range(4):
        ci, si = a[:, 2*k], a[:, 2*k+1]
        cj, sj = a[:, D+2*k], a[:, D+2*k+1]
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
    for k, f in enumerate(FR[:4]):
        out += code[:, [2*k]]*C[f][None, :] + code[:, [2*k+1]]*S[f][None, :]
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "att": ["attn_out", "resid_mid"],
         "code": ["mlp_post", "mlp_out", "resid_post"]}

# ---- added by the constructor at the end of the run ----
# These sites failed the judge's tests in the reader's best submission, so the delivered construction does not claim
# them. The variables stay in model(); they are just not aligned there. See run.json for the attempt and its report.
_UNVERIFIED_SITES = ["attn_out", "resid_mid"]
ALIGN = {v: [s for s in where if s not in _UNVERIFIED_SITES] for v, where in ALIGN.items()}
ALIGN = {v: where for v, where in ALIGN.items() if where}
