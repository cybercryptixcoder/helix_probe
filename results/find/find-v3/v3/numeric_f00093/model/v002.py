def predict(probe):
    # f is piecewise linear [E2].
    # Region A: x <= -15, slope ~ -0.5 (y rises as x falls) [E2]
    # Region B: -15 < x < 0, steep transition slope ~ -1.65 [E2]
    # Region C: x >= 0, slope ~ -0.55 [E2]
    # E1 points are consistent with these slopes (roughly).
    def f(x):
        if x <= -15:
            # anchor at x=-15, y=15.926, slope -0.5
            return 15.926 + (-0.5)*(x + 15)
        elif x < 0:
            # from (-15,15.926) to (0,-8.8302): slope = (-8.8302-15.926)/15 = -1.6504
            return 15.926 + (-1.6504)*(x + 15)
        else:
            # anchor at x=0, y=-8.8302, slope -0.55
            return -8.8302 + (-0.55)*x
    return {"y": [f(x) for x in probe["x"]]}
