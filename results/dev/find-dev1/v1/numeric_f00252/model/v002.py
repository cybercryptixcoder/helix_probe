import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None or x <= 0:
                out.append(None)
            else:
                try:
                    val = 1.1 + 141.0873 * math.log(x, 2)
                    out.append(round(val, 4))
                except Exception:
                    out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
