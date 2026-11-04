def predict(probe):
    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        if x == 0:
            return -383.12
        if x > 0:
            # small positive: linear 10.4x - 3.2; large: quadratic 10.4x + 0.5x^2
            # transition: at x=1.5 both give 12.4 vs 16.7; observed 14.15
            # use quadratic for x>=1, linear-ish for x<1
            if x >= 1.0:
                return 10.4 * x + 0.5 * x * x
            else:
                return 10.4 * x - 3.2
        # x < 0: linear with slope 1.4 and intercept -10
        return 1.4 * x - 10.0

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
