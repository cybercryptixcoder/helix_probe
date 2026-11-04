import math

def predict(probe):
    # Observations:
    # - For x <= -5.1: y = -0.7*x  [E1 x=-6 -> 4.2; E2 x=-40..-10; E8 x=-6.0..-5.1 -> 4.2]
    # - For -5.0 <= x <= 18.5: y ≈ -402.3 (constant, noisy)  [E2, E4 x=10..18, E6 x=-5..18.5, E8 x=-5.0..-2.5]
    # - For x >= 19: y = -16.8*x  [E4 x=19 -> -319.2; E2 x=20..100; E3; E5; E7]
    # Left break: sharp between -5.1 (4.2) and -5.0 (-402.3) [E8]
    # Right break: sharp between 18.5 (-402.5) and 19 (-319.2) [E6]
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -5.1:
                out.append(-0.7 * x)
            elif x < 19:
                out.append(-402.3)
            else:
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}
