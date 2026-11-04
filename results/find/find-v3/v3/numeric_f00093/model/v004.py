def predict(probe):
    # f is piecewise smooth, symmetric-ish structure with a curved middle.
    # Observations show a smooth curve everywhere, not piecewise linear.
    # Region A: x <= -15, slope ~ -0.5 [E2]
    # Region B: -15 < x < 0, curved (quadratic-ish) [E4, E6]
    # Region C: 0 <= x, curved, slope steepens with x [E8, E6]
    # Breakpoint near x=0 [E4]
    # Right side is NOT linear: slope goes from ~-3.4 at x=0 to ~-0.5 at x=128 [E8]
    # Left side beyond -15 is linear slope -0.5 [E2]
    # Middle region: fit quadratic through (-15,15.926),(-8,10.7344),(0,-8.8302)
    # Right region: fit quadratic through (0,-8.8302),(8,-34.5556),(128,-71.1191)
    def f(x):
        if x <= -15:
            return 15.926 + (-0.5)*(x + 15)
        elif x < 0:
            a = -0.11359452
            b = -3.35433116
            c = -8.8302
            return a*x*x + b*x + c
        else:
            # quadratic through (0,-8.8302),(8,-34.5556),(128,-71.1191)
            # c = -8.8302
            # 64a + 8b = -34.5556 + 8.8302 = -25.7254
            # 16384a + 128b = -71.1191 + 8.8302 = -62.2889
            # From first: 8a + b = -3.215675 => b = -3.215675 - 8a
            # 16384a + 128(-3.215675 - 8a) = -62.2889
            # 16384a - 411.6064 - 1024a = -62.2889
            # 15360a = 349.3175 => a = 0.02274203
            # b = -3.215675 - 8*0.02274203 = -3.215675 - 0.18193624 = -3.39761124
            a = 0.02274203
            b = -3.39761124
            c = -8.8302
            return a*x*x + b*x + c
    return {"y": [f(x) for x in probe["x"]]}
