import math

def predict(probe):
    # Model hypothesis:
    # - f is deterministic but pseudo-random-looking for ordinary x [E1,E3,E4,E5,E6,E7]
    # - Ordinary values lie in roughly [-1,1] [E1,E3,E4,E5,E6,E7]
    # - No periodicity, no smoothness, no fractional-part structure found [E4,E6]
    # - A sharp spike at x=0 gives ~475.5 [E2]; f(-1.2),f(-1.1) are ordinary [E1,E5]
    #   so the spike is narrower than ~1 unit; model as very narrow Gaussian (sigma~0.3)
    # - Ordinary part: treat as unpredictable noise; use a deterministic hash of x.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        spike = 475.5144 * math.exp(-(x * x) / (2.0 * 0.3 * 0.3))
        h = math.sin(x * 12.9898 + 4.1414) * 43758.5453
        noise = (h - math.floor(h)) * 2.0 - 1.0
        out.append(spike + noise)
    return {"y": out}
