import math

def predict(probe):
    # Beliefs (revised after E12-E16):
    # The output is a smooth function of x with amplitude growing with |x|,
    # but the oscillation is NOT sin(x/30). Looking at sign patterns:
    # - Large positive x (>~60) tends to give positive y [E7,E9,E10,E11,E14,E16]
    # - Large negative x (<~-60) tends to give negative y [E4,E5,E8,E13,E14,E15]
    # - Small |x| (<~30) gives small |y|, sign varies [E4,E6,E7,E12,E13]
    # So y ~ sign(x) * g(|x|) with oscillation. Try y = tanh-ish ramp * sin.
    # Actually simplest: y grows roughly linearly with x but with oscillation.
    # Fit: y ≈ 0.02*x + 1.5*sin(x/25)?? Let's try y = a*x*sin(x/b) style.
    # From data: at x=127 y~0.1, x=119 y~0.6-0.9, x=105 y~-0.3,
    # x=88 y~0.7-1.4, x=77 y~3.4, x=44 y~1.3, x=24 y~0.9.
    # Positive x mostly positive y. Negative x mostly negative y.
    # Model: y = 0.9*sin(x/18) + 0.015*x  (odd-ish, growing amplitude)
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # odd-ish oscillatory with growing amplitude
            y = 0.9 * math.sin(x / 18.0) + 0.015 * x
            ys.append(y)
        return {"y": ys}
    except Exception:
        try:
            return {"y": [None for _ in probe.get("x", [])]}
        except Exception:
            return {"y": []}
