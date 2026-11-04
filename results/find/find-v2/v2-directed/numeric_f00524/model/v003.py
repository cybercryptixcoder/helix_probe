def predict(probe):
    # f(x) = x for |x| <= 2 [E1, E2]
    # f(x) = round-half-away-from-zero(x) for 2 < |x| <= 4.25-ish [E2, E3]
    # f(x) = 0 for |x| > ~4.25 [E1, E3]
    # Boundary: -4.25 -> -4 (rounding), -4.5 -> 0; +4.25 -> 5, +4.5 -> 0.
    # So rounding region is |x| <= 4.25 (inclusive), zero beyond. [E3]
    # Note asymmetry: -4.25->-4 but +4.25->5, consistent with round-half-away.
    out = []
    for x in probe.get("x", []):
        try:
            if -2 <= x <= 2:
                out.append(float(x))
            elif -4.25 <= x <= 4.25:
                import math
                out.append(float(math.floor(x + 0.5)) if x >= 0 else float(math.ceil(x - 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
