
import numpy as np
import math

DESCRIPTION = ("The network does modular addition on the token indices at positions 0 and 1 "
               "(token 113 at position 2 is a fixed 'equals' token): output argmax = (i+j) mod 113. "
               "Embeddings are Fourier features of the token index; the output logits are a "
               "cosine-shaped readout peaked at the answer. This partial construction only gets the "
               "behaviour and the Fourier structure of the embedding stage.")

N = 113
KS = [8, 11, 22, 23, 25]

def fourier(t):
    cols = []
    for k in KS:
        a = 2*math.pi*k*t/N
        cols.append(np.cos(a))
        cols.append(np.sin(a))
    return np.stack(cols, axis=1)

def model(x, iv):
    i = x[:, 0].astype(int)
    j = x[:, 1].astype(int)
    e0 = iv("emb0", fourier(i))
    e1 = iv("emb1", fourier(j))
    tokens = np.round(np.fft.irfft(np.zeros((N, 1)), n=N))  # placeholder not used
    s = (i + j) % N
    # logits: cosine readout peaked at the correct class
    cls = np.arange(N)
    logits = np.cos(2*math.pi*(cls[None, :] - s[:, None])/N) * 20.0
    return logits

ALIGN = {"emb0": ["embed.0"], "emb1": ["embed.1"]}
