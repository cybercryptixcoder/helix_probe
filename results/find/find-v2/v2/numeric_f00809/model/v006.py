import math, random

def predict(probe):
    # f(x) model:
    # - x < -79: tiny constant ~0.006 [E9,E11,E14,E15,E21]
    # - x >= -79: random ~N(0,0.1) clipped ±0.32 [E10,E12,E16,E20]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        if x < -79:
            out.append(0.006)
        else:
            out.append(0.0)
    return {"y": out}
