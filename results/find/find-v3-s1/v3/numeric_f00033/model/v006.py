import math

def predict(probe):
    # Beliefs (revised):
    # - Central bump: peak ~0.3868 at x=0, asymmetric, right side narrower [E2,E4]
    #   f(1)=0.255, f(-1)=0.1972; f(2)=0.12, f(-2)=0.0575; f(0.5)=0.3225, f(-0.5)=0.3052
    # - Far field is NOT flat: it varies with x in a structured way [E1,E3,E5,E6,E7]
    #   * near |x|~10-15: ~-0.0043 (most negative)
    #   * near |x|~20-40: rises toward ~-0.001 to -0.003
    #   * near |x|~70-90: ~-0.003 to -0.0035
    #   * near |x|~120: ~-0.0043
    #   * near |x|~6-8: ~0
    #   So the far field oscillates slowly with |x| — a damped wave, not a drift.
    # - Small secondary positive bump near x=+4 (0.0185 at 3.5, 0.0099 at 4) [E6]
    #   and milder on left near x=-4 (0.0053) [E6]
    # - Noise ~0.001 level [E1,E3,E5]
    # - Model: asymmetric Gaussian main bump + secondary bumps
    #   + far-field as a damped oscillation in |x|.

    xs = probe["x"]
    ys = []
    for x in xs:
        try:
            peak = 0.3868
            sigma = 1.55 if x >= 0 else 1.85
            main = peak * math.exp(-(x * x) / (2 * sigma * sigma))

            right_bump = 0.0185 * math.exp(-((x - 3.7) ** 2) / (2 * 0.9 * 0.9))
            left_bump = 0.0060 * math.exp(-((x + 4.0) ** 2) / (2 * 1.0 * 1.0))

            # Far-field: damped oscillation in |x|.
            # Anchor points (|x|, y): (7,0), (10,-0.0043), (15,-0.0043),
            # (20,-0.0012), (25,-0.0017), (30,-0.0021), (40,-0.003),
            # (70,-0.0033), (90,-0.0035), (120,-0.0043)
            # Fit: baseline -0.0025 + amplitude * cos(2*pi*|x|/period + phase)
            # with period ~ 50 and amplitude ~0.002, plus a slow negative trend.
            ax = abs(x)
            # slow trend toward -0.004 at large |x|
            trend = -0.004 * (1.0 - math.exp(-(ax * ax) / (2 * 60.0 * 60.0)))
            # oscillation: zero near |x|~7, min near |x|~12 and |x|~120,
            # local max near |x|~25-30, min again near |x|~40
            # cos with period ~55, phase chosen so cos=0 at ax=7:
            # 2*pi*7/55 + phase = pi/2  => phase = pi/2 - 2*pi*7/55
            period = 55.0
            phase = math.pi / 2 - 2 * math.pi * 7.0 / period
            osc = 0.0018 * math.cos(2 * math.pi * ax / period + phase)
            # damp the oscillation near 0 so it doesn't disturb the bump region
            damp = 1.0 - math.exp(-(ax * ax) / (2 * 5.0 * 5.0))
            far = trend + osc * damp

            val = main + right_bump + left_bump + far
            ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}
