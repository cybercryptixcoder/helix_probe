def predict(probe):
    # Left region x < -5: f(x) = -0.7 * floor(x)  [E5,E8]
    # Flat region -5 <= x < 18.52: f ~ -402.3 (noisy constant)  [E4,E6,E10,E12,E14]
    #   E14: 18.50, 18.51 flat; 18.52+ right. So boundary in (18.51, 18.52].
    #   Pick 18.52 as start of right region (x >= 18.52).
    # Right region x >= 18.52: f(x) = -16.8 * floor(x)  [E2,E3,E4,E5,E6,E12,E13,E14]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5:
                y = -0.7 * math.floor(x)
            elif x < 18.52:
                y = -402.3
            else:
                y = -16.8 * math.floor(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
