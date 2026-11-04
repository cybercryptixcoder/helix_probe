import math

def predict(probe):
    # Model: f(x) is a small MLP approximating a smooth function.
    # Evidence E1: outputs are small (~0.02-0.05), vary smoothly with x,
    # roughly periodic-looking but weak. Without more data, best guess is a
    # small-amplitude smooth function. We can't fit an MLP from one probe,
    # so approximate with a low-amplitude sinusoid-like smooth function.
    # The sign flips (negative near x=2.9, x=-6.0) suggest oscillation.
    # Best guess: f(x) ~ A*sin(w*x + phi) with small A.
    # From E1: at x=2.9 -> -0.0469, x=-6.0 -> 0.0471, x=21.3 -> -0.0017.
    # A ~ 0.05, and sign changes suggest period ~ 20-30.
    # Use a simple sinusoid guess.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            y = 0.04 * math.sin(0.25 * x + 0.5)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
