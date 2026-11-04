def predict(probe):
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            lin = 16.79 * ax
            if ax >= 1.0:
                out.append(lin)
            else:
                # Near-zero region: erratic, roughly rising from ~0 at 0 to ~16.8 at 1.
                # Use a smooth ramp; individual fluctuations are unpredictable.
                base = 16.79 * (ax ** 1.05)
                out.append(base)
        except Exception:
            out.append(None)
    return {"y": out}
