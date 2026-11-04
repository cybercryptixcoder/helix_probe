import math

def predict(probe):
    # A: nonzero x -> output is per-call random in ~[-1,1], not a function of x [E1 vs E10 vs E18: same x, different y]
    # B: x==0 -> spike near 475 [E2,E6,E8]
    # C: near-zero nonzero x -> larger magnitude spikes (e.g. 0.5->12.9, -0.5->6.4) [E12]
    # D: otherwise best guess is 0 (mean of the noise) [E1-E18]
    ys = []
    for x in probe.get("x", []):
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None); continue
        if xv == 0.0:
            ys.append(475.0)
        elif abs(xv) < 1.0:
            # ? small-x regime: observed 12.9 at 0.5, 6.4 at -0.5; scale ~ 1/|x| * c? guess c~6.5
            ys.append(6.5 / abs(xv))
        else:
            ys.append(0.0)
    return {"y": ys}
