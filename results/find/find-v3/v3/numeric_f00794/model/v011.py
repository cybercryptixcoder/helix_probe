import random

def predict(probe):
    # A: nonzero |x|>=0.8 -> per-call random in ~[-1,1], independent of x [E20,E22,E23,E24,E25]
    # B: x==0 -> ~474 spike [E2,E6,E8,E24]
    # C: 0<|x|<0.8 -> positive spike ~6-14 (noisy), sign-independent [E12,E24]
    #    E24: |x| in {0.01..0.7} all give ~13-14; |x|>=0.8 give ordinary noise.
    #    So spike region is |x|<0.8, magnitude ~13-14 (not 1/|x|).
    ys = []
    for x in probe.get("x", []):
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None); continue
        if xv == 0.0:
            ys.append(474.0)
        elif abs(xv) < 0.8:
            ys.append(random.uniform(6.0, 14.5))
        else:
            ys.append(random.uniform(-1.0, 1.0))
    return {"y": ys}
