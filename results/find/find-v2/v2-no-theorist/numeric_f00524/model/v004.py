import math

def predict(probe):
    # f(x) = ceil(x) on a nonzero interval, else 0.0 [E2, E3, E4]
    # Positive interval: (0, ~4.35), since 4.3->5 but 4.4->0 [E4]
    #   lower cutoff <= 0.01 (0.01->1) [E4]; use 0 exclusive
    # Negative interval: [-4.0, 0), since -4.0->-4 but -4.5->0 [E4]
    #   ceil(-4.0) = -4 ok [E4]
    # Outside: 0.0 (signed zero sometimes, treat as 0.0) [E1, E2, E4]
    out = []
    for x in probe.get("x", []):
        try:
            if 0 < x < 4.35:
                out.append(float(math.ceil(x)))
            elif -4.0 <= x < 0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
