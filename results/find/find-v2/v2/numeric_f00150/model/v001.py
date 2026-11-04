def predict(probe):
    # Ordinary inputs: y = 0.2*x^5 exactly [E8, E12, E18, E20, E22]
    #   ratio y/x^5 = 0.2 confirmed across magnitudes 2..128 [E22, E18]
    # Small-|x| anomaly: for |x| < ~1.5 the law breaks; there is a smooth
    #   region near |x|~0.5-1.5 and a flat ~5 near x=0 [E10, E16, E18, E20]
    #   At x=0.5 y=2.9625, x=0.75 y=1.5342, x=1.0 y=-0.2, x=1.5 y=-2.0
    #   For very small |x| (0.002..0.05) y ~ 5 (odd-ish, sign flips) [E10]
    #   Negative x in anomaly: y=0 for x=-0.5,-0.25,-0.05,-0.005,-0.002 [E10]
    #   but x=-0.9,-1.1 give 0 and -12.17 [E14] -> sign-dependent
    # Best guess: anomaly is a smooth bump; model it piecewise.
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax >= 1.5:
                y = 0.2 * x**5
            elif x > 0:
                # smooth positive-side anomaly, roughly matching E16/E18/E20
                # fit: y ~ 5*exp(-(x/0.9)^2) - something; use interpolation-ish
                # Points: 0.3:3.83,0.5:2.96,0.6:2.44,0.75:1.53,0.9:0.50,1.0:-0.2,
                # 1.1:-1.71,1.2:-2.76,1.3:-3.34,1.4:-3.20,1.5:-2.0
                # Use a smooth cubic-ish guess via cosine blend to 0.2*x^5 at 1.5
                t = x / 1.5
                base = 0.2 * x**5
                # bump term that vanishes at x=1.5
                bump = 5.0 * math.exp(-(x/0.75)**2) - 3.0*x
                y = base + (1 - t) * bump
            else:
                # negative side: y=0 for small |x|, then -12.17 at -1.1
                if ax < 0.6:
                    y = 0.0
                else:
                    t = ax / 1.5
                    y = (1 - t) * (-12.1679) * (ax - 0.6) / 0.5 if ax < 1.1 else 0.2 * x**5
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
