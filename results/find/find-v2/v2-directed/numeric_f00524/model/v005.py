def predict(probe):
    # f(x) = round-half-away-from-zero(x) for |x| <= 4.3 [E2,E3,E4,E5]
    # f(x) = 0 for |x| >= 4.4 (sharp cutoff) [E1,E3,E5]
    # Boundary: -4.3 -> -4, +4.3 -> 5, |x|>=4.4 -> 0 [E5]
    # Rounding is symmetric: f(-x) = -f(x) [E2,E3,E4,E5]
    # Note: +4.3 rounds to 5 (not 4) — round-half-away gives 4, so
    #   positive side seems to round up (ceil-like) near boundary [E5]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if -4.3 <= x <= 4.3:
                if x >= 0:
                    out.append(float(math.floor(x + 0.5)))
                else:
                    out.append(float(math.ceil(x - 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
