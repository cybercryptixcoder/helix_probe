import math

def predict(probe):
    # Ordinary nonzero x: output is deterministic but NOT degree-sine [E14: sin(10°)=0.1736 vs obs 0.4399].
    # Repeated x across experiments give different y [E1 vs E10: x=66.0 -> 0.1235 vs 0.4241], so it's
    # stochastic/unpredictable per-call; best guess is mean 0 for nonzero x [E1-E14 spread ~[-1,1]].
    # x==0 is a spike regime near 475 [E2,E6,E8].
    ys = []
    for x in probe.get("x", []):
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None); continue
        ys.append(475.0 if xv == 0.0 else 0.0)
    return {"y": ys}
