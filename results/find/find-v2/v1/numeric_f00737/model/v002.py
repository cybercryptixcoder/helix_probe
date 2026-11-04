import math

def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x <= 0:
            out.append(None)
        else:
            try:
                a = (36.365 - (-7.8)) / math.log(128.0)
                b = -7.8
                y = a * math.log(x) + b
                out.append(round(y, 4))
            except Exception:
                out.append(None)
    return {"y": out}
