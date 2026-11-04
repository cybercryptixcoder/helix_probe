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
    if -2.0 <= x <= 2.0:
        d = x - 0.25
        if d < 0:
            a = 1.12
        else:
            a = 4.74
        return -48.84 + a * d * d

    if x > 2.0:
        # Far-positive plateau: f ~ 7773 for 98 <= x <= 117.5
        if 98.0 <= x <= 117.5:
            return 7773.0
        if 97.5 < x < 98.0:
            # sharp drop: log-linear from (97.5, 1226577) down to (98, 7773)
            return _interp_log([(97.5, 1226576.9625), (98.0, 7773.0)], x)
        if 117.5 < x < 118.0:
            # sharp jump: log-linear from (117.5, 7773) up to (118, 2167729.4)
            return _interp_log([(117.5, 7773.0), (118, 2167729.4)], x)
        anchors = [(2,-32.2),(2.25,-25.7484),(2.5,-17.9125),(2.75,-8.5703),
                   (3,2.4),(3.25,15.1203),(3.5,29.7125),(3.75,46.2984),
                   (4,65.0),(8,751.4),
                   (10,1465.4),(12,2509.8),(14,3947.0),(16,5839.4),
                   (18,8249.4),(20,11239.4),(24,19209.0),(28,30247.4),
                   (32,44853.8),(40,86767.4),(48,148943.4),(56,235375.4),
                   (64,350057.0),(80,680143.4),(96,1171151.4),
                   (97.5,1226576.9625),
                   (118,2167729.4),(120,2279279.4),(124,2513729.0),(128,2763727.4)]
        return _interp_log(anchors, x)

    if x <= -8:
        anchors = [(-8,-554.2),(-16,-4759.0),(-32,-40240.6),(-128,-2688458.2)]
        return _interp_log(anchors, x)
    else:
        anchors = [(-8,-554.2),(-7.5,-455.6625),(-7,-370.6),(-6.5,-298.0375),
                   (-6,-237.0),(-5.5,-186.5125),(-5,-145.6),(-4.5,-113.2875),
                   (-4,-88.6),(-3.5,-70.5625),(-3,-58.2),(-2.5,-50.5375),
                   (-2.25,-48.1641),(-2,-46.6)]
        return _interp_log(anchors, x)


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
