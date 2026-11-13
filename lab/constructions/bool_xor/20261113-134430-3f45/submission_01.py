import numpy as np

DESCRIPTION = (
    "XOR-like network. Both hidden units see the same pre-activation s = x1 + x2 (row 1 of W1 is [1,1], "
    "b1 = [0,-1]). Unit 1 is relu(s), unit 2 is relu(s-1). The output is h1_1 - 2*h1_2 - 0.5, which equals "
    "0.5 when s == 1 (exactly one input is 1) and -0.5 otherwise."
)

def model(x, iv):
    s = x[:, 0] + x[:, 1]
    u0 = iv("s_lin", s)
    u1 = iv("s_big", np.maximum(s - 1.0, 0.0))
    return (u0 - 2.0 * u1 - 0.5)[:, None]

ALIGN = {"s_lin": ["h1"], "s_big": ["h1"]}
