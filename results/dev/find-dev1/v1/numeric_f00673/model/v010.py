def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            out.append(16.79 * ax)
        except Exception:
            out.append(None)
    return {"y": out}
