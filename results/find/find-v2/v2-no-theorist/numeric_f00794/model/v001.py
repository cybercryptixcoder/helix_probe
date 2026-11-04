import math

def predict(probe):
    # Observations:
    # - f(x) is mostly a small pseudo-random-looking value in [-1,1] for most x [E1, E2]
    # - At x=0, f(0)=473.8752, a huge spike [E2]
    # - Elsewhere values look like noise / hash-like, not smooth [E1, E2]
    # Hypothesis: f(x) = sin(something) or hash-like, with a special spike at x=0.
    # Since no clear structure, best guess: pseudo-random in [-1,1], except x=0 -> 473.8752.
    # ? We can't reproduce the exact hash, so predict a deterministic pseudo-random value.
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(473.8752)
            else:
                # deterministic pseudo-random in [-1,1] based on x
                v = math.sin(x * 12.9898) * 43758.5453
                v = v - math.floor(v)  # fractional part in [0,1)
                out.append(round(v * 2 - 1, 4))
        except Exception:
            out.append(None)
    return {"y": out}
