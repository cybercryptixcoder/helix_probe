def predict(probe):
    # f is monotone decreasing, roughly odd, with a smooth sigmoid-like shape [E1, E2]
    # Slope near 0 is steep: f(1)-f(-1) ≈ -6.87, f(2)-f(-2) ≈ -13.0 [E2]
    # Slope flattens at large |x|: f(100)-f(80) ≈ 10.65 over 20 units, f(120)-f(100) ≈ 3.6 [E2]
    # f(0) ≈ -8.83, not 0, so there's a negative offset [E2]
    # Odd-ish: f(-x) ≈ -f(x) - 17.7 (offset ~ -8.8 each side) [E2]
    # Model: f(x) = c - A * tanh(x / s)  (smooth saturating odd shape)
    # Fit from E2: at x=0, f=-8.83 -> c=-8.83
    # At large x: f(120)=-69.68, f(-100)=61.21 -> A ≈ (61.21+69.68)/2 ≈ 65.4, c≈-4.2
    # Use c=-8.83, A=61, s≈35 (tuned to match mid-range curvature)
    import math
    c = -8.83
    A = 61.0
    s = 35.0
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            out.append(c - A * math.tanh(x / s))
        except Exception:
            out.append(None)
    return {"y": out}
