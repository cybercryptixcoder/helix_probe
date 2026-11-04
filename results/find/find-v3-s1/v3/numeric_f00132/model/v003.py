import math

def predict(probe):
    # Beliefs about f(x):
    # - f is essentially linear with slope ~4.71 for x>=0 and ~4.687 for x<0 [E1,E4,E19,E21]
    # - offset ~4.2 far from zero; near-zero region has a smooth wiggle [E2,E16,E18,E20]
    # - E22 shows the negative near-zero region is NOT the simple linear+small-bump
    #   model: observed values are systematically higher than v2 predicted for
    #   x in [-2,-0.4], and the shape is a smooth curve, not piecewise-linear.
    #   The residual (obs - 4.687*x - 4.2) on the negative side is a smooth bump
    #   peaking around x=-1.0 to -0.9, decaying by x=-2 and x=0.
    # - Positive side: residual (obs - 4.714*x - 4.2) is ~0 for x>=0.4 [E18,E20],
    #   with a small dip at x=0 [E20: f(0)=3.9155 vs 4.2].
    # So: f(x) = a*x + 4.2 + g(x), where g is a smooth near-zero correction.
    # Positive g: dip at 0, ~0 beyond 0.4.
    # Negative g: bump peaking near x=-0.9, ~0 by x=-2.5 and x=0.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            a = 4.714 if x >= 0 else 4.687
            y = a * x + 4.2
            if x >= 0:
                # dip at 0: f(0)=3.9155 -> g(0)=-0.2845; g(0.4)~0 [E20]
                y += -0.2845 * math.exp(-(x / 0.35) ** 2)
            else:
                # negative-side bump. Fit from E22 residuals:
                # r(x) = obs - (4.687*x + 4.2)
                # x=-2.0: -5.1471 - (-9.374+4.2)= -5.1471+5.174=0.027
                # x=-1.5: -2.9318 - (-7.0305+4.2)= -2.9318+2.8305=-0.101
                # x=-1.0: -0.2396 - (-4.687+4.2)= -0.2396+0.487=0.247
                # x=-0.9: 0.3127 - (-4.2183+4.2)= 0.3127+0.0183=0.331
                # x=-0.5: 1.9577 - (-2.3435+4.2)= 1.9577-1.8565=0.101
                # x=-0.1: 3.4123 - (-0.4687+4.2)= 3.4123-3.7313=-0.319
                # Hmm, residual is not a simple bump; it's a wiggle.
                # Let's use a Gaussian bump centered ~-0.9 plus a dip near 0.
                # bump: +0.33*exp(-((x+0.9)/0.6)^2)
                # dip near 0: -0.32*exp(-(x/0.3)^2) (matches x=-0.1 residual -0.32)
                y += 0.33 * math.exp(-((x + 0.9) / 0.6) ** 2)
                y += -0.32 * math.exp(-(x / 0.3) ** 2)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
