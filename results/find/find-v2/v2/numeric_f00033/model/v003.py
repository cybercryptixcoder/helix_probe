import math

def predict(probe):
    # Beliefs:
    # 1. f is a smooth bump peaking near x=0: f(0)≈0.3868, f(1)≈0.255, f(2)≈0.12,
    #    f(3)≈0.0327, f(4)≈0.0099, f(5)≈0.0012, f(6)≈0.0001 [E2, E4].
    # 2. The bump is asymmetric: left side decays slower than right side.
    #    f(-1)≈0.197, f(-2)≈0.0575, f(-3)≈0.0053, f(-4)≈0.0002 [E2, E4].
    # 3. For |x| large the output is a small negative constant around -0.003,
    #    with a shallow dip near x≈-60 and x≈-102 [E1, E3, E5].
    # 4. Values near x≈±1.2 are on the main bump [E3, E4].
    # 5. The MLP is smooth; approximate with a Gaussian-like bump plus a
    #    constant negative baseline and a tiny far-field wiggle.

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

        # Main bump: asymmetric Gaussian-like shape.
        # Peak value ~0.3868 at 0.
        if x >= 0:
            # Right side: decays fast. Fit f(1)=0.255, f(2)=0.12, f(3)=0.0327.
            # log(f/0.3868) at x=1: log(0.659)= -0.417 -> sigma_r^2 = 1/(2*0.417)=1.20
            # at x=2: log(0.310)= -1.171 -> sigma_r^2 = 4/(2*1.171)=1.71
            # at x=3: log(0.0845)= -2.47 -> sigma_r^2 = 9/(2*2.47)=1.82
            # Use sigma_r^2 ~ 1.7 for larger x, but near 0 slightly wider.
            sig2 = 1.25 + 0.55 * min(x, 3.0) / 3.0
            bump = 0.3868 * math.exp(-x * x / (2.0 * sig2))
        else:
            # Left side: decays slower. f(-1)=0.197 -> ratio 0.509, log=-0.675
            # sigma_l^2 = 1/(2*0.675)=0.741
            # f(-2)=0.0575 -> ratio 0.1487, log=-1.906 -> sigma_l^2=4/(2*1.906)=1.049
            # f(-3)=0.0053 -> ratio 0.0137, log=-4.29 -> sigma_l^2=9/(2*4.29)=1.049
            # f(-4)=0.0002 -> ratio 0.000517, log=-7.57 -> sigma_l^2=16/(2*7.57)=1.057
            # So left sigma^2 ~ 1.05 for |x|>=2, narrower near 0.
            ax = -x
            sig2 = 0.74 + 0.31 * min(ax, 2.0) / 2.0
            bump = 0.3868 * math.exp(-x * x / (2.0 * sig2))

        # Far-field baseline: small negative offset, ~ -0.003, with a shallow
        # dip near x≈-60 (f≈-0.0032) and near x≈-102 (f≈-0.004).
        # Also slight negative trend for large positive x.
        baseline = -0.0008
        # dip near -60
        baseline += -0.0024 * math.exp(-((x + 60.0) ** 2) / (2.0 * 20.0 ** 2))
        # dip near -102
        baseline += -0.0032 * math.exp(-((x + 102.0) ** 2) / (2.0 * 15.0 ** 2))
        # slight negative for large positive x
        if x > 10:
            baseline += -0.0002 * min((x - 10.0) / 100.0, 1.0)

        # Combine: bump dominates near 0; baseline elsewhere.
        # The bump already goes to ~0 for |x|>5, so sum is fine.
        y = bump + baseline * (1.0 - math.exp(-bump / 0.01)) if bump > 1e-6 else bump + baseline
        # Simpler: y = bump + baseline * (1 - exp(-bump/0.005)) to blend.
        # Actually just add; bump is tiny where baseline matters.
        y = bump + baseline

        ys.append(y)
    return {"y": ys}
