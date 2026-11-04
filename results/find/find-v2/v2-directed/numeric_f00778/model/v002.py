import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For |x| >= ~1.2, f(x) ≈ -3.9*x^3 (odd cubic) [E1, E2, E4]
    #   Check: f(100)=-3901796 vs -3.9e6; f(-100)=3897801; f(128)=-8181910 vs -3.901*128^3.
    # - For |x| < ~1.2, f(x) is small, roughly constant ~3, with noise [E3, E4, E5]
    #   E5: x in (-1.2,1.2) gives values 0.3..4.5, mean ~2.8, no cubic trend.
    #   E3: |x|<1.2 values 1.8..5.7, mean ~3.3.
    #   E4: |x|<1.2 values 1.8..5.8, mean ~3.6.
    # - Boundary: at |x|~1.2 the cubic takes over. E5: x=-1.2 -> 8.68, x=1.2 -> 0.34.
    #   Cubic at 1.2 = -3.9*1.728 = -6.74; at -1.2 = +6.74. Observed -1.2: 8.68 (close-ish),
    #   1.2: 0.34 (not close). So the transition is around |x|~1.2-1.4, gradual.
    # - Central region: model as a constant offset ~3 (mean of small-|x| observations),
    #   blended with cubic near the boundary. Noise can't be reproduced.
    #
    # Best guess: piecewise:
    #   |x| < 1.2: ~3 (constant, noisy)
    #   |x| >= 1.2: -3.9*x^3
    #   smooth blend in 1.0..1.4 to avoid a hard jump.
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            ax = abs(x)
            cubic = -3.9 * x * x * x
            if ax >= 1.4:
                ys.append(cubic)
            elif ax <= 1.0:
                ys.append(3.0)
            else:
                # blend from 3.0 at ax=1.0 to cubic at ax=1.4
                t = (ax - 1.0) / 0.4
                ys.append((1 - t) * 3.0 + t * cubic)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
