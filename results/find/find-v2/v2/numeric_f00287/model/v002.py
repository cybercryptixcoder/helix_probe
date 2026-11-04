import math

def predict(probe):
    # Observations:
    # - For x <= -6: y = -0.7*x  [E1 x=-6 -> 4.2; E2 x=-40..-10 -> 28..7]
    # - For -5 <= x <= 18: y ≈ -402.3 (constant, noisy)  [E2, E1 x=2.9, E4 x=10..18]
    # - For x >= 19: y = -16.8*x  [E4 x=19 -> -319.2 = -16.8*19; E2 x=20..100; E3]
    # Left break between -6 (linear) and -5 (middle): guess -5.5
    # Right break between 18 (middle) and 19 (linear): guess 18.5
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -5.5:
                out.append(-0.7 * x)
            elif x < 18.5:
                out.append(-402.3)
            else:
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}
