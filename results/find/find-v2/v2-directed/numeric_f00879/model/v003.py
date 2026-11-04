import math

def predict(probe):
    # Observations:
    # - Repeated x gives different y [E2,E3,E4,E5]: output is noisy.
    # - Mean depends on x, not constant [E5]: x=-8 mean ~ -1.15, x=-4 mean ~ -1.45,
    #   x=0 mean ~ 0.05, x=4 mean ~ 0.33. So mean rises with x, roughly.
    # - E4 small-x means: x=0.25 ~2.5, 0.75 ~1.87, 1.5 ~1.03, 2.5 ~1.75, 4 ~1.2,
    #   6 ~1.44, 8 ~1.02; negatives: -0.25 ~-1.67, -0.75 ~-0.11, -1.5 ~0.70.
    # - E3: x=0.5 ~2.57, 3 ~1.50, 5 ~0.01, 10 ~0.71, 20 ~0.35; negatives lower.
    # - E1 broad sweep: values scattered roughly in [-2,3], no clean trend visible,
    #   but large |x| values are noisy and near 0 mean.
    # - Best guess: mean ~ A*tanh(x/s) with A~1, s~4, plus small offset.
    #   Positives average higher, negatives lower. Noise sd ~1.
    # We predict the conditional mean.
    out = []
    for x in probe["x"]:
        try:
            x = float(x)
            m = 1.0 * math.tanh(x / 4.0) + 0.1
        except Exception:
            m = 0.1
        out.append(m)
    return {"y": out}
