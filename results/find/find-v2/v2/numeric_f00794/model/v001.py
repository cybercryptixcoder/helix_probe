import math

def predict(probe):
    # Observations:
    # - Outputs are mostly small values in [-1,1], except at x=0 where y≈475.36 [E2]
    # - Same x gives different y across experiments (E1 vs E2 for 88.2, 66.0, etc.) [E1,E2]
    #   => f is NOT a pure function of x alone; there is hidden state/noise/position dependence.
    # - Values look like sin/cos-like bounded oscillation for most x [E1,E2]
    # - x=0 is a special spike (~475) [E2]
    # Best guess: f(x) = sin(x) + spike at x=0, with noise/state making exact values unpredictable.
    # Since exact values aren't reproducible, predict the deterministic part.
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(475.3578)  # spike at zero [E2]
            else:
                out.append(math.sin(x))
        except Exception:
            out.append(None)
    return {"y": out}
