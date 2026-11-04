import math

def predict(probe):
    # Beliefs:
    # - Inner plateau: |x| < ~3.0 gives ~11-14, varying with x, not flat. [E2,E4,E6,E12]
    # - Boundary: plateau ends between 2.9 and 3.1; outside is small. [E4,E6]
    # - Outside region: values in ~[-2.3, 3.2], centered near 0, no smooth
    #   structure (neighbors uncorrelated). Treat as bounded pseudo-random. [E1,E3,E5,E7,E8,E10,E14,E15]
    # - No reproducible deterministic form found for outside; use hash-like noise. [E14]
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
        if ax < 3.0:
            val = 12.0 + 0.9 * math.sin(2.7 * xv) + 0.35 * math.cos(5.1 * xv)
        else:
            s = math.sin(xv * 12.9898 + 0.37) * 43758.5453
            frac = s - math.floor(s)
            val = (frac * 2.0 - 1.0) * 1.8
        ys.append(round(val, 4))
    return {"y": ys}
