
import numpy as np

DESCRIPTION = ("Task: input [i, j, 113]; the network outputs logits over c in 0..112 with the argmax "
               "at c = (i+j) mod 113. First stage: token embeddings are Fourier features of the token "
               "index at frequencies 8, 11, 23, 25 out of 113 (8 real dimensions); position embeddings are "
               "constants. So embed.0 is a fixed affine function of [cos/sin at 4 freqs of i], embed.1 the "
               "same for j, embed.2 is constant.")

N = 113
FR = [8, 11, 23, 25]

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
    e2 = iv("e2", np.ones((x.shape[0], 1)))
    c = (x[:, 0] + x[:, 1]) % N
    out = np.full((x.shape[0], N), -10.0)
    out[np.arange(x.shape[0]), c] = 10.0
    return out

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "e2": ["embed.2"]}
