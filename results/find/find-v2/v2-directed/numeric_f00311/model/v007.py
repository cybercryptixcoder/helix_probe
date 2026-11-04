import math

def predict(probe):
    # A: for x < -9.4, output is constant ~8 with noise [E1,E3,E9,E12,E13,E14]
    # B: for x >= -9.4, output is linear y = 8 - 9.6*x [E1,E2,E4,E5,E10,E11]
    # C: transition boundary is at x = -9.4 (constant for x < -9.4, linear for x >= -9.4) [E15: -9.4 -> 7.96 (constant), -9.398 -> 98.2208 (linear)]
    # D: constant branch is flat at 8 (noise only) [E12,E13,E14]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x < -9.4:
            y = 8.0
        else:
            y = 8.0 - 9.6 * x
        ys.append(y)
    return {"y": ys}
