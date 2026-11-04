import math

def predict(probe):
    # Beliefs:
    # - Central band roughly (-3.5, 3.5): y ~ 11-13, noisy [E1, E2]
    # - Outside band: y is small, noisy, roughly in [-2, 2], NOT smooth/monotone [E4]
    #   E4 shows adjacent x give wildly different y (e.g. -7->1.93, -5->0.69, -4.5->-0.81)
    #   So outside band behaves like noise around ~0 with std ~1.
    # - E1/E3 confirm: outside values scattered in [-2.2, 2.0], no clear trend with x.
    # - Best model: piecewise constant. Inside band -> ~11.5. Outside -> ~0 (mean of noise).
    #   Since noise dominates, predicting the mean minimizes expected error.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if -3.5 < x < 3.5:
                ys.append(11.5)
            else:
                ys.append(0.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
