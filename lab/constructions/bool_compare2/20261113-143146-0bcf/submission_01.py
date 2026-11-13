
import numpy as np

DESCRIPTION = ("The output depends on s = 2*(x1-x3) + (x2-x4). Unit h1_0 = relu(s), h1_1 = relu(s-1). "
               "The output is h1_0 - h1_1 - 0.5, i.e. +0.5 when s>=1 and -0.5 otherwise.")

def model(x, iv):
    s = 2.0 * (x[:, 0] - x[:, 2]) + (x[:, 1] - x[:, 3])
    u0 = iv("u0", np.maximum(s, 0.0))
    u1 = iv("u1", np.maximum(s - 1.0, 0.0))
    return (u0 - u1 - 0.5)[:, None]

ALIGN = {"u0": ["h1"], "u1": ["h1"]}
