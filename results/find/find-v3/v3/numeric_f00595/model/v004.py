import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - For x >= 1: output = floor(x) + 1   [E2: 1.5->2, 3.2->4; E3: 1.2->2, 65.5->66; E6: 1.01->2, 1.99->2]
    # - For x <= -1: output = ceil(x) - 1  [E2: -1.5->-3, -3.2->-5; E3: -55.8->-57; E4: -2.0->-3]
    # - For -1 < x < 1: output = 1 if x >= 0 else -2   [E2: 0.5->1, -0.5->-2, 0.1->1, -0.1->-2; E4: -0.9->-2, -0.1->-2, 0.0->-1, 0.9->1]
    #   Note: E4 shows 0.0 -> -1, so zero is a special case.
    # - For x in (-1, 1), nonzero: sign-based (positive -> 1, negative -> -2)
    # - x = 0 -> -1  [E4]
    # - For x >= 1: floor(x)+1; for x <= -1: ceil(x)-1
    # - At x = 1.0? Not directly tested; E6 has 1.01->2, E2 1.5->2. Assume x>=1 rule.
    # - At x = -1.0? Not directly tested; E2 -1.5->-3, E4 -1.1->-3. Assume x<=-1 rule.
    # - Large values: E2 100->101, -100->-101; E3 123.6->124; consistent with floor/ceil rules.
    
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
        if v > 0:
            if v < 1:
                y.append(1.0)
            else:
                y.append(float(math.floor(v) + 1))
        elif v < 0:
            if v > -1:
                y.append(-2.0)
            else:
                y.append(float(math.ceil(v) - 1))
        else:  # v == 0
            y.append(-1.0)
    return {"y": y}
