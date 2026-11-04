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
                # Near-zero region: mostly monotone rise from ~0.3 at 0 to ~16.8 at 1,
                # with small erratic dips near 0.04-0.08 and 0.15-0.22.
                # Use a smooth ramp anchored at f(0)~0.3 and f(1)~16.8.
                base = 0.3 + (16.79 - 0.3) * (ax ** 1.1)
                # Small dip near 0.05
                dip1 = 0.6 * math.exp(-((ax - 0.05) / 0.03) ** 2)
                # Small dip near 0.18
                dip2 = 1.5 * math.exp(-((ax - 0.18) / 0.05) ** 2)
                val = base - dip1 - dip2
                if val < 0:
                    val = 0.0
                out.append(val)
        except Exception:
            out.append(None)
    return {"y": out}
