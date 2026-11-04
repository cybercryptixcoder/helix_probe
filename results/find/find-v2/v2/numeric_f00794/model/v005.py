import math

def predict(probe):
    # Beliefs:
    # 1. Ordinary region (|x| >= ~1.2): output is fresh noise per call, ~uniform in [-1,1],
    #    independent of x, sign, magnitude, and position [E8,E12,E14,E16,E18,E20: repeated x give unrelated y].
    # 2. Special region 0 < |x| < ~1: output is a plateau. But the plateau VALUE differs by sign:
    #    positive x (0<x<~1) -> ~12.5-14.4 [E12: 0.1..0.75 -> 13.6-14.4; E20: 0.5 -> 12.6-13.0];
    #    negative x (-1<x<0) -> ~6.4-7.4 [E6: -0.5 -> 7.39; E14: -0.7..-0.2 -> ~6.5-7.5; E20: -0.5 -> 6.4-7.0].
    # 3. At x=0 exactly, output ~475 [E6,E14].
    # 4. Boundary: plateau for 0<|x|<~0.75; ordinary for |x|>=~0.76 [E16: 0.76..1.15 all ordinary].
    #    E12 0.75 -> 14.15 (plateau), E16 0.76 -> ordinary. So boundary ~0.755.
    # 5. No deterministic structure recoverable in ordinary region.

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
        elif ax < 0.755:
            if xf > 0:
                ys.append(round(_plateau_pos(xf), 4))
            else:
                ys.append(round(_plateau_neg(xf), 4))
        else:
            ys.append(round(_pseudo(xf), 4))
    return {"y": ys}


def _plateau_pos(x):
    # ~13.5 mean, small spread; fresh noise per call
    v = math.sin(x * 91.7 + 13.1) * 43758.5453
    frac = v - math.floor(v)
    return 12.6 + frac * 1.8


def _plateau_neg(x):
    # ~7.0 mean, small spread; fresh noise per call
    v = math.sin(x * 57.3 + 41.7) * 43758.5453
    frac = v - math.floor(v)
    return 6.4 + frac * 1.0


def _pseudo(x):
    v = math.sin(x * 12.9898 + 78.233) * 43758.5453
    frac = v - math.floor(v)
    return frac * 2.0 - 1.0
