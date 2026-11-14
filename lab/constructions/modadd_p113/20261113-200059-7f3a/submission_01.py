import numpy as np
DESCRIPTION = "Adds the two tokens mod 113: out = argmax_c cos(2pi((i+j)-c)/113). Rough first sketch."
def model(x, iv):
    i = x[:, 0].astype(float)
    j = x[:, 1].astype(float)
    s = (i + j) % 113.0
    P = 113.0
    c = np.cos(2 * np.pi * (s[:, None] - np.arange(113)[None, :]) / P)
    a = iv("a", np.stack([np.cos(2*np.pi*i/P), np.sin(2*np.pi*i/P)], 1))
    b = iv("b", np.stack([np.cos(2*np.pi*j/P), np.sin(2*np.pi*j/P)], 1))
    return c
ALIGN = {"a": ["embed.0"], "b": ["embed.1"]}
