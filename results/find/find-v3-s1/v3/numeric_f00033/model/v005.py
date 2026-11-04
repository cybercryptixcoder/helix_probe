import math

def predict(probe):
    # Beliefs (revised):
    # - f is a smooth unimodal bump centered near x=0, peak ~0.3868 at x=0 [E2,E4]
    # - The bump is asymmetric: right side falls faster than left [E2,E4]
    #   e.g. f(1)=0.255, f(-1)=0.1972; f(2)=0.12, f(-2)=0.0575
    # - Far field is NOT a constant: it drifts, roughly -0.004 at large |x|
    #   and ~0 near |x|~6-8, with a small positive shoulder near |x|~4 [E6]
    # - There is a small secondary positive bump around x=+4 (0.0185 at 3.5,
    #   0.0099 at 4) and a milder one on the left near x=-4 (0.0053) [E6]
    # - Values are noisy at ~0.001 level [E1,E3,E5]
    # - Model: asymmetric Gaussian main bump + small secondary bumps
    #   + smooth far-field drift.

    xs = probe["x"]
    ys = []
    for x in xs:
        try:
            # Main asymmetric bump: different sigma on each side
            peak = 0.3868
            if x >= 0:
                sigma = 1.55
            else:
                sigma = 1.85
            main = peak * math.exp(-(x * x) / (2 * sigma * sigma))

            # Secondary bumps near +/-4
            right_bump = 0.0185 * math.exp(-((x - 3.7) ** 2) / (2 * 0.9 * 0.9))
            left_bump = 0.0060 * math.exp(-((x + 4.0) ** 2) / (2 * 1.0 * 1.0))

            # Far-field drift: negative at large |x|, near zero around |x|~7
            # Approximate with a gentle negative term growing with |x|
            ax = abs(x)
            drift = -0.004 * (1.0 - math.exp(-(ax * ax) / (2 * 9.0 * 9.0)))
            # small negative dip around |x|~10-15 then back toward -0.004
            # (E6 shows -0.0043 at 10 and 15, -0.0004 at 25) -> add a dip
            dip = -0.0005 * math.exp(-((ax - 12.0) ** 2) / (2 * 4.0 * 4.0))

            val = main + right_bump + left_bump + drift + dip
            ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}
