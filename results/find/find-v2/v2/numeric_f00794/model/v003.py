import math

def predict(probe):
    # Beliefs:
    # 1. For most x, output is roughly a random-looking value in [-1, 1] [E1,E3,E5,E7].
    #    Repeated x give different y (E4: 21.3 -> -0.9926 and -0.2205; 0.0 -> 474.0491, 475.1603,
    #    475.3578, 475.3104), so the box is noisy/stochastic, not a deterministic function.
    # 2. There is a special region near x = 0 where the output is huge (~475) [E2,E4,E6].
    #    Observed huge values at x = 0.0 (475.36, 474.05, 475.16, 475.31).
    #    At x = -0.5 output is 7.39, at x = 0.5 output is 12.78 (E6): still elevated but not 475.
    #    At x = -1, 1, -2, 2 outputs are ordinary (~[-1,1]) [E6]. So the special interval is
    #    roughly |x| < 1, with the spike concentrated at x = 0. ? (boundary uncertain)
    # 3. Outside that region, no visible structure: outputs are pseudo-random in [-1,1] [all E].
    #    So we model the ordinary part as a deterministic pseudo-random function of x
    #    (consistent with noise; can't recover the true random draw).
    # 4. Undefined: none observed.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue

        ax = abs(xf)
        if ax < 1.0:
            # Special region near zero: large spike, largest at x=0.
            # Model: spike ~ 475 at x=0, decaying to ~10 near |x|=0.5, ordinary near |x|=1.
            # Use a peaked function. 475 * exp(-(x/0.15)^2) + 10*exp(-(x/0.5)^2) + ordinary.
            spike = 475.0 * math.exp(-(xf / 0.15) ** 2)
            shoulder = 10.0 * math.exp(-(xf / 0.5) ** 2)
            base = _pseudo(xf)
            ys.append(round(spike + shoulder + base, 4))
        else:
            ys.append(round(_pseudo(xf), 4))
    return {"y": ys}


def _pseudo(x):
    # Deterministic pseudo-random value in [-1, 1], mimicking the noisy ordinary output.
    # Uses a hash-like combination of sin; stable for a given x.
    v = math.sin(x * 12.9898 + 78.233) * 43758.5453
    frac = v - math.floor(v)
    return frac * 2.0 - 1.0
