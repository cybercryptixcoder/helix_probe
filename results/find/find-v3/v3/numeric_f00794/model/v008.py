import math, random

def predict(probe):
    # A: nonzero x -> per-call random in ~[-1,1], independent of x [E20: same x=37 ten times gives 10 different y; E18 vs E10 same x different y]
    # B: x==0 -> spike near 475 [E2,E6,E8]
    # C: near-zero nonzero x -> larger magnitude spikes [E12: 0.5->12.9, -0.5->6.4]
    # D: ordinary nonzero -> mean 0 noise [E1-E21]
    ys = []
    for x in probe.get("x", []):
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None); continue
        if xv == 0.0:
            ys.append(475.0)
        elif abs(xv) < 1.0:
            ys.append(6.5 / abs(xv))
        else:
            ys.append(random.uniform(-1.0, 1.0))
    return {"y": ys}
