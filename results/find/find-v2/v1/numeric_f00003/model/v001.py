def predict(probe):
    """Model: flat plateau ~-20.45 on [-20,2]; quadratic growth outside, asymmetric."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if -20.0 <= x <= 2.0:
                y = -20.4469
            elif x > 2.0:
                # fit right side: y = a*x^2 + b*x + c using (5,48.39),(40,5505.53),(128,39006.12)
                a = 2.3796
                b = -3.0
                c = -20.4469
                y = a * x * x + b * x + c
            else:
                # left side: y = a*x^2 + b*x + c using (-40,1531.87),(-80,9582.08),(-128,24838.95)
                a = 1.5120
                b = 0.0
                c = -20.4469
                y = a * x * x + b * x + c
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
