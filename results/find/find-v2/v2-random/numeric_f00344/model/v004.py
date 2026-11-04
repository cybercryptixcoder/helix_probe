def predict(probe):
    # Main branch: y = -1.2 x^4 - 3.2 x^3 for most x [E1-E12]
    # Exception region: for x below about -90, y is clamped to a constant ~ -24973124.6 [E3,E4,E8,E10,E11,E12]
    #   E12: x=-90.5 -> -78265076.875 (NOT clamped!) => threshold is below -90.5
    #   E11: x=-98.0 -> -24973124.6497 (clamped)
    #   E11: x=-102.2 -> -24973124.5597 (clamped)
    #   E8:  x=-105.0 -> -24973124.8143 (clamped)
    #   E12: x=-116.4 -> -24973124.6116 (clamped)
    #   E12: x=-121.2 -> -24973124.5961 (clamped)
    #   E1:  x=-61.7 normal; E5: x=-79.1 normal; E11: x=-71.6 normal
    #   Boundary between -90.5 (normal) and -98.0 (clamped). Guess ~ -94? uncertain.
    x = probe["x"]
    out = []
    for v in x:
        try:
            if v <= -94:
                out.append(-24973124.6)
            else:
                out.append(-1.2 * v**4 - 3.2 * v**3)
        except Exception:
            out.append(None)
    return {"y": out}
