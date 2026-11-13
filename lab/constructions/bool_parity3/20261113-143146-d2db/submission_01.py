
DESCRIPTION = ("The three hidden ReLU units are all driven by the same scalar s = x0+x1+x2, with biases 0,-1,-2: "
               "h1 = [relu(s), relu(s-1), relu(s-2)]. These three shifted/thresholded copies of s are the site's "
               "three coordinates. The output weights (1,-2,2) with bias -0.5 make out = relu(s) - 2relu(s-1) "
               "+ 2relu(s-2) - 0.5, which equals +0.5 when s is odd and -0.5 when s is even (parity of the input).")
import numpy as np

def model(x, iv):
    s = x[:, 0] + x[:, 1] + x[:, 2]
    u0 = iv("u0", np.maximum(s, 0.0))
    u1 = iv("u1", np.maximum(s - 1.0, 0.0))
    u2 = iv("u2", np.maximum(s - 2.0, 0.0))
    out = u0 - 2.0 * u1 + 2.0 * u2 - 0.5
    return out[:, None]

ALIGN = {"u0": ["h1"], "u1": ["h1"], "u2": ["h1"]}
