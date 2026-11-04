def predict(probe):
    """Best guess: f(x)=x^3+2^x+22 fails on positives; values grow much faster.
    Keep piecewise idea: special interval on (0,1) with negative dip.
    Base formula uncertain; use a scaled exponential fit as placeholder."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                if 0 < x < 1:
                    # special interval: negative dip, roughly f(0.5)=-21.96
                    # crude interpolation: f(0)=22.28, f(0.5)=-21.96, f(1)=70.35
                    # quadratic through these three points
                    a = 2*(22.28 + 70.35) - 4*(-21.96)  # placeholder
                    # fit quadratic p(x)=A x^2 + B x + C with p(0)=22.28, p(0.5)=-21.96, p(1)=70.35
                    C = 22.28
                    A = 2*(70.35 + 22.28) - 4*(-21.96)
                    A = 70.35 + 22.28 - 2*(-21.96)  # = 70.35+22.28+43.92 = 136.55
                    B = (70.35 - 22.28) - A  # = 48.07 - 136.55 = -88.48
                    y = A*x*x + B*x + C
                else:
                    # base formula: try x^3 + 2^x + 22 (known wrong on positives but best guess)
                    y = x**3 + 2.0**x + 22.0
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
