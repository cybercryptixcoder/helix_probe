import numpy as np

DESCRIPTION = "Computes s=x0+x1. Hidden unit 1 is relu(s), hidden unit 2 is relu(s-1); the output is h1 - 2*h2 - 0.5, i.e. positive exactly when the two binary inputs differ."

def model(x, iv):
    s = x[:, 0] + x[:, 1]
    u = iv("u", np.maximum(s, 0.0))
    v = iv("v", np.maximum(s - 1.0, 0.0))
    return (u - 2.0 * v - 0.5)[:, None]

ALIGN = {"u": ["h1"], "v": ["h1"]}
