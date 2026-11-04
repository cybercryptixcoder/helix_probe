import math

def predict(probe):
    # Mechanism beliefs:
    # - Outside a central interval, f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 (exact cubic) [E1, E17]
    # - Inside interval the function is flat ~7773 with small noise [E2-E16].
    # - Lower boundary is exactly 97.5, EXCLUDED: 97.5 gives cubic, 97.5001 gives flat [E9, E10, E20].
    # - Upper boundary: flat through 117.5638, cubic at 117.564 [E21]. So boundary in (117.5638, 117.564].
    #   Best guess 117.5639 (open) [?].
    # - Flat value is ~7773 (noise mean ~7772.95); return 7773.0.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            if 97.5 < x < 117.5639:
                ys.append(7773.0)
            else:
                ys.append(1.3 * x**3 + 2.3 * x**2 - 1.6 * x - 48.6)
        except Exception:
            ys.append(None)
    return {"y": ys}
