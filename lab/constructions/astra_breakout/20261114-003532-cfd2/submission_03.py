
import numpy as np
DESCRIPTION = """
Mechanism (stage by stage).
Inputs are 0/1 in 3-blocks (index 3m); the useful positions are the pairs 6k+3 / 6k+4 of a 100-step sequence.
h1: W1 has nonzero columns only 0..5 (units 6..31 dead; b1=0 except b1[5]=5).
  units 0,1 (and 2,3) are small linear maps of the input, |h1|<=0.18, i.e. the linear form itself.
  units 4,5 have huge weights (norms 1499 / 745) so they are saturated +-1: they are two selectors
  a = h1[4], b = h1[5].
h2: W2 uses rows 0..5 and columns 0..7 only, b2 = -415 on units 0..7, so each h2 unit j is a
  threshold detector: pre2_j = -1000*h1[j//2] (sign + for odd j) + 200*(a,b) sign pattern - 415.
  Pair (2i,2i+1) is armed only by one of the four (sign a, sign b) combinations:
  (+,+)->i=0, (-,+)->i=1, (+,-)->i=2, (-,-)->i=3, and then
  h2[2i] = +1 iff h1[i] < -0.015, h2[2i+1] = +1 iff h1[i] > +0.015.
out: W3 puts 30 on h2 units 0,2,4,6 into out1 and on 1,3,5,7 into out3; b3 = [0,90,-100,90,-100,-100],
  so out1 = 60*S1-30, out3 = 60*S3-30 with S in {0,1}, out0 = 0 and out2 = out4 = out5 = -100.
  Decision: the two selectors pick which of h1[0..3] is compared; out1 wins if it is below -0.015,
  out3 if it is above +0.015, and out0 (the constant 0) if it is in between.
Status: units 0, 1 and 5 are exact; units 2, 3 and 4 are still placeholders/approximations here.
"""
U0 = ("3:16 9:18 15:18 21:16 27:14 33:12 39:10 45:8 51:6 57:4 63:14 69:16 75:18 81:18 87:16 93:14 99:12 "
      "105:10 111:8 117:6 123:12 129:14 135:16 141:18 147:18 153:16 159:14 165:12 171:10 177:8 183:10 189:12 "
      "195:14 201:16 207:18 213:18 219:16 225:14 231:12 237:10 243:8 249:10 255:12 261:14 267:16 273:18 279:18 "
      "285:16 291:14 297:12 303:6 309:8 315:10 321:12 327:14 333:16 339:18 345:18 351:16 357:14 363:5 369:7 375:9 "
      "381:11 387:13 393:15 399:17 405:18 411:17 417:15 423:3 429:5 435:7 441:9 447:11 453:13 459:15 465:17 471:18 "
      "477:17 483:1 489:3 495:5 501:7 507:9 513:11 519:13 525:15 531:17 537:18 546:-2 549:2 552:-4 555:4 558:-6 "
      "561:6 564:-8 567:8 570:-10 573:10 576:-12 579:12 582:-14 585:14 588:-16 591:16 594:-18 597:18")
U1 = ("3:14 9:12 15:10 21:8 27:6 33:4 39:2 57:2 63:12 69:10 75:8 81:6 87:4 93:2 111:2 117:4 123:10 129:8 "
      "135:6 141:4 147:2 165:2 171:4 177:6 183:8 189:6 195:4 201:2 219:2 225:4 231:6 237:8 243:6 249:4 255:2 "
      "273:2 279:4 285:6 291:8 297:10 303:4 309:2 327:2 333:4 339:6 345:8 351:10 357:12 363:3 369:1 381:1 387:3 "
      "393:5 399:7 405:9 411:11 417:13 423:1 435:1 441:3 447:5 453:7 459:9 465:11 471:13 477:15 489:1 495:3 501:5 "
      "507:7 513:9 519:11 525:13 531:15 537:17 546:-2 549:2 552:-4 555:4 558:-6 561:6 564:-8 567:8 570:-10 573:10 "
      "576:-12 579:12 582:-14 585:14 588:-16 591:16 594:-18 597:18")
def _p(s, sc):
    q = np.array([[int(t) for t in p.split(':')] for p in s.split()])
    return q[:, 0], q[:, 1] * sc
I0, V0 = _p(U0, 0.01)
I1, V1 = _p(U1, 0.01)
K = np.arange(10, 100)
I5a, I5b = 6 * K + 3, 6 * K + 4
KM = np.arange(1, 100)
I4a, I4b = 6 * KM + 3, 6 * KM + 4
def model(x, iv):
    u0 = iv("h1u0", np.tanh(x[:, I0] @ V0))
    u1 = iv("h1u1", np.tanh(x[:, I1] @ V1))
    u2 = iv("h1u2", u0)                                  # placeholder
    u3 = iv("h1u3", u1)                                  # placeholder
    pre4 = 10.0 * x[:, 3] + 20.0 * KM * (x[:, I4a] @ np.ones(99) - x[:, I4b] @ np.ones(99))
    a = iv("sel_a", np.tanh(pre4))                        # approximate
    b = iv("sel_b", np.tanh(10.0 * (x[:, I5a].sum(1) - x[:, I5b].sum(1)) + 5.0))
    p = [u0, u1, u2, u3]
    pre = np.stack([-1000 * p[0], 1000 * p[0], -1000 * p[1], 1000 * p[1],
                    -1000 * p[2], 1000 * p[2], -1000 * p[3], 1000 * p[3]], 1)
    sA = np.array([200.0, 200.0, -200.0, -200.0, 200.0, 200.0, -200.0, -200.0])
    sB = np.array([200.0, 200.0, 200.0, 200.0, -200.0, -200.0, -200.0, -200.0])
    pre = pre + a[:, None] * sA + b[:, None] * sB - 415.0
    h2 = iv("h2", np.tanh(pre))
    se = h2[:, 0::2].sum(1); so = h2[:, 1::2].sum(1)
    z = np.zeros_like(se)
    return np.stack([z, 30 * se + 90, -100 + z, 30 * so + 90, -100 + z, -100 + z], 1)
ALIGN = {"h1u0": ["h1"], "h1u1": ["h1"], "h1u2": ["h1"], "h1u3": ["h1"],
         "sel_a": ["h1"], "sel_b": ["h1"], "h2": ["h2"]}
