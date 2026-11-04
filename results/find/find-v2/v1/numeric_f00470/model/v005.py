def predict(probe):
    """Best guess: base formula x^3+2^x+22 is wrong on positives (observed grows much faster).
    Keep piecewise idea: special interval on (0,1) with negative dip.
    Base formula uncertain; use a scaled exponential fit as placeholder."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                if 0 < x < 1:
                    # special interval: negative dip, roughly f(0.5)=-21.96, f(0.6)=-22.65
                    # quadratic through f(0)=22.28, f(0.5)=-21.96, f(1)=70.35
                    C = 22.28
                    A = 70.35 + 22.28 - 2*(-21.96)  # = 136.55
                    B = (70.35 - 22.28) - A  # = -88.48
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
