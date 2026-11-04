def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            # Mean of f: roughly linear 16.79*|x| across the whole domain,
            # with slight sublinearity at very large |x|.
            if ax > 64:
                out.append(16.79 * ax - 0.001 * (ax - 64) ** 2)
            else:
                out.append(16.79 * ax)
        except Exception:
            out.append(None)
    return {"y": out}
