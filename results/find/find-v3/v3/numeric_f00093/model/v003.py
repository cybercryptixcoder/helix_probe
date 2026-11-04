def predict(probe):
    # f is piecewise linear, but with more regions than v2 assumed.
    # Region A: x <= -15, slope ~ -0.5 [E2]
    # Region B: -15 < x < 0, slope varies (curved), not constant -1.65 [E4]
    # Region C: 0 <= x, slope ~ -0.55 [E2, E3, E5]
    # Breakpoint near x=0 confirmed [E4]
    def f(x):
        if x <= -15:
            # anchor at x=-15, y=15.926, slope -0.5
            return 15.926 + (-0.5)*(x + 15)
        elif x < 0:
            # E4 shows curvature: slope steepens as x approaches 0.
            # Fit a quadratic through (-15,15.926), (-8,10.7344), (0,-8.8302)
            # Using quadratic y = a*x^2 + b*x + c
            # c = -8.8302 (at x=0)
            # At x=-15: 225a -15b -8.8302 = 15.926 => 225a -15b = 24.7562
            # At x=-8: 64a -8b -8.8302 = 10.7344 => 64a -8b = 19.5646
            # Solve: from second, 8a - b = 2.445575 => b = 8a - 2.445575
            # 225a -15(8a - 2.445575) = 24.7562 => 225a -120a + 36.683625 = 24.7562
            # 105a = -11.927425 => a = -0.11359452
            # b = 8*(-0.11359452) - 2.445575 = -0.90875616 - 2.445575 = -3.35433116
            a = -0.11359452
            b = -3.35433116
            c = -8.8302
            return a*x*x + b*x + c
        else:
            # anchor at x=0, y=-8.8302, slope -0.55
            return -8.8302 + (-0.55)*x
    return {"y": [f(x) for x in probe["x"]]}
