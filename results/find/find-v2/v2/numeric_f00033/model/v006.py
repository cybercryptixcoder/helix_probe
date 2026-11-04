import math

def predict(probe):
    # Beliefs:
    # 1. Main bump peaks at x=0 with f(0)=0.3868; asymmetric [E2,E4].
    # 2. Right side: f(1)=0.255, f(2)=0.12, f(3)=0.0327, f(4)=0.0099,
    #    f(5)=0.0012, f(6)=0.0001 [E2,E4].
    # 3. Left side: f(-1)=0.197, f(-2)=0.0575, f(-3)=0.0053, f(-4)=0.0002 [E2,E4].
    # 4. Far negative baseline: -0.0004 at -10, -0.0012 at -20, -0.0021 at -30,
    #    -0.003 at -40, -0.0032 at -50..-60, -0.0034 at -70, -0.0037 at -90,
    #    -0.0041 at -110, -0.0044 at -128 [E6].
    # 5. Far positive baseline ~ -0.0001 to -0.0004, roughly flat [E1,E3,E5,E7].
    # 6. Small positive bump near x=-5 (f(-5)=0.0027, f(-5.9)=0.0003) [E6,E7].
    # 7. Negative trough centered ~x=11.5, min ~-0.0061 at x=12, width ~3 [E2,E7,E8].
    #    f(9)=-0.0032, f(10)=-0.0043, f(11)=-0.0054, f(12)=-0.0061, f(13)=-0.0055,
    #    f(14)=-0.0049, f(15)=-0.0043, f(16)=-0.0037, f(18)=-0.0025, f(20)=-0.0013,
    #    f(22)=-0.0004, f(25+)=-0.0004 [E8].

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(x) or math.isinf(x):
            ys.append(None)
            continue

        # Main bump: asymmetric Gaussian-like.
        if x >= 0:
            sig2 = 1.25 + 0.55 * min(x, 3.0) / 3.0
            bump = 0.3868 * math.exp(-x * x / (2.0 * sig2))
        else:
            ax = -x
            sig2 = 0.74 + 0.31 * min(ax, 2.0) / 2.0
            bump = 0.3868 * math.exp(-x * x / (2.0 * sig2))

        # Far-field baseline.
        if x < 0:
            if x >= -40:
                t = -x / 40.0
                baseline = -0.003 * (t ** 1.3)
            else:
                baseline = -0.003 - 0.0014 * (1 - math.exp(-(-x - 40) / 50.0))
            # small positive bump near x=-5
            baseline += 0.0035 * math.exp(-((x + 5.0) ** 2) / (2.0 * 2.0 ** 2))
        else:
            baseline = -0.0003

        # Negative trough around x~11.5 (visible on right side).
        trough = -0.0058 * math.exp(-((x - 11.5) ** 2) / (2.0 * 3.0 ** 2))

        y = bump + baseline + trough
        ys.append(y)
    return {"y": ys}
