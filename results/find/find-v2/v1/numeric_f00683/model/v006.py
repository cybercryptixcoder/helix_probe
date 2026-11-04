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
            elif x < 2.0:
                # erratic region; best guess: quadratic plus noise
                return 10.4 * x + 0.5 * x * x
            else:
                return 10.4 * x + 0.5 * x * x
        # x < 0: approximate line with scatter; use 1.4x - 10 as base
        return 1.4 * x - 10.0

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
