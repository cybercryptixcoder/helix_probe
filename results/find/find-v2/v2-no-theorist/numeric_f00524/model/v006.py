import math

def predict(probe):
    # f(x) = ceil(x) on (0, 4.35] [E2, E4, E6, E8]
    #   positive cutoff: 4.35->5 but 4.36->0 [E6, E8]
    # f(x) = ceil(x) on [-4.35, 0) [E4, E6, E8]
    #   -4.35->-4 but -4.36->-0.0 [E8]; so interval is [-4.35, 0)
    # Outside: 0.0 [E1, E2, E4, E5, E6, E7, E8]
    out = []
    for x in probe.get("x", []):
        try:
            if 0 < x <= 4.35:
                out.append(float(math.ceil(x)))
            elif -4.35 <= x < 0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
