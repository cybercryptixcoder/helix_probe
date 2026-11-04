import math

def predict(probe):
    # For x < -75: y ≈ -0.6/x (tiny positive tail) [E1,E3,E4,E5]
    #   e.g. x=-128→0.0046, -110→0.0053, -95→0.0062, -80→0.0074
    # Elsewhere: oscillating ~0.1 amplitude, high-ish frequency [E2,E4]
    #   near 0 rapid sign flips (period ~2-4) [E4]
    #   noisy; best guess sinusoid [E2,E4]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x < -75:
                ys.append(-0.6 / x)
            else:
                ys.append(0.1 * math.sin(1.5 * x))
        except Exception:
            ys.append(None)
    return {"y": ys}
