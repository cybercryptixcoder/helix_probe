def predict(probe):
    """Best guess: f(x) ≈ (x-1)^3 + 2^x + 22, known to be wrong at negative x."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                y = (x - 1.0)**3 + 2.0**x + 22.0
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
