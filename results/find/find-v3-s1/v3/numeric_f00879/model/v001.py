import math

def predict(probe):
    # Observations are noisy; f looks like a smooth oscillatory function of x
    # with amplitude ~1-3 and no obvious linear trend [E1, E2].
    # Try a sinusoid: y ≈ A*sin(w*x + p) + c, with noise.
    # E2 suggests period ~ 60-70 (peaks near x=10, x=50; troughs near x=-40, x=-5).
    # Best guess: w ≈ 2π/60, amplitude ~1.5, offset ~0.3, phase fit roughly.
    # This is a hypothesis; noise makes exact fit impossible.
    A = 1.5
    w = 2 * math.pi / 60.0
    p = 0.5
    c = 0.3
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(A * math.sin(w * x + p) + c)
        except Exception:
            ys.append(None)
    return {"y": ys}
