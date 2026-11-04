import math

def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            ys.append(_f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}


def _f(x):
    # Near-zero dip: parabola centered at 0.25 with min -48.84
    # Fit through (0.25, -48.84), (-1.5, -45.41), (1.5, -41.44)
    # Use quadratic a*(x-0.25)^2 + c with c=-48.84
    # At x=-1.5: a*(1.75)^2 = 3.43 -> a=1.12
    # At x=1.5: a*(1.25)^2 = 7.40 -> a=4.74  (asymmetric)
    # Use asymmetric quadratic
    if -2.0 <= x <= 2.0:
        d = x - 0.25
        if d < 0:
            a = 1.12
        else:
            a = 4.74
        return -48.84 + a * d * d

    if x > 2.0:
        anchors = [(2,-32.2),(3,2.4),(4,65.0),(8,751.4),(16,5839.4),
                   (32,44853.8),(64,350057.0),(128,2763727.4)]
        return _interp_log(anchors, x)

    # x < -2.0
    if x <= -8:
        anchors = [(-8,-554.2),(-16,-4759.0),(-32,-40240.6),(-128,-2688458.2)]
        return _interp_log(anchors, x)
    else:
        # -8 < x < -2: bridge from dip edge to (-8,-554.2)
        # dip at x=-2: -48.84 + 1.12*(2.25)^2 = -48.84 + 5.67 = -43.17
        anchors = [(-8,-554.2),(-4,-88.6),(-3,-58.2),(-2,-43.17)]
        return _interp_lin(anchors, x)


def _interp_lin(anchors, x):
    anchors = sorted(anchors)
    if x <= anchors[0][0]:
        (x0,y0),(x1,y1) = anchors[0], anchors[1]
        return y0 + (y1-y0)*(x-x0)/(x1-x0)
    if x >= anchors[-1][0]:
        (x0,y0),(x1,y1) = anchors[-2], anchors[-1]
        return y1 + (y1-y0)*(x-x1)/(x1-x0)
    for i in range(len(anchors)-1):
        (x0,y0),(x1,y1) = anchors[i], anchors[i+1]
        if x0 <= x <= x1:
            return y0 + (y1-y0)*(x-x0)/(x1-x0)
    return anchors[-1][1]


def _interp_log(anchors, x):
    pts = [(ax, _slog(ay)) for ax, ay in anchors]
    s = _interp_lin(pts, x)
    return _sexp(s)


def _slog(y):
    if y == 0:
        return 0.0
    return math.copysign(math.log(abs(y)), y)


def _sexp(s):
    if s == 0:
        return 0.0
    return math.copysign(math.exp(abs(s)), s)
