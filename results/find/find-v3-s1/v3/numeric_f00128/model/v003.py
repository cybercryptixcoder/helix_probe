import math

def predict(probe):
    # f is piecewise linear with three regimes [E2, E4]:
    #   x <= -2: slope -6.7601  [E2]
    #   x >=  2: slope -16.8999 [E2]
    #   -2 < x < 2: smooth transition, NOT linear [E4]
    # E4 shows the transition is smooth (curved), with slopes matching
    # the outer lines at the endpoints (-2 and 2) and steeper in the middle.
    # At x=-2: slope ~ -6.76 (matches left line)
    # At x= 2: slope ~ -16.90 (matches right line)
    # Middle is steeper than linear interp -> convex/concave blend.
    #
    # Fit a cubic Hermite on [-2,2] with:
    #   y(-2)=15.9142, y(2)=-22.6804
    #   y'(-2)=-6.7601, y'(2)=-16.8999
    # Check against E4 points.
    #
    # Left line: through (-128, 867.6846), slope -6.7601
    #   y = 867.6846 - 6.7601*(x+128)
    # Right line: through (128, -2151.9921), slope -16.8999
    #   y = -2151.9921 - 16.8999*(x-128)

    SL = -6.7601
    SR = -16.8999
    # anchor points
    xL, yL = -128.0, 867.6846
    xR, yR = 128.0, -2151.9921

    # Hermite on [-2,2]
    a, b = -2.0, 2.0
    ya, yb = 15.9142, -22.6804
    ma, mb = SL, SR
    h = b - a  # 4

    def hermite(x):
        t = (x - a) / h
        t2 = t*t
        t3 = t2*t
        h00 = 2*t3 - 3*t2 + 1
        h10 = t3 - 2*t2 + t
        h01 = -2*t3 + 3*t2
        h11 = t3 - t2
        return h00*ya + h10*h*ma + h01*yb + h11*h*mb

    def f(x):
        if x <= a:
            return yL + SL*(x - xL)
        elif x >= b:
            return yR + SR*(x - xR)
        else:
            return hermite(x)

    return {"y": [f(x) for x in probe["x"]]}
