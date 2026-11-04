import math

def predict(probe):
    # Observations:
    # E2: for x in [-128,-16] step 8, y decreases smoothly and nearly linearly:
    #     from 0.0479 at -128 down to 0.0149 at -16. Slope ~ -0.00029 per unit.
    #     This is a slow linear-ish trend, NOT a sinusoid [E2].
    # E2: at x=-8 y jumps to 0.031, x=0 -> -0.0008, x=8 -> -0.03, x=16 -> -0.0126, x=24 -> 0.0003.
    #     Behaviour changes near x ~ -12: inside a special interval the function oscillates.
    # E1: random points: x=2.9 -> -0.0469, x=-6 -> 0.0471, x=21.3 -> -0.0017, x=-20.3 -> 0.0163.
    #     These are consistent with an oscillatory region roughly on [-12, 24] plus the linear trend outside.
    # Model: linear trend y = a + b*x everywhere, plus an oscillation term active on an interval.
    # Fit linear trend from E2 outer points: at x=-128 y=0.0479, x=-16 y=0.0149 -> b=-0.000295, a=0.0102.
    # Inside interval, oscillation: from E1/E2, sign flips suggest period ~ 16-20, amplitude ~0.03.
    # Use y = a + b*x + A*sin(w*x + p) * window, window=1 inside [-12,24], else 0.
    a = 0.0102
    b = -0.000295
    A = 0.035
    w = 2*math.pi/18.0
    p = 0.0
    out = []
    for x in probe["x"]:
        try:
            base = a + b*x
            if -12.0 <= x <= 24.0:
                y = base + A*math.sin(w*x + p)
            else:
                y = base
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
