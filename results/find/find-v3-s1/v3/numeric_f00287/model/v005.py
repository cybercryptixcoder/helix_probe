import math

def predict(probe):
    # Model of the black box f(x):
    # Regions determined by floor(x):
    #   floor(x) <= -6  ->  y = -0.7 * floor(x)   [E1,E2,E3,E5: -93.6->65.8, -127.5->89.6, etc.]
    #   -5 <= floor(x) <= 18 -> y ≈ -402.37 (noisy constant)  [E4,E6: x in [-5,18] all ~-402.3..-402.5]
    #   floor(x) >= 19 -> y = -16.8 * floor(x)   [E1,E3,E5,E6: 67.5->-1125.6, 19->-319.2, etc.]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            fx = math.floor(x)
        except Exception:
            ys.append(None)
            continue
        if fx <= -6:
            ys.append(-0.7 * fx)
        elif fx >= 19:
            ys.append(-16.8 * fx)
        else:
            # small region: noisy constant, predict mean
            ys.append(-402.37)
    return {"y": ys}
