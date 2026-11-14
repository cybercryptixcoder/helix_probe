
import numpy as np

DESCRIPTION = """Placeholder first pass. The net's output is effectively three-valued: out0=0, out2=out4=out5=-100 always, and out1 = 90+30*S, out3 = 90-30*S. So the decision is S = sum(h2 units 0,2,4,6) - sum(h2 units 1,3,5,7) (each with saturated tanh). Only h1 units 0..5 receive input (W1 columns 6..31 are zero, only 6 nonzero rows per column), and only h2 units 0..7 have nonzero output weights; b2=-415 on those 8 makes them near-threshold detectors. The input is 100 blocks of 6 bits; blocks act as 6 fields over index k=0..99: field0/3/4 are one-hot codes, field2 is a multi-hot (~10 ones). W1 col4/col5 (h1 units 4,5) read field3/field4 with weights growing with index k, i.e. they encode the one-hot indices i3 and i4 (differences). cols 0-3 read field3 with small weights (a periodic function of k). Here I only take the raw index codes and the field-2 count as candidate h1-level variables and guess the decision from sign(i3-i4); this is not yet the real mechanism."""

def model(x, iv):
    idx = np.arange(100.0)
    i3 = iv("i3", (x[:, 3::6] * idx).sum(1))
    i4 = iv("i4", (x[:, 4::6] * idx).sum(1))
    c2 = iv("c2", x[:, 2::6].sum(1))
    s = iv("s", i3 - i4)
    S = np.tanh(s / 20.0)
    B = x.shape[0]
    out = np.zeros((B, 6))
    out[:, 0] = 0.0
    out[:, 1] = 90.0 + 30.0 * S
    out[:, 2] = -100.0
    out[:, 3] = 90.0 - 30.0 * S
    out[:, 4] = -100.0
    out[:, 5] = -100.0
    return out

ALIGN = {"i3": ["h1"], "i4": ["h1"], "c2": ["h1"], "s": ["h1"]}
