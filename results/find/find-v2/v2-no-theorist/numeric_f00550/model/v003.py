import math

def predict(probe):
    # f(x) = 0 outside (-1, 1) [E1, E2, E3]
    # Nonzero only on (-1, 1); f(-1)=f(1)=0, f(-0.9)=0 [E4]
    # Inside (-1,1) the shape is a smooth curve, not linear [E4]
    # Known points: (-0.75,-4.9062),(-0.6,-3.968),(-0.5,-3.425),(-0.25,-2.3563),
    #   (0,-1.7),(0.25,-1.4562),(0.5,-1.625),(0.6,-1.808),(0.75,-2.2062) [E2,E4]
    # Shape looks like a smooth function with a local max near x=0.25 and
    #   minima near the edges; fit a polynomial through the known points (?).
    pts = [
        (-1.0, 0.0),
        (-0.9, 0.0),
        (-0.75, -4.9062),
        (-0.6, -3.968),
        (-0.5, -3.425),
        (-0.25, -2.3563),
        (0.0, -1.7),
        (0.25, -1.4562),
        (0.5, -1.625),
        (0.6, -1.808),
        (0.75, -2.2062),
        (0.9, 0.0),
        (1.0, 0.0),
    ]
    def f(x):
        if x <= -1 or x >= 1:
            return 0.0
        # linear interpolation between known points (smooth-ish approximation)
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0
    return {"y": [f(x) for x in probe["x"]]}
