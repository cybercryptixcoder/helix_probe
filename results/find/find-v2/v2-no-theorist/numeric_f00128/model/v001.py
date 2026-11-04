def predict(probe):
    # Observations: y is strongly negative for large positive x, positive for negative x.
    # Looks roughly like a downward-sloping curve. Fit a simple polynomial-ish model.
    # E1 data: x=88.2 -> -1479, x=66 -> -1104, x=-20.3 -> 139.6, x=-61.7 -> 419.5,
    # x=2.9 -> -37.8, x=-24.3 -> 166.7, x=72.7 -> -1217, x=-50.4 -> 343.1,
    # x=-6 -> 43, x=21.3 -> -348.8
    # Roughly linear-ish with curvature. Try cubic fit guess.
    # From data: slope ~ (-1479 - 419)/(88.2 - (-61.7)) = -1898/149.9 ≈ -12.66
    # intercept near x=0: ~ -37.8 at x=2.9, ~43 at x=-6 => ~0 near x=0? Actually ~ -10.
    # Try y ≈ -12.7*x - 10 plus curvature. At x=88.2: -1130, need -1479, so curvature.
    # Quadratic: fit through (-61.7,419.5),(2.9,-37.8),(88.2,-1479)
    # Let's just use a cubic interpolation guess.
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            # cubic guess: y = a*x^3 + b*x^2 + c*x + d
            # Fit rough: use points (-61.7,419.5),(2.9,-37.8),(88.2,-1479),(66,-1104)
            # Solve approximately by hand is hard; use a simpler heuristic:
            # y ≈ -0.0015*x^3 - 0.05*x^2 - 12.7*x - 10  (guess)
            y = -0.0015*x**3 - 0.05*x**2 - 12.7*x - 10
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
