import math

def predict(probe):
    # f(x) = 0 outside (-1, 1) [E2, E3, E4, E5]
    # Nonzero only on (-1, 1); f(-1)=f(1)=0, f(-0.9)=0, f(0.9)=0 [E4]
    # f(-0.95)=0 and f(-0.85)=0, so left boundary is between -0.85 and -0.8 [E6]
    # f(0.75)=-2.2062, f(0.9)=0, so right boundary is between 0.75 and 0.9 [E4]
    # Inside the interval the shape is smooth, not piecewise-linear [E6]
    # Known points (x, y):
    #   (-0.8,-5.252),(-0.75,-4.9062),(-0.7,-4.577),(-0.65,-4.2643),
    #   (-0.6,-3.968),(-0.55,-3.6883),(-0.5,-3.425),(-0.45,-3.1783),
    #   (-0.4,-2.948),(-0.35,-2.7342),(-0.3,-2.537),(-0.25,-2.3563),
    #   (-0.2,-2.192),(-0.15,-2.0442),(-0.1,-1.913),(-0.05,-1.7982),
    #   (0,-1.7),(0.05,-1.6182),(0.1,-1.553),(0.15,-1.5042),(0.2,-1.472),
    #   (0.25,-1.4562),(0.35,-1.4742),(0.5,-1.625),(0.6,-1.808),
    #   (0.65,-1.9242),(0.75,-2.2062) [E2,E4,E6]
    # Shape: minimum near x=-0.8, rises to local max near x=0.25, then falls [E4,E6]
    # Looks like a smooth bump; try a polynomial fit through all points (?)
    pts = [
        (-0.8, -5.252),
        (-0.75, -4.9062),
        (-0.7, -4.577),
        (-0.65, -4.2643),
        (-0.6, -3.968),
        (-0.55, -3.6883),
        (-0.5, -3.425),
        (-0.45, -3.1783),
        (-0.4, -2.948),
        (-0.35, -2.7342),
        (-0.3, -2.537),
        (-0.25, -2.3563),
        (-0.2, -2.192),
        (-0.15, -2.0442),
        (-0.1, -1.913),
        (-0.05, -1.7982),
        (0.0, -1.7),
        (0.05, -1.6182),
        (0.1, -1.553),
        (0.15, -1.5042),
        (0.2, -1.472),
        (0.25, -1.4562),
        (0.35, -1.4742),
        (0.5, -1.625),
        (0.6, -1.808),
        (0.65, -1.9242),
        (0.75, -2.2062),
    ]
    # Left boundary between -0.85 and -0.8; right boundary between 0.75 and 0.9
    # Use a smooth interpolation (cubic-ish via monotone piecewise) on known points,
    # and taper to 0 at the boundaries.
    def f(x):
        if x <= -0.85 or x >= 0.9:
            return 0.0
        if x < -0.8:
            # taper from 0 at -0.85 to -5.252 at -0.8
            t = (x - (-0.85)) / (-0.8 - (-0.85))
            return -5.252 * t
        if x > 0.75:
            # taper from -2.2062 at 0.75 to 0 at 0.9
            t = (0.9 - x) / (0.9 - 0.75)
            return -2.2062 * t
        # linear interpolation between known points
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0
    return {"y": [f(x) for x in probe["x"]]}
