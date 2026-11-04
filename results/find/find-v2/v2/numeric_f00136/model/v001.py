import math

def predict(probe):
    # Observations: outputs are small, roughly in [-0.05, 0.05], for inputs across [-128,128].
    # E1: y values vary with x but stay small; sign changes (e.g. x=2.9 -> -0.0469, x=-6.0 -> 0.0471).
    # Looks like a smooth bounded function, possibly sin-like or a small-amplitude MLP output.
    # Best guess: small-amplitude sinusoid of x. Fit roughly from E1.
    # E1 points: (88.2,0.0352),(66,0.0231),(-20.3,0.0163),(-61.7,0.0282),(2.9,-0.0469),
    #            (-24.3,0.0175),(72.7,0.0267),(-50.4,0.0249),(-6,0.0471),(21.3,-0.0017)
    # Try y = A*sin(w*x + p). Sign flip between 2.9 (neg) and -6 (pos) suggests period ~ small.
    # Rough: amplitude ~0.04, and zero crossings near x~ -3 and x~ 5? Hard to pin.
    # Use a simple sinusoid guess: A=0.04, w=0.05, p=0.
    out = []
    for x in probe["x"]:
        try:
            y = 0.04 * math.sin(0.05 * x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
