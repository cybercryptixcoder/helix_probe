def predict(probe):
    # Observations [E1]:
    # - For x <= -48: y rises steeply and linearly as x decreases.
    #   Points: (-128,326549.8),(-112,256101.5),(-96,185653.3),(-80,115205.0),(-64,44756.7)
    #   Slope ≈ (44756.7-326549.8)/(-64+128) = -281793.1/64 ≈ -4403.0 per unit x.
    #   Intercept via (-64,44756.7): 44756.7 + 4403.0*64 ≈ 44756.7+281792 ≈ 326549 (matches -128).
    # - For -48 <= x <= 16: y = constant -84.3663 (flat plateau).
    # - For x >= 64: y rises steeply again; (64,15971.3),(128,258084.0).
    #   Slope ≈ (258084.0-15971.3)/(128-64) = 242112.7/64 ≈ 3783.0 per unit x.
    #   Intercept via (64,15971.3): 15971.3 - 3783.0*64 ≈ 15971.3-242112 ≈ -226141.
    # - Between 16 and 64: unknown transition; assume smooth/linear interpolation between
    #   the plateau value at 16 and the right-branch value at 64. (?)
    # - Between -64 and -48: unknown transition; assume linear between left-branch value
    #   at -64 and plateau at -48. (?)
    try:
        xs = probe["x"]
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x <= -64:
                y = -4403.0 * x - 237034.0  # fits (-64,44756.7) and (-128,326549.8)
            elif x <= -48:
                # transition from left branch at -64 to plateau at -48 (?)
                y_left = -4403.0 * (-64) - 237034.0  # 44756.7
                t = (x + 64) / 16.0
                y = y_left + t * (-84.3663 - y_left)
            elif x <= 16:
                y = -84.3663
            elif x <= 64:
                # transition from plateau at 16 to right branch at 64 (?)
                y_right = 3783.0 * 64 - 226141.0  # 15971.3
                t = (x - 16) / 48.0
                y = -84.3663 + t * (y_right + 84.3663)
            else:
                y = 3783.0 * x - 226141.0
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
