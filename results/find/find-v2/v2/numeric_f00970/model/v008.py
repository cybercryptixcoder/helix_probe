import math

def predict(probe):
    # Beliefs:
    # - Central region |x| < ~3.0 gives values around 11-14, varying with x. [E2,E4,E6,E12]
    # - Plateau boundary is between 2.9 and 3.1. [E4,E6]
    # - Outside region: values roughly in [-2.3, 3.2], centered near 0, no smooth
    #   structure (neighbors uncorrelated). [E1,E3,E5,E7,E8,E10,E14,E15]
    # - E16 shows re-probing identical x gives DIFFERENT values than before
    #   (e.g. x=-6.0: E4 gave 1.0064, E16 gave -1.8155; x=40.0: E14 gave -0.3097,
    #   E16 gave -1.1261). So outside region is NOT deterministic in x: it is
    #   run-to-run noise. [E16]
    # - Inside region may also be noisy but stays in ~11-14 band. [E12]
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
            # plateau: ~11-14, slight x-dependence, plus noise
            val = 12.0 + 0.9 * math.sin(2.7 * xv) + 0.35 * math.cos(5.1 * xv)
        else:
            # outside: run-to-run noise, roughly uniform in [-2.3, 3.2]
            s = math.sin(xv * 12.9898 + 0.37) * 43758.5453
            frac = s - math.floor(s)
            val = (frac * 5.5 - 2.3)
        ys.append(round(val, 4))
    return {"y": ys}
