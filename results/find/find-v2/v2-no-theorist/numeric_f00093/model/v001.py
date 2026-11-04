def predict(probe):
    # Model: f(x) is approximately a smooth, roughly linear/odd function of x.
    # Fit from E1: y ≈ -0.72*x + small offset, with mild nonlinearity.
    # Evidence: E1 shows y negative for positive x, positive for negative x,
    #   roughly proportional to x (e.g. x=88.2 -> -63.96, ratio -0.725;
    #   x=-61.7 -> 40.81, ratio -0.662; x=66 -> -59.96, ratio -0.909).
    # The MLP approximates a monotone decreasing function; use linear fit.
    # Best linear fit through E1 points: y ≈ a*x + b.
    # Compute least squares from E1 data (hardcoded coefficients).
    # a ≈ -0.72, b ≈ 1.5 (rough).  [E1]
    a = -0.72
    b = 1.5
    out = []
    for x in probe.get("x", []):
        try:
            out.append(a * float(x) + b)
        except Exception:
            out.append(None)
    return {"y": out}
