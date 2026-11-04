import math

def predict(probe):
    # Model hypothesis:
    # - f(x) is mostly a small-amplitude oscillatory function of x, bounded roughly in [-1, 1] [E1, E2]
    # - At x = 0 there is a huge spike (~475.25), so a special region/point near 0 behaves differently [E2]
    # - Elsewhere, values look like a smooth-ish periodic function; fit a sinusoid plus a narrow spike at 0
    # - The spike appears localized: only x=0 shows 475.25; neighbors (5, -5) are normal [E2]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # Narrow spike at x = 0
            if abs(x) < 1e-9:
                ys.append(475.2497)
            else:
                # Oscillatory baseline: guess period ~ 100, amplitude ~0.7, offset ~0
                # Use a simple sinusoid as best guess from E2 shape
                val = 0.7 * math.sin(2 * math.pi * x / 100.0 + 0.5)
                ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}
