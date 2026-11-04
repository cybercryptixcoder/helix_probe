import math

def predict(probe):
    # Model: f(x) is a smooth nonlinear function (small MLP).
    # Evidence:
    #  - E1: large |x| gives small positive outputs (~0.02-0.05), roughly flat.
    #  - E2: near x in [-6,3] there is a smooth bump: rises from 0.047 at -6
    #        to a peak ~0.078 around x=-2, then drops sharply through 0 at x=0
    #        to a negative trough ~-0.095 at x=1, then rises back toward ~-0.05.
    #  - So there is a localized structure near the origin, and a flat
    #    small-positive baseline far away.
    # We model: baseline + a localized bump (positive lobe left of 0)
    #           + a localized dip (negative lobe right of 0).
    # The exact shape is unknown; use smooth Gaussian-like lobes. [E1,E2]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        # baseline: small positive, slowly varying far from origin
        base = 0.03
        # positive lobe centered near x=-2, width ~2.5
        pos = 0.05 * math.exp(-((x + 2.0) ** 2) / (2 * 2.5 ** 2))
        # negative lobe centered near x=1, width ~2.0
        neg = -0.12 * math.exp(-((x - 1.0) ** 2) / (2 * 2.0 ** 2))
        y = base + pos + neg
        out.append(round(y, 4))
    return {"y": out}
