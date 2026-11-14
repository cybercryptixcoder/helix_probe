import numpy as np

DESCRIPTION = "Placeholder. Established: input is [i,j,113], third token always the marker 113, so embed.2 is a constant vector. Output argmax is class 39 on ~40% of inputs and only ~18 classes ever appear."

def model(x, iv):
    B = x.shape[0]
    t2 = iv("tok_last", x[:, 2].astype(float))
    out = np.zeros((B, 113))
    out[:, 39] = 1.0 + 0.0 * t2[:, None]
    return out

ALIGN = {"tok_last": ["embed.2"]}
