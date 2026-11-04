def predict(probe):
    # Large positive x -> -6.9 [E1, E2]
    # Large negative x -> -7.9 [E1, E2]
    # Small positive x gives a value between -7.9 and -6.9 [E1: x=2.9 -> -6.9015; E2: x=1.2 -> -7.7016]
    #   The closer to 0, the closer to -7.9; the larger, the closer to -6.9.
    #   Interpolate linearly between 0 and some threshold T: y = -7.9 + (x/T)*1.0
    #   From E2: x=1.2 -> -7.7016 => 1.2/T = 0.1984 => T ≈ 6.05
    #   From E1: x=2.9 -> -6.9015 => 2.9/T = 0.9985 => T ≈ 2.90 (inconsistent!)
    # ?: The two points don't fit a single linear ramp. Maybe a smooth curve.
    #   Try y = -7.9 + 1.0*(1 - exp(-x/k))? E2: 1.2 -> -7.7016 => 1-exp(-1.2/k)=0.1984 => k≈5.5
    #   E1: 2.9 -> -6.9015 => 1-exp(-2.9/k)=0.9985 => k≈0.34. Still inconsistent.
    # ?: Perhaps noise. Best guess: a ramp over [0, ~3] with midpoint behavior.
    #   Use linear ramp with T=3: x=1.2 -> -7.5 (obs -7.7016), x=2.9 -> -6.933 (obs -6.9015).
    #   Or T=2.9 fits E1 exactly, E2 off by 0.2. T=6 fits E2, E1 off by 0.9.
    #   Weighted: pick T≈3.5 as compromise. Mark as uncertain.
    # Negative small x: no data; assume -7.9 (same as negative) [no evidence otherwise]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                out.append(-7.9)
            elif x == 0:
                out.append(-7.9)  # ? guess
            else:
                T = 3.5  # ? uncertain threshold
                frac = min(x / T, 1.0)
                out.append(-7.9 + frac * 1.0)
        except Exception:
            out.append(None)
    return {"y": out}
