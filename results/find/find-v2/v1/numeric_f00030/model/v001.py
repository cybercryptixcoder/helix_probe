def predict(probe):
    """Rough model: broad parabola centered near 0 with a small linear tilt."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Parabola centered near 0: min ~ -1.79 at x~0, rising to ~ -1.47 at |x|=128
            # curvature a: at x=128, a*128^2 = (-1.47) - (-1.79) = 0.32 -> a ~ 1.95e-5
            a = 1.95e-5
            base = -1.79 + a * x * x
            # small linear tilt: f(128) ~ -1.51, f(-128) ~ -1.47 -> slope ~ (-1.51+1.47)/256
            tilt = -1.56e-4 * x
            ys.append(base + tilt)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
