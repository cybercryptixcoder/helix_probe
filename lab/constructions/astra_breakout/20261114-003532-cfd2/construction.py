
import numpy as np
DESCRIPTION = """
A gated three-way comparison on a 0/1 input laid out as 100 groups of 6 (index 6k+r; data in r=3 and r=4).
h1: only columns 0..5 of W1 are nonzero (units 6..31 dead, b1=0 except b1[5]=5). Units 0..3 are small
  linear forms of the input (|h1|<=0.18, i.e. essentially their preactivation): unit j sums the r=3
  position of each group with a drifting triangular 0.02-valued profile (plus a shared ramp on the last
  nine even positions). Units 4 and 5 have huge norms (1499, 745), so they saturate to +-1: they are two
  selectors, a = h1[4] (period-10 ramp on r=3 / r=4 pairs) and b = h1[5] (level k//10 of the group index,
  the r=4 side negated, plus bias 5).
h2: W2 uses rows 0..5 and columns 0..7 only with b2 = -415, so each h2 unit is a threshold detector
  pre2 = -1000*h1[j//2]*(+1 for even j, -1 for odd) + 200*(sA_j*a + sB_j*b) - 415. Pair (2i,2i+1) can be
  armed only by one (sign a, sign b) combination: (+,+)->i=0, (-,+)->i=1, (+,-)->i=2, (-,-)->i=3, and then
  h2[2i] = +1 iff h1[i] < -0.015, h2[2i+1] = +1 iff h1[i] > +0.015 (the other pairs stay at -1).
out: W3 puts 30 on h2 units 0,2,4,6 into out1 and on 1,3,5,7 into out3, b3 = [0,90,-100,90,-100,-100],
  hence out1 = 60*S1-30, out3 = 60*S3-30 with S in {0,1}, out0 = 0 and out2 = out4 = out5 = -100.
  Decision: the selectors pick one of h1[0..3]; out3 wins if it exceeds +0.015, out1 if it is below
  -0.015, and the constant out0 = 0 if it lies in between.
"""
K = np.arange(100)
def V(s): return np.array([int(t) for t in s.split()], float)
G = np.stack([
 V("16 18 18 16 14 12 10 8 6 4 14 16 18 18 16 14 12 10 8 6 12 14 16 18 18 16 14 12 10 8 10 12 14 16 18 18 16 14 12 10 8 10 12 14 16 18 18 16 14 12 6 8 10 12 14 16 18 18 16 14 5 7 9 11 13 15 17 18 17 15 3 5 7 9 11 13 15 17 18 17 1 3 5 7 9 11 13 15 17 18 0 2 4 6 8 10 12 14 16 18"),
 V("14 12 10 8 6 4 2 0 0 2 12 10 8 6 4 2 0 0 2 4 10 8 6 4 2 0 0 2 4 6 8 6 4 2 0 0 2 4 6 8 6 4 2 0 0 2 4 6 8 10 4 2 0 0 2 4 6 8 10 12 3 1 0 1 3 5 7 9 11 13 1 0 1 3 5 7 9 11 13 15 0 1 3 5 7 9 11 13 15 17 0 2 4 6 8 10 12 14 16 18"),
 V("18 18 16 14 12 10 8 6 4 2 18 16 14 12 10 8 6 4 2 0 14 16 18 18 16 14 12 10 8 6 12 14 16 18 18 16 14 12 10 8 10 12 14 16 18 18 16 14 12 10 12 14 16 18 18 16 14 12 10 8 14 16 18 18 16 14 12 10 8 6 16 18 18 16 14 12 10 8 6 4 18 18 16 14 12 10 8 6 4 2 0 2 4 6 8 10 12 14 16 18"),
 V("16 14 12 10 8 6 4 2 0 0 18 16 14 12 10 8 6 4 2 0 12 10 8 6 4 2 0 0 2 4 10 8 6 4 2 0 0 2 4 6 8 6 4 2 0 0 2 4 6 8 10 8 6 4 2 0 0 2 4 6 12 10 8 6 4 2 0 0 2 4 14 12 10 8 6 4 2 0 0 2 16 14 12 10 8 6 4 2 0 0 0 2 4 6 8 10 12 14 16 18")], 1) * 0.01
I3 = 6 * K + 3
I4 = 6 * K + 4
S9 = np.arange(9)
IE = 546 + 6 * S9
TAIL = -0.02 * (S9 + 1.0)
CYC = np.array([1, 2, 4, 6, 8, 10, 12, 14, 16, 17.])[K % 10]
CYCB = np.array([0, -2, -4, -6, -8, -10, -12, -14, -16, -18.])[K % 10]
CV = np.zeros(100); CV[10:] = K[10:] // 10; CV[80:90] = 7.0; CV[90:] = 9.0
DV = -(K // 10).astype(float)
SA = np.array([200.0, 200.0, -200.0, -200.0, 200.0, 200.0, -200.0, -200.0])
SB = np.array([200.0, 200.0, 200.0, 200.0, -200.0, -200.0, -200.0, -200.0])
def model(x, iv):
    P = x[:, I3] @ G + (x[:, IE] @ TAIL)[:, None]
    u0 = iv("h1u0", np.tanh(P[:, 0]))
    u1 = iv("h1u1", np.tanh(P[:, 1]))
    u2 = iv("h1u2", np.tanh(P[:, 2]))
    u3 = iv("h1u3", np.tanh(P[:, 3]))
    a = iv("sel_a", np.tanh(x[:, I3] @ (10.0 * CYC) + x[:, I4] @ (10.0 * CYCB)))
    b = iv("sel_b", np.tanh(x[:, I3] @ (10.0 * CV) + x[:, I4] @ (10.0 * DV) + 5.0))
    pre = np.stack([-1000 * u0, 1000 * u0, -1000 * u1, 1000 * u1,
                    -1000 * u2, 1000 * u2, -1000 * u3, 1000 * u3], 1)
    h2 = iv("h2", np.tanh(pre + a[:, None] * SA + b[:, None] * SB - 415.0))
    se = h2[:, 0::2].sum(1); so = h2[:, 1::2].sum(1)
    z = np.zeros_like(se)
    return np.stack([z, 30 * se + 90, -100 + z, 30 * so + 90, -100 + z, -100 + z], 1)
ALIGN = {"h1u0": ["h1"], "h1u1": ["h1"], "h1u2": ["h1"], "h1u3": ["h1"],
         "sel_a": ["h1"], "sel_b": ["h1"], "h2": ["h2"]}
