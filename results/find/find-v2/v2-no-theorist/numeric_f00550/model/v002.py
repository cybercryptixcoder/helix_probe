def predict(probe):
    # f(x) = 0 for all x except a small interval around 0 [E1, E2]
    # Nonzero only at x = -0.5, 0, 0.5 in E2; zero at x = -1 and x = 1 [E2]
    # Values: f(-0.5) = -3.425, f(0) = -1.7, f(0.5) = -1.625 [E2]
    # Hypothesis (?): a narrow bump/well on (-1, 1), zero outside.
    #   Exact shape unknown; interpolate linearly between known points,
    #   with zero at the endpoints -1 and 1.
    def f(x):
        if x <= -1 or x >= 1:
            return 0.0
        # piecewise-linear through (-1,0), (-0.5,-3.425), (0,-1.7), (0.5,-1.625), (1,0)
        pts = [(-1.0, 0.0), (-0.5, -3.425), (0.0, -1.7), (0.5, -1.625), (1.0, 0.0)]
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0
    return {"y": [f(x) for x in probe["x"]]}
