import math

def predict(probe):
    # f(x) = 0 for |x| >= 1 [E2, E3, E4, E5]
    # Nonzero only for |x| < 1 [E2, E4]
    # Asymmetric: left side deeper than right [E4, E6]
    # At x=0: f=-1.7 [E2]
    # Left side (x<0): monotone decreasing toward -1, then drops to 0 at |x|>=1 [E4, E6]
    #   f(-0.02)=-1.7373, f(-0.15)=-2.0442, f(-0.35)=-2.7342, f(-0.5)=-3.425,
    #   f(-0.65)=-4.2643, f(-0.7)=-4.577, f(-0.8)=-5.252, f(-0.85)=0, f(-0.95)=0 [E6]
    #   So left nonzero only for -0.8 <= x < 0; zero for x <= -0.85 [E6]
    # Right side (x>0): min near x~0.25 (~-1.456), rises then drops to 0 [E4, E6]
    #   f(0.02)=-1.6653, f(0.15)=-1.5042, f(0.35)=-1.4742, f(0.5)=-1.625,
    #   f(0.7)=-2.057, f(0.8)=-2.372, f(0.85)=0, f(0.95)=0 [E6]
    #   So right nonzero only for 0 < x <= 0.8; zero for x >= 0.85 [E6]
    # Boundary: |x| in (0.8, 1) is zero on both sides [E6]
    left = [(-0.8, -5.252), (-0.7, -4.577), (-0.65, -4.2643), (-0.6, -3.968),
            (-0.5, -3.425), (-0.4, -2.948), (-0.35, -2.7342), (-0.3, -2.537),
            (-0.25, -2.3563), (-0.2, -2.192), (-0.15, -2.0442), (-0.1, -1.913),
            (-0.05, -1.7982), (-0.02, -1.7373), (0.0, -1.7)]
    right = [(0.0, -1.7), (0.02, -1.6653), (0.05, -1.6182), (0.1, -1.553),
             (0.15, -1.5042), (0.2, -1.472), (0.25, -1.4562), (0.3, -1.457),
             (0.35, -1.4742), (0.4, -1.508), (0.5, -1.625), (0.6, -1.808),
             (0.65, -1.9242), (0.7, -2.057), (0.8, -2.372)]

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
        if x <= -0.8 or x >= 0.8 or x == 0.0 and False:
            out.append(0.0)
        elif x < 0:
            out.append(interp(left, x))
        elif x > 0:
            out.append(interp(right, x))
        else:
            out.append(-1.7)
    return {"y": out}
