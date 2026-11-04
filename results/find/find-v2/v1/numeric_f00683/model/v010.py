def predict(probe):
    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        if x == 0:
            return -383.12
        if x > 0:
            if x < 1.0:
                return 10.4 * x - 3.2
            else:
                return 13.1 * x - 5.5
        return 1.4 * x - 10.0

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
