def predict(probe):
    # f is a smooth bump centered near x=0, positive for small |x|, ~0 far out [E1]
    # Peak ~0.39 at x=0, falls to ~0.12 at x=2, ~0.01 at x=4, ~0 beyond |x|>=8 [E1]
    # Asymmetric: left side smaller (0.197 at -1 vs 0.255 at 1; 0.0575 at -2 vs 0.12 at 2) [E1]
    # Slight negative tail on far left (-0.004 at -128) [E1]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            # Gaussian-ish bump, asymmetric width and amplitude
            if x >= 0:
                y = 0.39 * math.exp(-(x/1.9)**2)
            else:
                y = 0.39 * math.exp(-(x/1.5)**2)
            # small negative baseline far out
            y -= 0.004 * math.exp(-((abs(x)-128)/40.0)**2) if abs(x) > 60 else 0.0
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
