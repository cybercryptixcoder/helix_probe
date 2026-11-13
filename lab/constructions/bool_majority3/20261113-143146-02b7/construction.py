DESCRIPTION = "Network counts how many of the 3 binary inputs are 1 (s=sum x). Hidden unit 1 is relu(s-1), hidden unit 2 is relu(s-2). Output is h1+h2-0.5, i.e. positive iff at least two inputs are 1."
import numpy as np

def model(x, iv):
    s = iv("s", x.sum(axis=1))
    h1 = iv("h1", np.maximum(s - 1.0, 0.0))
    h2 = iv("h2", np.maximum(s - 2.0, 0.0))
    return (h1 + h2 - 0.5)[:, None]

ALIGN = {"h1": ["h1"], "h2": ["h1"]}
