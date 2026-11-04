import math

def predict(probe):
    # Model hypothesis based on E1:
    # Outputs are small, roughly in [-0.12, 0.12], and vary non-monotonically.
    # Large |x| (e.g. -93.6, -104, -120.7) give tiny positive values (~0.005-0.006),
    # suggesting a decaying tail like 1/x or sin(x)/x.
    # Near x=0 (e.g. -1.2) output is largest (~0.116), consistent with sin(x)/x -> 1.
    # Sign flips: x=-62.7 -> -0.0815, x=-12.9 -> +0.0972, x=38.8 -> +0.0677.
    # Try sin(x)/x scaled: sin(-1.2)/(-1.2) = 0.777; observed 0.1162 -> scale ~0.15.
    # Check x=-62.7: sin(-62.7)/(-62.7) = -0.0159; *0.15 = -0.0024, observed -0.0815. Not matching.
    # Try sin(x)/x with different scale or sin(x^2)/x? Uncertain. Use sin(x)/x as best guess.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x == 0:
                ys.append(0.15)
            else:
                ys.append(0.15 * math.sin(x) / x)
        except Exception:
            ys.append(None)
    return {"y": ys}
