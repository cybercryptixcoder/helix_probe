import math

def predict(probe):
    # Beliefs:
    # - Output is noisy (~±0.3) around a smooth curve [all E].
    # - Positive side (x>0): mean ~+1.0, oscillation amplitude ~1.5 [E12,E14,E17].
    # - Negative side (x<-30): mean ~-1.2, oscillation amplitude ~1.5 [E8,E10].
    # - Transition is gradual around x in [-30,0] [E16].
    # - Oscillation is irregular; period ~30-50, not a clean sinusoid [E12,E14].
    # - Use sum of two incommensurate sines with a slowly varying phase.
    def offset(x):
        t = (x + 30.0) / 30.0
        if t <= 0: return -1.2
        if t >= 1: return 1.0
        s = t * t * (3 - 2 * t)
        return -1.2 + 2.2 * s
    def wobble(x):
        return (1.1 * math.sin(2*math.pi*x/37.0 + 0.3)
                + 0.6 * math.sin(2*math.pi*x/19.0 + 2.1))
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(offset(x) + wobble(x))
        except Exception:
            ys.append(None)
    return {"y": ys}
