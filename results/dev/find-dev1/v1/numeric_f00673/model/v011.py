def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            mean = 16.79 * ax
            # relative noise amplitude: larger near zero, ~0.5-1% at large |x|
            # interpolate: at ax~0.1 -> ~0.30, ax~0.5 -> ~0.08, ax~1.2 -> ~0.05, large -> ~0.007
            if ax < 0.05:
                rel = 0.35
            elif ax < 1.0:
                # from 0.35 at 0.05 down to ~0.06 at 1.0
                rel = 0.35 - (0.35 - 0.06) * (ax - 0.05) / 0.95
            elif ax < 2.0:
                rel = 0.06 - (0.06 - 0.03) * (ax - 1.0) / 1.0
            else:
                # decay toward ~0.007 at large |x|
                rel = 0.03 * (2.0 / ax) ** 0.5
                if rel < 0.007:
                    rel = 0.007
            out.append(mean)
        except Exception:
            out.append(None)
    return {"y": out}
