
import numpy as np

DESCRIPTION = """
The network computes t = (i + j) mod 113 for the input [i, j, 113]: token 113 is a readout
marker at the last position, the first two tokens carry i and j. Position 2 therefore holds
only a constant embedding (token 113 + position 2), and the answer is coded in the attention
output / MLP at that position.

Variables so far: at embed.2 the activation is literally constant (W_E[113] + W_pos[2]); it is
named by a single constant variable. Output: logits peaked at class t.
"""

def model(x, iv):
    i = x[:, 0]
    j = x[:, 1]
    t = (i + j) % 113
    iv("const2", np.ones(len(x)))
    ang = 2.0 * np.pi * t / 113.0
    k = np.arange(113)[None, :]
    a = 2.0 * np.pi * k / 113.0
    logits = (3.0 * np.cos(ang[:, None] - a) + 1.5 * np.cos(2 * (ang[:, None] - a))
              + np.cos(3 * (ang[:, None] - a)) + 0.5 * np.cos(4 * (ang[:, None] - a)))
    return logits

ALIGN = {"const2": ["embed.2"]}
