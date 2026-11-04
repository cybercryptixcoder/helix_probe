import math

def predict(probe):
    # Beliefs:
    # - Central region |x| < ~3.0 gives values around 11-14, varying with x. [E2,E4,E6,E12,E18]
    # - Plateau boundary is between 2.9 and 3.1. [E4,E6]
    # - Outside region: values roughly in [-2.3, 3.2], centered near 0, no smooth
    #   structure (neighbors uncorrelated). [E1,E3,E5,E7,E8,E10,E14,E15]
    # - E16 shows re-probing identical x gives DIFFERENT values than before
    #   (e.g. x=-6.0: E4 gave 1.0064, E16 gave -1.8155). So outside region is
    #   run-to-run noise. [E16]
    # - E18 shows inside region is ALSO run-to-run noisy: x=-3.0 gave 11.0985 in
    #   E12 but 10.2725 in E18; x=0.0 gave 13.2751 then 11.1789. So plateau is
    #   noisy too, band ~10.3-14.1. [E18]
    # - Since both regions are noisy, the best we can do is predict the MEAN.
    #   Outside mean ~0.5 (values skew slightly positive: many 0.2-1.5, some
    #   negatives). Inside mean ~11.8. [E7,E8,E10,E14,E15,E17,E19]
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
            # plateau: noisy around ~11.8
            val = 11.8
        else:
            # outside: noisy around ~0.5
            val = 0.5
        ys.append(round(val, 4))
    return {"y": ys}
