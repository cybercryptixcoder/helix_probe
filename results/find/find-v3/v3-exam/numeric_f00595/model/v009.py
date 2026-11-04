import math

def predict(probe):
    # Model of the black box f(x).
    #
    # - Outside the anomalous interval: f(x) = floor(x)+1 for x>0, floor(x)-1 for x<=0.
    #   [E1..E19, E21, E23]
    # - Anomalous noisy interval: outputs are small negative values (~-0.3..-0.7), noisy.
    #   Lower boundary: E24 shows 33.3 -> 34 (normal), 33.35 -> -0.4888 (noisy).
    #     So lower boundary is in (33.3, 33.35]. Use 33.35.
    #   Upper boundary: E20 shows 42.0 -> -0.3499 (noisy), 42.05 -> 43 (normal).
    #     So boundary in (42.0, 42.05]. Use 42.05.
    #   Inside: noisy. Return -0.5 as best guess (mean-ish). Cannot predict exact.
    x = probe["x"]
    ys = []
    for v in x:
        if v is None:
            ys.append(None)
            continue
        if 33.35 <= v < 42.05:
            ys.append(-0.5)
        else:
            if v > 0:
                ys.append(float(math.floor(v) + 1))
            else:
                ys.append(float(math.floor(v) - 1))
    return {"y": ys}
