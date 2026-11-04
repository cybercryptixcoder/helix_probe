import math

def predict(probe):
    # Beliefs about f(x):
    # - Baseline is a smooth, slowly varying function of x over the whole
    #   domain, roughly linear with slope ~+0.0005 on the right and a
    #   gentle rise on the left [E2, E6, E10, E12].
    # - There is a sharp negative dip near x=1 (min ~-0.095 at x=1) with a
    #   narrow width, and a positive hump peaking ~0.078 near x=-2 [E4, E8].
    # - The dip/hump region is localized to roughly x in [-16, 8]; outside
    #   it the baseline is smooth [E2, E6, E8, E10, E12].
    # - f(0) ~ -0.0008 consistently [E2, E4, E6, E8, E12].
    # - Baseline on the right: from E12, f(24..76) rises linearly from
    #   0.0003 to 0.0285, slope ~0.00054, intercept ~ -0.0127 at x=24.
    #   Extrapolating: f(0) baseline ~ -0.0137, f(128) ~ 0.0564.
    # - Baseline on the left: from E6, f(-128..-16) rises from 0.0479 to
    #   0.0149, slope ~ -0.000295, intercept ~ 0.0102 at x=0.
    # - The two baselines don't meet at 0; there's a transition. The hump
    #   and dip sit on top of a blend.

    # Baseline right: fit through (24,0.0003) and (76,0.0285)
    a_R = (0.0285 - 0.0003) / (76 - 24)   # 0.0005423
    b_R = 0.0003 - a_R * 24                # -0.01272

    # Baseline left: through (-128,0.0479) and (-16,0.0149)
    a_L = (0.0149 - 0.0479) / (-16 - (-128))   # -0.0002946
    b_L = 0.0149 - a_L * (-16)                  # 0.01019

    def base(x):
        # blend left/right baseline smoothly over [-16, 8]
        if x <= -16:
            return a_L * x + b_L
        if x >= 8:
            return a_R * x + b_R
        t = (x + 16) / 24.0
        t = t * t * (3 - 2 * t)
        return (a_L * x + b_L) * (1 - t) + (a_R * x + b_R) * t

    # Hump: positive, peaks ~0.078 near x=-2, extends from ~-16 to ~0.
    # At x=-2, base(-2) ~ a_L*-2+b_L = 0.0108; need +0.0676.
    # At x=-8, base ~ 0.0126; observed 0.031 -> +0.0184.
    # At x=-16, base ~ 0.0149; observed 0.0149 -> +0.
    # At x=0, base ~ -0.0127; observed -0.0008 -> +0.0119.
    # So hump is asymmetric: rises from -16, peaks near -2, falls to 0.
    # Model as Gaussian centered -2, sigma ~5, amplitude 0.068, but
    # truncated: at -16 exp(-(14)^2/50)=exp(-3.92)=0.02 -> 0.0014 ok.
    # At 0: exp(-4/50)=0.92 -> 0.063, too big. Need narrower on right.
    # Use asymmetric sigma: sigma_left=5, sigma_right=2.5.
    def hump(x):
        if x > -2:
            s = 2.5
        else:
            s = 5.0
        return 0.068 * math.exp(-((x + 2) ** 2) / (2 * s * s))

    # Dip: negative, min ~-0.095 at x=1, narrow. At x=0.5 obs -0.0484,
    # base(0.5)~-0.0124, hump(0.5)~0.068*exp(-6.25/12.5)=0.041 -> 0.0286,
    # need dip -0.077. At x=1: base~-0.0122, hump~0.068*exp(-9/12.5)=0.033
    # -> 0.0208, need -0.095 -> dip -0.116. At x=1.5: obs -0.0782,
    # base~-0.0119, hump~0.068*exp(-12.25/12.5)=0.0255 -> 0.0136,
    # need dip -0.092. At x=2: obs -0.0595, base~-0.0116,
    # hump~0.068*exp(-16/12.5)=0.0189 -> 0.0073, need dip -0.067.
    # At x=2.5: obs -0.0507, base~-0.0114, hump~0.068*exp(-20.25/12.5)=0.0134
    # -> 0.002, need dip -0.053. At x=3: obs -0.0466, base~-0.0111,
    # hump~0.068*exp(-25/12.5)=0.0092 -> -0.0019, need dip -0.045.
    # At x=4: obs -0.0438, base~-0.0106, hump~0.068*exp(-36/12.5)=0.0038
    # -> -0.0068, need dip -0.037. At x=8: obs -0.03, base~-0.0084,
    # hump~0.068*exp(-100/12.5)=0.0002 -> -0.0082, need dip -0.022.
    # So dip has a long right tail. Model as Gaussian centered 1,
    # sigma_left=0.7, sigma_right=2.5, amplitude -0.116.
    def dip(x):
        if x > 1:
            s = 2.5
        else:
            s = 0.7
        return -0.116 * math.exp(-((x - 1) ** 2) / (2 * s * s))

    def f(x):
        return base(x) + hump(x) + dip(x)

    out = []
    for xv in probe.get("x", []):
        try:
            x = float(xv)
        except (TypeError, ValueError):
            out.append(None)
            continue
        if not math.isfinite(x):
            out.append(None)
            continue
        try:
            out.append(round(f(x), 4))
        except Exception:
            out.append(None)
    return {"y": out}
