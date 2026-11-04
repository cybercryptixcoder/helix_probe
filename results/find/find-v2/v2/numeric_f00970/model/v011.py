import math

def predict(probe):
    # Beliefs:
    # - Central region |x| < ~3.0 gives values around 11-13 (mean ~11.8). [E2,E4,E6,E12,E18]
    # - Plateau boundary between 2.9 and 3.1. [E4,E6]
    # - Outside region: values roughly in [-2.3, 3.2], mean ~0.3, spread ~1. [E1,E3,E5,E7,E8,E10,E14,E15]
    # - Both regions are run-to-run NOISY (not deterministic in x): E16 vs E22 same x, different y;
    #   E12 vs E18 same x, different y. [E16,E18,E22]
    # - E20: dense grid shows no fine structure; white noise. [E20]
    # - So best prediction is the MEAN of each region; noise is irreducible.
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
        if abs(xv) < 3.0:
            val = 11.8
        else:
            val = 0.3
        ys.append(round(val, 4))
    return {"y": ys}
