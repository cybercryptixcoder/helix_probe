import random

def predict(probe):
    # The box is stochastic: same x gives different y across experiments
    # (e.g. x=66.0 -> 0.1235 [E1] vs 0.4241 [E10]; x=-20.3 -> 0.8325 vs 0.3217).
    # For x != 0, y appears uniform in [-1, 1] [E1-E10], so expected value is 0.
    # For x == 0, y is tightly clustered near 475 [E2: 475.35, E6: 474.93, E8: 474.94],
    #   so expected value is ~475. Only exact 0 shows this spike (x=+-1 give ~0).
    # Best single prediction = expected value of each regime.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None)
            continue
        if xv == 0.0:
            # mean of the spike regime (~475); small noise around it
            ys.append(475.0 + random.uniform(-0.3, 0.3))
        else:
            # mean of uniform[-1, 1] is 0
            ys.append(0.0)
    return {"y": ys}
