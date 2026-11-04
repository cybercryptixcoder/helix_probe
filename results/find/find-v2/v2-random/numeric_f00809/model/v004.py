import math

def predict(probe):
    # Beliefs (v4):
    # 1. Many outputs are tiny (~0.005-0.01) [E5,E8,E10,E12,E13]: product structure,
    #    one factor often near zero.
    # 2. Occasional large |y| up to ~0.32 [E3,E5,E7,E10]: amplitude ~0.3 when both factors large.
    # 3. Signs flip over small x gaps (104.5 vs 104.9) [E2,E5]: a high-frequency factor exists.
    # 4. Sign flips also over ~0.7 gaps [E5 94.1/94.8]: high-freq period ~1-1.5 units.
    # 5. Best guess: y = 0.3 * sin(a*x+p) * sin(b*x+q), a~4.5, b~0.3. (?)
    #    Product gives near-zero values often and large values rarely.
    # 6. No special interval detected; treat domain as uniform. (?)
    x = probe.get("x", [])
    ys = []
    for xi in x:
        try:
            xi = float(xi)
        except Exception:
            ys.append(None)
            continue
        hi = math.sin(4.5 * xi + 0.5)      # fast carrier -> rapid sign flips
        lo = math.sin(0.30 * xi + 1.0)     # slow envelope -> varying magnitude
        val = 0.30 * hi * lo
        if val > 0.35:
            val = 0.35
        if val < -0.35:
            val = -0.35
        ys.append(round(val, 4))
    return {"y": ys}
