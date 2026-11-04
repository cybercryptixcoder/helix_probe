import math

def predict(probe):
    # Beliefs:
    # - Output is noisy around an x-dependent mean [E2-E15].
    # - Mean is ~ -1 for negative x (roughly flat), ~ +2 for positive x (roughly flat) [E11,E12,E13,E14].
    # - Near zero the mean transitions smoothly; at x=-0.5 mean ~ -0.2, x=0.5 mean ~ +1.9 [E13,E14].
    # - No decay at large positive x: mean stays ~1 at 10-80 [E15]; large negative stays ~ -1 [E1,E6].
    # - Noise sd ~ 1.2, so single samples scatter widely [all].
    out = []
    for x in probe["x"]:
        try:
            x = float(x)
            # smooth step from -1 to +2 centered at 0, width ~1
            m = -1.0 + 3.0 / (1.0 + math.exp(-x / 0.5))
        except Exception:
            m = 0.0
        out.append(m)
    return {"y": out}
