import math, struct

def predict(probe):
    # Beliefs:
    # - For x < ~-75: y is tiny positive, linear: y ≈ 0.0046 + (x+128)*5.83e-5 [E2,E7,E9,E11]
    #   e.g. -128->0.0046, -100->0.0059, -80->0.0074
    # - Elsewhere: unpredictable noise, roughly uniform in [-0.26, 0.25], mean ~0 [E1-E13]
    # - No smooth dependence, no grid structure, no periodicity in noise region [E4,E8,E10,E12]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            v = float(x)
            if not math.isfinite(v):
                ys.append(None); continue
            if v < -75.0:
                y = 0.0046 + (v + 128.0) * 5.83e-5
                ys.append(round(y, 4)); continue
            b = struct.pack('<d', v)
            h = 2166136261
            for byte in b:
                h ^= byte
                h = (h * 16777619) & 0xFFFFFFFF
            frac = (h & 0xFFFFFF) / float(0xFFFFFF)
            y = (frac - 0.5) * 0.51
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}
