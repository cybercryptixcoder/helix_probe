import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - For |x| >= ~1.1, f(x) ≈ -3.9*x^3 (odd cubic) [E1,E2,E4,E9,E11,E13]
    #   f(128)=-8181910, f(100)=-3901796.
    # - For |x| <= ~1.0, f(x) is ~3 plus substantial noise; no clean odd trend
    #   [E3,E5,E6,E7,E8,E10,E12,E14,E15,E16,E17,E18,E19,E20,E21,E22].
    #   Values scatter ~1.5..6.7, mean ~3. Matched +/- pairs show no systematic
    #   odd or even component [E14..E22].
    # - Transition: cubic ramps in between |x|~1.0 and ~1.1 [E11,E13,E18,E19].
    # - Noise: large in central region; use mean ~3.
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
            if ax >= 1.1:
                ys.append(cubic)
            elif ax <= 1.0:
                ys.append(3.0)
            else:
                t = (ax - 1.0) / 0.1
                ys.append((1 - t) * 3.0 + t * cubic)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
