import math

def predict(probe):
    # Beliefs:
    # - Outputs are noisy (jitter ~±0.3-0.5) around a smooth underlying curve [E1-E8].
    # - For x > ~0: oscillatory, roughly sinusoid with period ~50-60, amplitude ~1.5, offset ~+0.8 [E2,E4,E6].
    # - For x < ~-30: values are mostly negative, mean around -1.5, still wiggly but shifted down [E4,E5,E7,E8].
    # - There's a transition region around x in [-30, 0] where offset moves from negative to positive [E2,E4].
    # - Model: y = offset(x) + A*sin(w*x + p), with offset a smooth step from -1.5 to +0.8.
    A = 1.5
    w = 2 * math.pi / 55.0
    p = 0.3
    def offset(x):
        # smooth step from -1.5 (x<=-30) to +0.8 (x>=0)
        t = (x + 30.0) / 30.0
        if t <= 0: return -1.5
        if t >= 1: return 0.8
        # smoothstep
        s = t * t * (3 - 2 * t)
        return -1.5 + (0.8 - (-1.5)) * s
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(offset(x) + A * math.sin(w * x + p))
        except Exception:
            ys.append(None)
    return {"y": ys}
