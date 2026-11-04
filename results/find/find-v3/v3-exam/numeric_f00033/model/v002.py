import math

def predict(probe):
    # A: f has a sharp tall spike at x=0, peak ~0.387 [E2]
    # B: f has a broad bump peaking near x≈1-3, value ~0.036 at 2.9, ~0.228 at 1.2 [E1,E3]
    #    -> the broad bump is actually centered near x≈1.2 with amplitude ~0.23?
    #    E1: x=2.9 -> 0.0362; E3: x=1.2 -> 0.228. So bump is centered near 1.2, not 2.9.
    #    At 2.9 (dist 1.7) value 0.036; at 1.2 value 0.228. Gaussian: ratio 0.036/0.228=0.158
    #    exp(-1.7^2/(2s^2))=0.158 -> 1.7^2/(2s^2)=1.845 -> s^2=0.783 -> s≈0.885.
    # C: far field is a slowly varying negative baseline ~ -0.0002 at large |x|,
    #    more negative at moderate |x| (-0.004 at ±40..128, -0.002 at ±30, -0.0008 at -15) [E2]
    #    Looks like baseline ~ -0.004 * exp(-|x|/large) plus small offset. Fit roughly.
    # D: spike at 0 is narrow: at x=-3 -> 0.008, x=5 -> 0.0012, so width ~1 [E2]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # broad bump near 1.2
            bump = 0.228 * math.exp(-((x - 1.2) ** 2) / (2 * 0.885 ** 2))
            # sharp spike at 0
            spike = 0.387 * math.exp(-(x ** 2) / (2 * 0.9 ** 2))
            # baseline: negative, magnitude grows with |x| up to ~0.004
            base = -0.004 * (1 - math.exp(-abs(x) / 25.0)) - 0.0002
            v = bump + spike + base
        except Exception:
            v = None
        ys.append(v)
    return {"y": ys}
