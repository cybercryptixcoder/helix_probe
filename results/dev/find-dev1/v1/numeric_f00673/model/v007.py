def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            if ax >= 1.0:
                # Slight sublinearity at very large |x|
                if ax > 64:
                    out.append(16.79 * ax - 0.001 * (ax - 64) ** 2)
                else:
                    out.append(16.79 * ax)
            else:
                # Noisy special region: best estimate is the mean ramp.
                out.append(16.79 * ax)
        except Exception:
            out.append(None)
    return {"y": out}
