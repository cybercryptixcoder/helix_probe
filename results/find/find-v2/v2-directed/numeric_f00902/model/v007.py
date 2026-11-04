import math

def predict(probe):
    # Mechanism beliefs:
    # - Outside a central interval, f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 (exact cubic fit)
    #   [E1: x=0 -> -48.6, x=50 -> 168121.4, x=-50 -> -156718.6, x=128 -> 2763727.4, x=-128 -> -2688458.2]
    # - Inside an interval the function is flat ~7773 with small noise [E2-E11].
    # - Lower boundary is exactly 97.5, EXCLUDED: 97.5 gives cubic, 97.5001 gives flat [E9, E10].
    # - Upper boundary is between 117 (flat) and 118 (cubic) [E11]; best guess 117.5 (open) [?].
    # - Flat value is ~7773 (noise mean ~7772.9); return 7773.0.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            if 97.5 < x < 117.5:
                ys.append(7773.0)
            else:
                ys.append(1.3 * x**3 + 2.3 * x**2 - 1.6 * x - 48.6)
        except Exception:
            ys.append(None)
    return {"y": ys}
