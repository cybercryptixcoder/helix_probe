import math

def predict(probe):
    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        if abs(x) < 4.36:
            ys.append(float(math.ceil(x)))
        else:
            ys.append(0.0)
    return {"y": ys}
