import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Observations:
    #  - For x >= ~1, f decreases roughly linearly with x [E4, E2]:
    #       f(2)=-0.0595, f(4)=-0.0438, f(8)=-0.03, f(12)=-0.0208,
    #       f(20)=-0.0043, f(40)=0.0089, f(80)=0.0307, f(100)=0.0415,
    #       f(128)=0.0565.  Slope ~ +0.0005 per unit, intercept ~ -0.05.
    #  - For x <= -8, f decreases roughly linearly with x too [E6]:
    #       f(-128)=0.0479, f(-80)=0.0335, f(-40)=0.0219, f(-16)=0.0149,
    #       f(-8)=0.031.  Slope ~ -0.0002 per unit, intercept ~ +0.02.
    #  - There is a "hump" region around x in (-8, 2): f rises from
    #    ~0.015 at x=-16 to a peak ~0.078 around x=-2..-1, then drops
    #    steeply through 0 (f(0)=-0.0008) to ~-0.095 at x=1, then
    #    recovers toward the linear branch [E4, E8].
    #  - f(0) is consistently ~ -0.0008 [E2, E4, E6, E8].
    #
    # The shape looks like a smooth MLP approximation of a piecewise
    # function: linear outside, with a localized bump/dip near 0.
    #
    # We model it as:
    #   left branch  (x <= -8):  a_L * x + b_L
    #   right branch (x >=  2):  a_R * x + b_R
    #   middle region: smooth interpolation with a Gaussian-like bump
    #                  plus a sharp dip near x=1.
    #
    # Fit constants from the evidence.

    # Right branch: through (20,-0.0043) and (100,0.0415)
    a_R = (0.0415 - (-0.0043)) / (100 - 20)   # 0.0005725
    b_R = -0.0043 - a_R * 20                    # -0.01575

    # Left branch: through (-128,0.0479) and (-16,0.0149)
    a_L = (0.0149 - 0.0479) / (-16 - (-128))   # -0.0002946
    b_L = 0.0149 - a_L * (-16)                  # 0.01019

    # Middle: build a smooth function matching E4/E8.
    # Key anchors (x, y):
    #   (-16, 0.0149), (-8, 0.031), (-4, 0.0628), (-2, 0.0784),
    #   (-1, 0.0776), (0, -0.0008), (1, -0.0951), (2, -0.0595),
    #   (4, -0.0438), (8, -0.03)
    #
    # The bump from -16 to 0 looks like a raised cosine / Gaussian
    # centered near -2.5 with amplitude ~0.06 on top of the left
    # linear continuation.  The dip near 1 looks like a narrow
    # Gaussian of amplitude ~-0.1 centered at 1.

    def left_lin(x):
        return a_L * x + b_L

    def right_lin(x):
        return a_R * x + b_R

    # Bump: Gaussian centered at -2.5, sigma ~ 4, amplitude tuned so
    # that peak reaches ~0.078 at x=-2.
    # left_lin(-2) = -0.0002946*-2 + 0.01019 = 0.01078
    # need bump(-2) ~ 0.0784 - 0.01078 = 0.0676
    bump_amp = 0.0676
    bump_center = -2.5
    bump_sigma = 3.5

    # Dip: Gaussian centered at 1.0, sigma ~ 0.8, amplitude ~ -0.10
    # At x=1, right_lin(1) = 0.0005725 - 0.01575 = -0.01518
    # bump(1) = 0.0676*exp(-(3.5)^2/(2*3.5^2)) = 0.0676*exp(-0.5)=0.041
    # so base at 1 ~ -0.01518 + 0.041 = 0.0258; need -0.0951 -> dip ~ -0.121
    dip_amp = -0.121
    dip_center = 1.0
    dip_sigma = 0.9

    def middle(x):
        # blend between left and right linear based on x
        # use smooth transition: for x < -8 use left, x > 2 use right
        # but add bump and dip
        base = left_lin(x) if x < -8 else right_lin(x)
        # smooth blend in transition zone
        if -8 <= x <= 2:
            t = (x + 8) / 10.0
            # smoothstep
            t = t * t * (3 - 2 * t)
            base = left_lin(x) * (1 - t) + right_lin(x) * t
        bump = bump_amp * math.exp(-((x - bump_center) ** 2) / (2 * bump_sigma ** 2))
        dip = dip_amp * math.exp(-((x - dip_center) ** 2) / (2 * dip_sigma ** 2))
        return base + bump + dip

    def f(x):
        if x <= -8:
            # left branch, but ensure continuity with middle at -8
            # left_lin(-8) = 0.01255; middle(-8) should be ~0.031
            # The bump extends left of -8, so use middle formula for
            # x in [-16, -8] too, blending.
            if x >= -16:
                return middle(x)
            return left_lin(x)
        elif x >= 2:
            return right_lin(x)
        else:
            return middle(x)

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
