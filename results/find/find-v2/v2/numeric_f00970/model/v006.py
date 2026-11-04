import math

def predict(probe):
    # Beliefs:
    # - There is an inner plateau region roughly |x| < 3 where f(x) ~ 11-14,
    #   with substantial variation (not flat). [E2,E4,E6,E12]
    # - At |x| >= ~3.1, f(x) is small (~[-2,2]) with no reproducible structure
    #   from x; treat as bounded pseudo-random. [E1,E3,E5,E7,E8,E10,E13]
    # - Boundary is between 3.0 and 3.2; use |x| < 3.1 as inner. [E4,E6]
    # - Inner values vary ~11-14 with no clean trend; model as ~12 + ripple. [E12]
    # - Outer values look like bounded noise; no trend found. [E10]
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            xv = float(v)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(xv) or math.isinf(xv):
            ys.append(None)
            continue

        ax = abs(xv)
        if ax < 3.1:
            val = 12.0 + 0.9 * math.sin(2.7 * xv) + 0.35 * math.cos(5.1 * xv)
        else:
            s = math.sin(xv * 12.9898) * 43758.5453
            frac = s - math.floor(s)
            val = (frac * 2.0 - 1.0) * 1.8
        ys.append(round(val, 4))
    return {"y": ys}
