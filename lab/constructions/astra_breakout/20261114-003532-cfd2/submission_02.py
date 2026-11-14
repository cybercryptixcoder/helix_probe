
import numpy as np
DESCRIPTION = """
Skeleton of the mechanism (input weights still approximate).
Only h1 units 0..5 are alive (W1 columns 6..31 are zero, b1=0 except b1[5]=5).
h1 units 4 and 5 have huge weights (norms 1499, 745) so they are saturated +-1 selectors
a = h1[4], b = h1[5]; h1 units 0..3 are small linear maps of the input (|.|<=0.18).
W2 uses only rows 0..5 and columns 0..7, with b2 = -415 on those 8 units, so
h2[j] = +-1 is a threshold detector: pre2 = -1000/h1[0..3] terms + 200*(a,b) signs - 415.
Pairing: unit 0 needs (a,b)=(+,+) and h1[0]>0; unit 1 needs (+,+) and h1[0]<0;
unit 2/3 select h1[1] with (a,b)=(-,+); unit4/5 select h1[2] with (+,-); unit6/7 select h1[3] with (-,-).
W3 has 30 on h2 units 0,2,4,6 into out1 and on 1,3,5,7 into out3; b3=[0,90,-100,90,-100,-100].
So out1 = 60*S1-30, out3 = 60*S3-30 with S=#{even/odd h2 = +1} in {0,1}, out0=0, others -100:
the decision is out1 if the selected h1 unit is negative, out3 if positive, out0 (0) if it is ~0.
Input layout: index 6k+3 / 6k+4 pairs (a 100-step sequence) plus a tail at stride 3 from 540.
This file only has the selectors approximately and no h1 units 0..3 yet.
"""
IDX3 = np.arange(3, 600, 6)
def model(x, iv):
    idx4 = IDX3 + 1
    w = np.zeros(100); w[1:] = 20.0 * np.arange(1, 100)
    a = iv("sel_a", np.tanh(x[:, IDX3] @ w - x[:, idx4] @ w))
    b = iv("sel_b", np.tanh(10.0 * (x[:, IDX3[10:]].sum(1) - x[:, idx4[10:]].sum(1)) + 5.0))
    p = np.zeros((x.shape[0], 4))          # placeholder for h1 units 0..3
    p0, p1, p2, p3 = p[:, 0], p[:, 1], p[:, 2], p[:, 3]
    pre = np.stack([-1000 * p0, 1000 * p0, -1000 * p1, 1000 * p1,
                    -1000 * p2, 1000 * p2, -1000 * p3, 1000 * p3], 1)
    sA = np.array([200.0, 200.0, -200.0, -200.0, 200.0, 200.0, -200.0, -200.0])
    sB = np.array([200.0, 200.0, 200.0, 200.0, -200.0, -200.0, -200.0, -200.0])
    pre = pre + a[:, None] * sA + b[:, None] * sB - 415.0
    h2 = iv("h2", np.tanh(pre))
    se = h2[:, 0::2].sum(1); so = h2[:, 1::2].sum(1)
    z = np.zeros_like(se)
    return np.stack([z, 30 * se + 90, -100 + z, 30 * so + 90, -100 + z, -100 + z], 1)
ALIGN = {"sel_a": ["h1"], "sel_b": ["h1"], "h2": ["h2"]}
