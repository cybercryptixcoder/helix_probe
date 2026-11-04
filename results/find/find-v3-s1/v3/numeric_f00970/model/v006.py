import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (revised):
    # - There is a central "active" band where f is large (~12), and outside
    #   it f is small (~0). [E2, E5, E6, E11, E13, E15]
    # - The active band is NOT symmetric and NOT exactly |x|<3.5. Evidence:
    #     E16: x=-3.9,-3.7,-3.5,-3.3,-3.1 are SMALL; x=-2.7..2.3 are LARGE.
    #     E6:  x=-3.6,-3.4,-3.2 small; x=-3.0,-2.8 large; x=2.8,3.0 large;
    #          x=3.2,3.4,3.5,3.6,3.8,4.0 small; x=2.0,-2.0 large.
    #     E14: x in [-3.0,3.0] all large.
    #   => active band is roughly x in (-3.05, 3.05) on the left edge ~ -3.05
    #      and right edge ~ +3.05. Left boundary between -3.1 and -3.0;
    #      right boundary between 3.0 and 3.2. [E6, E16]
    # - Inside the band values scatter around ~12.2 with spread ~0.7; no
    #   smooth shape is evident (E14, E16 look noise-like). Best point
    #   prediction is the mean ~12.2. [E14, E16]
    # - Outside the band values scatter around 0 with spread ~0.8; no smooth
    #   or periodic structure found (E4, E8, E10, E12). Best point prediction
    #   is 0. [E4, E8, E10, E12]
    # - The transition is sharp (no gradual ramp observed). [E6, E16]

    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue

        # Active band boundaries (asymmetric guess, left ~ -3.05, right ~ 3.1)
        if -3.05 <= v <= 3.1:
            ys.append(12.2)
        else:
            ys.append(0.0)

    return {"y": ys}
