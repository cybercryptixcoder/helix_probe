import math

def predict(probe):
    # Model: f(x) is approximately constant ~81 across the whole range,
    # except near the upper edge where it rises sharply.
    # E1: values ~80.88-81.10 for x in [-128, 96]; at x=128 it jumps to ~88.99.
    # The jump appears to be a boundary effect near x=128 (upper domain edge).
    # Hypothesis: there is a special region near x=128 where f rises.
    # We don't know the boundary precisely; E1 shows x=96 -> ~80.98, x=128 -> ~88.99.
    # Guess: a smooth rise starting somewhere between 96 and 128, reaching ~89 at 128.
    # Base level ~81.0 with small noise.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        base = 81.0
        # Edge region near 128: rise toward ~89 at x=128.
        # Assume rise begins around x=112 (midpoint guess) and is linear to 128.
        if x > 112:
            t = (x - 112.0) / 16.0
            if t > 1:
                t = 1.0
            base = 81.0 + 8.0 * t
        out.append(base)
    return {"y": out}
