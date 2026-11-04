import math

def predict(probe):
    # Beliefs:
    # - Output = piecewise-constant mean + large noise (~±1.5), no clean period [E18,E20,E22,E24].
    # - Positive side (x>=0): mean ~+1.0 [E18,E24,E14].
    # - Negative side (x<0): mean ~-1.2 [E20,E8,E16].
    # - Sharp step at x=0; transition too narrow to resolve through noise [E16,E22].
    # - Noise is irreducible; predict the mean.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(1.0 if x >= 0 else -1.2)
        except Exception:
            ys.append(None)
    return {"y": ys}
