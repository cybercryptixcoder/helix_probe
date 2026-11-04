import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Positive side (x > 0): f = 13.1*x - 3.5 [E11,E12,E13,E15,E17]
    #   Single straight line confirmed from x=0.01 to 108.4.
    #
    # x == 0: f(0) = -385.12 [E2].
    #
    # Negative side: piecewise linear, with noise ~±1.
    #   Near 0 (x in [-1,0)): f ~ -11, roughly flat [E14,E16,E18].
    #     E18: -0.05->-10.97, -0.1->-10.03, -0.2->-10.16, -0.3->-10.29,
    #          -0.5->-8.56(noise), -0.7->-11.82, -1.0->-11.21.
    #     Values hover around -10.5 to -11.2. Use flat ~-10.9.
    #   For x <= -1: slope ~1.35, intercept ~-9.85 [E6,E8,E18].
    #     E18: -1->-11.21, -2->-10.52(noise), -3->-14.83, -4->-16.14,
    #          -5->-17.45, -6->-17.76, -7->-20.07, -8->-20.38, -9->-21.69,
    #          -10->-22.0, -11->-24.31, -12->-25.62, -15->-29.55.
    #     Fit -1 to -15: slope ~1.31, intercept ~-9.9.
    #     E6 -30->-50.2: 1.31*-30-9.9=-49.2, close.
    #     E4 -128->-178.58: 1.31*-128-9.9=-177.6, close.
    #   So x < -1: f = 1.31*x - 9.9.
    #   Transition at x=-1: near-0 gives -10.9, line gives -11.21. Close enough.

    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            x = float(x)
            if x == 0.0:
                y = -385.12
            elif x > 0.0:
                y = 13.1 * x - 3.5
            elif x >= -1.0:
                y = -10.9
            else:
                y = 1.31 * x - 9.9
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
