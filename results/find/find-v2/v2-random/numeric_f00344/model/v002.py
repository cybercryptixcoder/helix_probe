def predict(probe):
    # Main branch: y = -1.2 x^4 - 3.2 x^3 for most x [E1,E2,E3,E4]
    # Exception region: for x below about -100, y is clamped to a constant -24973124.6 [E3,E4]
    #   E3: x=-102.2 -> -24973124.5844
    #   E4: x=-124.4 -> -24973124.6302
    #   Both nearly identical => saturation/clamp at ~ -2.4973e7
    # Boundary: unknown between -61.7 (normal) and -102.2 (clamped) [E1,E3]
    #   Guess threshold at x <= -100 (only evidence is -102.2 and -124.4 clamped,
    #   -61.7 normal). Marked uncertain "?".
    x = probe["x"]
    out = []
    for v in x:
        try:
            if v <= -100:
                out.append(-24973124.6)
            else:
                out.append(-1.2 * v**4 - 3.2 * v**3)
        except Exception:
            out.append(None)
    return {"y": out}
