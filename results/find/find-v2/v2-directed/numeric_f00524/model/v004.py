def predict(probe):
    # f(x) = round-half-away-from-zero(x) for |x| <= 4.25 [E2, E3, E4]
    # f(x) = 0 for |x| > 4.25 [E1, E3]
    # Rounding region boundary: -4.25 -> -4, +4.25 -> 5, |x|>=4.5 -> 0 [E3]
    # Interior is also rounded (not linear): f(1.5)=2, f(0.5)=1, f(-0.5)=-0 [E4]
    # So the whole |x|<=4.25 region is just rounding. [E4]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if -4.25 <= x <= 4.25:
                out.append(float(math.floor(x + 0.5)) if x >= 0 else float(math.ceil(x - 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
