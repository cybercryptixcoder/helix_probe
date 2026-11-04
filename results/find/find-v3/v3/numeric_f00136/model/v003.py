import math

def predict(probe):
    # Beliefs:
    # - For |x| >= ~13, f is a smooth, slowly varying "background" function of x,
    #   roughly periodic/oscillatory with small amplitude ~0.01-0.05 [E1,E3,E5,E7,E9].
    # - Inside |x| < ~13 there is a distinct "core" region with much larger
    #   amplitude and a piecewise-linear structure [E2,E4,E6,E8].
    # - Core: on x in [-6, -1], f rises linearly ~0.0079 per unit, peaking near
    #   x=-1.5..-2 at ~0.078 [E2,E6,E8].
    # - Core: on x in [0, 6], f falls linearly from ~0 at 0 to ~-0.037 at 6,
    #   slope ~ -0.0062..-0.0065 per unit [E2,E6,E8].
    # - Core: on x in [-12,-6], f rises from ~0.019 at -12 to ~0.043 at -6.5,
    #   slope ~0.0039 per unit [E6].
    # - Core: on x in [6,12], f rises from ~-0.037 at 6 to ~-0.021 at 12,
    #   slope ~0.0027 per unit [E6].
    # - There are sharp transitions near x=-0.5 (drops to ~0.049) and x=0.5
    #   (drops to ~-0.048) and x=1.5 (~-0.078) — a dip/bump structure
    #   [E4,E8]. Model as triangular spikes on top of the linear trends.
    # - Outside core, background looks like small oscillations; approximate
    #   with a low-amplitude sinusoid plus slow trend. [E1,E3,E5,E7,E9]
    # - Noisy; outputs are approximate.

    x = probe["x"]
    ys = []
    for v in x:
        ys.append(_f(v))
    return {"y": ys}


def _f(x):
    try:
        x = float(x)
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None

    ax = abs(x)

    # Core region: |x| < 13
    if ax < 13.0:
        return _core(x)
    else:
        return _background(x)


def _core(x):
    # Piecewise-linear skeleton for the core region, with spike features.
    # Left branch x <= -1.5: rising line from x=-12 (0.019) to x=-1.5 (0.078)
    # then slight fall to x=-1 (0.0776).
    if x <= -1.5:
        # slope ~ (0.078 - 0.019)/(-1.5 - (-12)) = 0.059/10.5 = 0.00562
        # but E6 shows -12->0.0187, -6.5->0.0431: slope 0.0244/5.5=0.00444
        # E8: -4.5->0.0589, -2->0.0784: slope 0.0195/2.5=0.0078
        # Use two-segment: [-12,-6] slope 0.0044; [-6,-1.5] slope 0.0078
        if x <= -6.0:
            return 0.0187 + (x + 12.0) * 0.00444
        else:
            return 0.0431 + (x + 6.5) * 0.0078
    elif x <= -0.5:
        # from -1.5 (0.078) to -0.5 (0.049): slope -0.029
        return 0.078 + (x + 1.5) * (-0.029)
    elif x <= 0.0:
        # from -0.5 (0.049) to 0 (-0.0008): slope -0.0996
        return 0.049 + (x + 0.5) * (-0.0996)
    elif x <= 0.5:
        # from 0 (-0.0008) to 0.5 (-0.0484): slope -0.0952
        return -0.0008 + x * (-0.0952)
    elif x <= 1.5:
        # from 0.5 (-0.0484) to 1.5 (-0.0782): slope -0.0298
        return -0.0484 + (x - 0.5) * (-0.0298)
    elif x <= 6.0:
        # from 1.5 (-0.0782) rising toward 6 (-0.0371): slope 0.00913
        return -0.0782 + (x - 1.5) * 0.00913
    elif x <= 12.0:
        # from 6 (-0.0371) to 12 (-0.0208): slope 0.00272
        return -0.0371 + (x - 6.0) * 0.00272
    else:
        return -0.0208


def _background(x):
    # Slow, small-amplitude oscillation. Fit roughly:
    # E1: 88.2->0.0352, 66->0.0231, -20.3->0.0163, 72.7->0.0267
    # E3: 104.5->0.0439, 123.6->0.0541, 79.4->0.0304
    # E9: -127.7->0.0478, 119.7->0.0521
    # Looks like increasing trend with |x| plus small wiggles.
    # Use: base = 0.025 + 0.00015*|x| plus sinusoid amplitude 0.012
    # period ~ 60 in x.
    base = 0.025 + 0.00015 * abs(x)
    osc = 0.012 * math.sin(x * 0.10) + 0.006 * math.sin(x * 0.23 + 1.0)
    return base + osc
