def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            if x >= 0:
                # Positive side: exact linear law 11.0 - 16.9*x for large x,
                # softened near zero. Use a wider softening so mid-range
                # (x~2-4) sits a few units below the linear law as observed.
                b = -16.9
                c_lin = 11.0
                # softened version: g = b*x*|x|/(|x|+k) + c_lin*x/(|x|+k) blended
                # Simpler: linear law minus a decaying correction.
                # correction ~ 2.5*exp(-x/6) keeps x=2..4 a few below linear.
                lin = c_lin + b * x
                corr = 2.6 * (1.0 / (1.0 + x / 1.5))  # ~2.6 near 0, ~0.9 at x=3
                # near zero we need f(0)=5.42, f(0.5)=2.12, f(1)=-5.32
                # blend a steep near-zero form with the linear law
                k = 0.55
                soft = 5.42 + b * x * x / (x + k)
                w = x / (x + 1.2)  # 0 at x=0, ->1 for large x
                val = (1 - w) * soft + w * (lin - corr)
                ys.append(val)
            else:
                # Negative side: exact linear law -6.8*x + 5.42, softened near zero
                b = -6.8
                c = 5.42
                ax = abs(x)
                g = b * x * ax / (ax + 0.6)
                ys.append(g + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
