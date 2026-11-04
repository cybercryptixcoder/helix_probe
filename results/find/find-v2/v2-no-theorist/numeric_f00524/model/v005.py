import math

def predict(probe):
    # f(x) = ceil(x) on (0, 4.35) [E2, E4, E6]
    #   upper cutoff: 4.35->5 but 4.36->0 [E6]; use x <= 4.35
    #   lower: arbitrarily small positive -> 1 [E6]; use x > 0
    # f(x) = ceil(x) on [-4.4, 0) [E4, E6]
    #   -4.4->-0.0 (zero) but -4.3->-4 [E6]; so interval is [-4.4, 0)
    #   ceil(-4.4) = -4, but observed 0.0 at -4.4 -> boundary is exclusive of -4.4
    #   Actually -4.4 gives -0.0, so interval is (-4.4, 0); use x > -4.4
    # Outside: 0.0 [E1, E2, E4, E5, E6]
    out = []
    for x in probe.get("x", []):
        try:
            if 0 < x <= 4.35:
                out.append(float(math.ceil(x)))
            elif -4.4 < x < 0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
