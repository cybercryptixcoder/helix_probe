import math

def predict(probe):
    # f(x) = 0 for |x| >= 1 [E1, E2, E3, E4]
    # Nonzero only for |x| < 1 [E2, E4]
    # Shape is asymmetric: left side deeper than right [E2, E4]
    # At x=0: f=-1.7 [E2]
    # Left side (x<0): f(-0.05)=-1.7982, f(-0.1)=-1.913, f(-0.2)=-2.192,
    #   f(-0.3)=-2.537, f(-0.4)=-2.948, f(-0.6)=-3.968, f(-0.75)=-4.9062 [E4]
    # Right side (x>0): f(0.05)=-1.6182, f(0.1)=-1.553, f(0.2)=-1.472,
    #   f(0.25)=-1.4562, f(0.3)=-1.457, f(0.4)=-1.508, f(0.6)=-1.808,
    #   f(0.75)=-2.2062 [E4]
    # Right side has a minimum near x~0.25 (around -1.456) then rises [E4]
    # Left side decreases monotonically toward -1 [E4]
    # Looks like log-ish / rational shape; fit with interpolation on known points
    # ?: use piecewise linear interpolation through observed points, 0 at |x|>=1
    left = [(-1.0, 0.0), (-0.9, 0.0), (-0.75, -4.9062), (-0.6, -3.968),
            (-0.4, -2.948), (-0.3, -2.537), (-0.25, -2.3563), (-0.2, -2.192),
            (-0.1, -1.913), (-0.05, -1.7982), (0.0, -1.7)]
    right = [(0.0, -1.7), (0.05, -1.6182), (0.1, -1.553), (0.2, -1.472),
             (0.25, -1.4562), (0.3, -1.457), (0.4, -1.508), (0.6, -1.808),
             (0.75, -2.2062), (0.9, 0.0), (1.0, 0.0)]

    def interp(pts, x):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0

    out = []
    for x in probe["x"]:
        if x < -1.0 or x > 1.0:
            out.append(0.0)
        elif x < 0:
            out.append(interp(left, x))
        else:
            out.append(interp(right, x))
    return {"y": out}
