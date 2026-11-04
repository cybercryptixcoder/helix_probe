import math

def predict(probe):
    # Beliefs:
    # 1. Main bump peaks at x=0 with f(0)=0.3868; smooth, asymmetric [E2,E4].
    # 2. Right side decays: f(1)=0.255, f(2)=0.12, f(3)=0.0327, f(4)=0.0099,
    #    f(5)=0.0012, f(6)=0.0001 [E2,E4].
    # 3. Left side decays slower: f(-1)=0.197, f(-2)=0.0575, f(-3)=0.0053,
    #    f(-4)=0.0002 [E2,E4].
    # 4. Far field (|x| large) is a slowly varying negative baseline that
    #    becomes more negative as x decreases: ~-0.0004 at x=-10, -0.0012 at
    #    -20, -0.0021 at -30, -0.003 at -40, -0.0032 at -50..-60, -0.0034 at
    #    -70, -0.0037 at -90, -0.0041 at -110, -0.0044 at -128 [E6].
    # 5. For large positive x baseline ~ -0.0003 to -0.0004 [E1,E3,E5].
    # 6. Near x=-5 there is a small positive bump (f(-5)=0.0027) [E6].

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

        # Far-field baseline: smooth function of x.
        # For x <= 0: use a smooth ramp from ~0 near x=0 down to -0.0044 at -128.
        # Fit roughly: baseline(x) = -0.0032 - 0.0012 * tanh((x+60)/40) for x<0
        # Check: x=-128: tanh(-68/40)=tanh(-1.7)=-0.935 -> -0.0032+0.00112=-0.00208 (too high)
        # Better: linear-ish in x for x<-40, saturating.
        if x < 0:
            # Piecewise smooth: near 0 rises to 0; far negative approaches -0.0044.
            # Use: baseline = -0.0032 + 0.0032*exp(-(x/25)^2) ... no.
            # Direct: baseline = -0.0044 + 0.0044*exp(-(-x/60)^1.5)? 
            # Simpler: interpolate key points smoothly.
            # Key: x=0 ->0 (bump covers), -5->0.0027 (small bump), -10->-0.0004,
            # -20->-0.0012, -30->-0.0021, -40->-0.003, -50->-0.0032,
            # -60->-0.0032, -70->-0.0034, -90->-0.0037, -110->-0.0041, -128->-0.0044
            # Approximate with: baseline = -0.0032 - 0.0012*tanh((-x-60)/50) for x<-40
            # and a smooth rise to 0 near 0.
            if x >= -40:
                # from 0 at x=0 to -0.003 at x=-40, roughly linear then curve
                t = -x / 40.0
                baseline = -0.003 * (t ** 1.3)
            else:
                baseline = -0.003 - 0.0014 * (1 - math.exp(-(-x - 40) / 50.0))
            # small positive bump near x=-5
            baseline += 0.0035 * math.exp(-((x + 5.0) ** 2) / (2.0 * 2.0 ** 2))
        else:
            # positive side: small negative, slightly more negative for larger x
            baseline = -0.0004 + 0.0001 * math.exp(-x / 20.0)

        y = bump + baseline
        ys.append(y)
    return {"y": ys}
