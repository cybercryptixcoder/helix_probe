
import numpy as np

DESCRIPTION = ("Input [i, j, 113]. The network's argmax is c = (i+j) mod 113. Embeddings: token t<113 is "
               "a Fourier code at 4 frequencies (8, 11, 23, 25) out of 113; position embeddings are constants. "
               "The last position's query is fixed, so attention mixes the two Fourier codes; the MLP then "
               "forms products (angle addition) and the unembedding reads cos(2*pi*f*(c - (i+j))/113) for "
               "f in {8,11,23,25}. This file names the two embedding Fourier codes and computes the output "
               "from them by the product (angle-addition) identity.")

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
    out = np.zeros((x.shape[0], N))
    for k, f in enumerate(FR):
        ci, si = e0[:, 2*k], e0[:, 2*k+1]
        cj, sj = e1[:, 2*k], e1[:, 2*k+1]
        cs = ci*cj - si*sj
        ss = si*cj + ci*sj
        out += cs[:, None]*C[f][None, :] + ss[:, None]*S[f][None, :]
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"]}
