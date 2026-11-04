import math

def predict(probe):
    # Beliefs:
    # 1. Ordinary region output is fresh noise each call, not a function of x [E12,E14: repeated x give different y].
    #    So ordinary predictions are essentially unpredictable; output ~ uniform in [-1,1].
    # 2. Special region: for 0 < |x| < ~1, output is a plateau ~6.5-7.5 [E14: x=-0.7..-0.2 -> ~6.5-7.5].
    #    At |x| >= ~1.2 output is ordinary [E14: x=1.2,1.3,1.4 ordinary].
    #    At x=0 exactly, output ~475 [E6,E14].
    # 3. Transition: |x| in [0.8,1.0] mixed [E14: -0.9,-0.8 ordinary; -0.7..-0.2 plateau].
    #    So plateau for 0<|x|<~0.75, ordinary for |x|>=~0.85. Boundary uncertain.
    # 4. No deterministic structure recoverable in ordinary region.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue
        ax = abs(xf)
        if xf == 0.0:
            ys.append(round(475.0, 4))
        elif ax < 0.75:
            ys.append(round(7.0, 4))
        else:
            ys.append(round(_pseudo(xf), 4))
    return {"y": ys}


def _pseudo(x):
    v = math.sin(x * 12.9898 + 78.233) * 43758.5453
    frac = v - math.floor(v)
    return frac * 2.0 - 1.0
