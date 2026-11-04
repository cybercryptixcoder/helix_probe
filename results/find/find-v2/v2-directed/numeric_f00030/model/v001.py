def predict(probe):
    # Observations [E1]: y is smooth, roughly -1.48 at x=-120 rising to a peak
    # near x=0 (-1.756) then falling symmetrically to -1.52 at x=120.
    # The shape is a shallow downward-opening parabola (concave), with a small
    # dip/notch near x=0. Fit: y ≈ a + b*x^2 with a≈-1.756, b≈1.9e-5.
    # Check: x=±120 -> -1.756+1.9e-5*14400 = -1.756+0.274 = -1.482 ✓
    #        x=±60  -> -1.756+1.9e-5*3600  = -1.756+0.068 = -1.688 (obs -1.606/-1.580)
    # Hmm, quadratic overshoots at mid-range; the curve is flatter than a parabola
    # in the middle and steeper at the ends — more like a cosine / smooth bump.
    # Try y = c - A*(1-cos(pi*x/120))/2? At x=0 -> c=-1.756; x=120 -> c-A=-1.5207
    # so A=0.235. At x=60: c - A*(1-cos(pi/2))/2 = -1.756-0.235*0.5=-1.874 (obs -1.606)
    # Too steep. The observed curve is nearly linear away from center with a
    # rounded peak — like -1.756 + k*|x|^p with small p? 
    # Fit endpoints: -1.4799 at -120, -1.5207 at 120 (asymmetry ~0.04, likely noise).
    # Midpoint x=60: -1.606. Linear from center: -1.756 + (0.235/120)*60 = -1.638.
    # Observed -1.606 is above linear -> curve is slightly convex (flatter near center).
    # Best simple model: y = -1.756 + 0.00196*|x|^1.15 (approx), plus small dip at 0.
    # The x=0 value (-1.756) is notably below neighbors (-1.6729 at -5, -1.6853 at 5),
    # suggesting a narrow notch/dip at x=0.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            # Base trend: shallow V/U shape, peak (minimum y) at 0.
            # Use |x|^1.1 scaled to hit endpoints.
            base = -1.756 + 0.00196 * (abs(x) ** 1.1)
            # Narrow dip at x=0 (notch): observed -1.756 vs ~-1.68 nearby.
            dip = -0.06 * math.exp(-(x * x) / 8.0)
            y = base + dip
            out.append(round(y, 4))
        except Exception:
            out.append(None)
    return {"y": out}
