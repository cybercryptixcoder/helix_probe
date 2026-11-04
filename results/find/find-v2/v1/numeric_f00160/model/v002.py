import math

def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            out.append(None)
            continue
        if math.isnan(xf) or math.isinf(xf):
            out.append(None)
            continue
        try:
            out.append(float(math.floor(xf) - 39))
        except Exception:
            out.append(None)
    return {"y": out}
