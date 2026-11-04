def predict(probe):
    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        # Positive branch: quadratic-ish fit
        if x > 0:
            return 10.4 * x + 0.5 * x * x
        # Zero spike
        if x == 0:
            return -383.12
        # Negative branch: linear, with special interval near [-2,-1]
        if -2.0 <= x <= -1.0:
            # interpolate between observed -2 -> -13.52 and -1 -> -11.21
            t = (x - (-2.0)) / 1.0
            return -13.52 + t * (-11.21 - (-13.52))
        return 1.4 * x

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
