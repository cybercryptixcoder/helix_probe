import math

def predict(probe):
    # Beliefs (revised):
    # - Outputs are noisy (~±0.3-0.5) around a smooth underlying curve [all E].
    # - The oscillation is NOT a clean sinusoid in x; period looks irregular [E12,E14].
    # - Positive side (x>0): values oscillate roughly in [-0.8, 2.8], mean ~+0.8 [E12,E14].
    # - Negative side (x<-30): values oscillate roughly in [-3.1, 0.7], mean ~-1.5 [E8,E10].
    # - Transition around x in [-30, 0] is gradual, not a sharp step [E16].
    # - The oscillation phase is not well captured by a fixed sinusoid; use a
    #   pseudo-random-but-deterministic wobble keyed on x to mimic irregularity.
    # - Best guess: y = offset(x) + wobble(x), where wobble has amplitude ~1.5
    #   and pseudo-period ~40-60 but irregular. [E12,E14 show irregular spacing]
    def offset(x):
        # smooth step from -1.5 (x<=-30) to +0.8 (x>=0)
        t = (x + 30.0) / 30.0
        if t <= 0: return -1.5
        if t >= 1: return 0.8
        s = t * t * (3 - 2 * t)
        return -1.5 + (0.8 - (-1.5)) * s
    def wobble(x):
        # irregular oscillation: sum of two incommensurate sines
        return (1.0 * math.sin(2*math.pi*x/47.0 + 0.7)
                + 0.7 * math.sin(2*math.pi*x/23.0 + 1.9))
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(offset(x) + wobble(x))
        except Exception:
            ys.append(None)
    return {"y": ys}
