import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - For x >= 1: output = floor(x) + 1   [E2: 1.5->2, 3.2->4; E3: 1.2->2, 65.5->66; E6: 1.01->2, 1.99->2; E8: 2.5->3, 3.99->4, 4.01->5, 10.5->11]
    # - For x <= -1: output = ceil(x) - 1  [E2: -1.5->-3, -3.2->-5; E3: -55.8->-57; E4: -2.0->-3; E8: -1.5->-3, -2.5->-4, -3.99->-5, -4.01->-6, -10.5->-12; E10: -1.0->-2, -1.25->-3, -1.75->-3, -1.01->-3]
    # - For -1 < x < 0: output = -2  [E2: -0.5->-2, -0.1->-2; E4: -0.9->-2; E8: -0.99->-2, -0.5->-2; E10: -0.5,-0.25,-0.75,-0.99,-0.001 all ->-2]
    # - For 0 < x < 1: output = 1  [E2: 0.5->1, 0.1->1; E4: 0.9->1; E8: 0.99->1, 0.01->1, 0.5->1; E10: 0.999->1, 0.001->1]
    # - x = 0 -> -1  [E4]
    # - Boundary at x = -1.0 belongs to the x <= -1 rule: -1.0 -> -2  [E10]
    # - Boundary at x = 1.0 belongs to the x >= 1 rule: 1.0 -> 2  [E10]
    x = probe["x"]
    y = []
    for v in x:
        if v is None:
            y.append(None)
            continue
        try:
            v = float(v)
        except Exception:
            y.append(None)
            continue
        if math.isnan(v) or math.isinf(v):
            y.append(None)
            continue
        if v >= 1:
            y.append(float(math.floor(v) + 1))
        elif v <= -1:
            y.append(float(math.ceil(v) - 1))
        elif v > 0:
            y.append(1.0)
        elif v < 0:
            y.append(-2.0)
        else:  # v == 0
            y.append(-1.0)
    return {"y": y}
