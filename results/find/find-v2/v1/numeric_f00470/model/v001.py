def predict(probe):
    """Best guess: f(x) ≈ x^3 + 2^x + 22, but known to be wrong at negative x."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                y = x**3 + 2.0**x + 22.0
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
