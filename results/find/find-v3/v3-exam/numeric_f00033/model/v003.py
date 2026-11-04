import math

def predict(probe):
    # A: sharp spike at x=0, peak ~0.387 [E2,E4]
    # B: broad bump centered near x=0, not 1.2: E4 shows monotone decay from 0
    #    (0.387 at 0, 0.305 at 0.5, 0.197 at 1, 0.0575 at 2, 0.0012 at 5).
    #    Fit: Gaussian-ish with sigma ~1.0 plus small tail. Use sigma ~0.95.
    # C: far field baseline is ~0 for |x|>~20, and slightly negative (-0.003..-0.004)
    #    in a band around |x|~40-128 [E1,E2,E5]. Actually E2: -0.0044 at -128,
    #    -0.003 at -40, -0.0021 at -30, -0.0008 at -15, ~0 at 25..128 on +side.
    #    E5: -0.0032 at -48.6, -0.004 at -102.2, -0.001 at -16.9, ~0 on +side.
    #    So negative baseline is on the NEGATIVE side for large |x|, ~0 on positive.
    #    Model: base = -0.004 * sigmoid-ish on negative x beyond ~15, decaying to 0.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # broad bump centered at 0 (includes spike as peak)
            bump = 0.387 * math.exp(-(x ** 2) / (2 * 0.95 ** 2))
            # negative baseline on negative side, moderate magnitude
            if x < -10:
                base = -0.004 * (1 - math.exp(-(abs(x) - 10) / 20.0))
            else:
                base = 0.0
            v = bump + base
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
