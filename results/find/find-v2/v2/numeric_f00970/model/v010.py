import math

def predict(probe):
    # Beliefs:
    # - Central region |x| < ~3.0 gives values around 11-14. [E2,E4,E6,E12,E18]
    # - Plateau boundary is between 2.9 and 3.1 (E4: x=3.0 -> 12.24; E6: 2.9 in, 3.1 out). [E4,E6]
    # - Outside region: values roughly in [-2.3, 3.2], centered near 0. [E1,E3,E5,E7,E8,E10,E14,E15]
    # - E16: identical x re-probed gives DIFFERENT values (x=-6.0: 1.0064 then -1.8155). [E16]
    # - E18: inside region also run-to-run noisy (x=0.0: 13.2751 then 11.1789). [E18]
    # - E20: dense grid 10.0-14.75 shows no fine structure; values look like white noise. [E20]
    # - Both regions are run-to-run noise; best prediction is the MEAN.
    # - Outside mean ~0.3 (slight positive skew). Inside mean ~11.8. [E7,E8,E10,E14,E15,E17,E19,E21]
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
            val = 11.8
        else:
            val = 0.3
        ys.append(round(val, 4))
    return {"y": ys}
