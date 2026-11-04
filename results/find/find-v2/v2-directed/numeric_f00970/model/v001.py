import math

def predict(probe):
    # Observations from E1:
    # For |x| >= 4: y is small (~ -2 to 1), roughly noisy around 0.
    # For |x| <= 2: y is large (~10-13), roughly noisy around 12.
    # Sharp transition between |x|=2 and |x|=4.
    # Values: x=-2 -> 10.9, x=-1 -> 13.3, x=-0.5 -> 12.35, x=0 -> 12.05,
    #         x=0.5 -> 11.56, x=1 -> 12.65, x=2 -> 10.42
    # Outside: x=-4 -> -0.048, x=4 -> 0.895, x=8 -> -0.056, ...
    # Model: inside |x| < 3 (approx), output ~12; outside, output ~0.
    # Boundary between 2 and 4; pick 3 as midpoint guess.
    # Noise is present, so predict the mean.
    out = []
    for x in probe.get("x", []):
        try:
            if abs(x) < 3:
                out.append(12.0)
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
