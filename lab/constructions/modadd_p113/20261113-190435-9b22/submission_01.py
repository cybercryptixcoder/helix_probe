import numpy as np

DESCRIPTION = "Placeholder: outputs a constant preference for the most common class (39). Established so far: inputs are [i,j,113]; the argmax is class 39 on ~40% of inputs, with ~18 classes ever used."

def model(x, iv):
    B = x.shape[0]
    out = np.zeros((B, 113))
    out[:, 39] = 1.0
    return out

ALIGN = {}
