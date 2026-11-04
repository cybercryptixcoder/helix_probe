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
            # Piecewise model based on E1 observations.
            # Near-zero plateau/dip region.
            if -1.0 <= x <= 0.5:
                # interpolate roughly: f(-1)=-46.0, f(-0.5)=-47.3875, f(0)=-48.6, f(0.5)=-48.6625
                # simple quadratic-ish fit through these
                y = -48.6 + 2.6 * x + 0.0 * x * x
                # refine using known points
                if x <= 0:
                    y = -48.6 + 2.6 * x
                else:
                    y = -48.6 - 0.125 * x
                ys.append(y)
            elif x > 0.5:
                # positive branch: exponential-like growth
                # fit log-ish: use base growth. f(2)=-32.2, f(3)=2.4, f(4)=65, f(8)=751.4
                # Try form a*exp(b*x)+c for x>=2
                if x >= 2:
                    # fit through (2,-32.2),(4,65),(8,751.4),(16,5839.4)
                    # approximate: y = A*exp(k*x) + c
                    # Using (4,65) and (8,751.4): ratio ~11.56 over 4 units -> k=ln(11.56)/4=0.611
                    # Using (8,751.4) and (16,5839.4): ratio 7.77 over 8 -> k=0.256... not constant
                    # Try y = a*x^b*exp(c*x)
                    # Simpler: interpolate in log space using known anchors
                    anchors = [(2,-32.2),(3,2.4),(4,65.0),(8,751.4),(16,5839.4),(32,44853.8),(64,350057.0),(128,2763727.4)]
                    y = _interp_log(anchors, x)
                    ys.append(y)
                else:
                    # 0.5 < x < 2: interpolate between (0.5,-48.6625),(1,-46.6),(2,-32.2)
                    anchors = [(0.5,-48.6625),(1,-46.6),(2,-32.2)]
                    y = _interp_lin(anchors, x)
                    ys.append(y)
            else:
                # x < -1
                if x <= -8:
                    anchors = [(-8,-554.2),(-16,-4759.0),(-32,-40240.6),(-128,-2688458.2)]
                    y = _interp_log_neg(anchors, x)
                    ys.append(y)
                else:
                    # -8 < x < -1: interpolate between (-8,-554.2),(-4,-88.6),(-3,-58.2),(-2,-46.6),(-1,-46.0)
                    anchors = [(-8,-554.2),(-4,-88.6),(-3,-58.2),(-2,-46.6),(-1,-46.0)]
                    y = _interp_lin(anchors, x)
                    ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}


def _interp_lin(anchors, x):
    # linear interpolation, extrapolate with nearest slope
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
    # interpolate log(|y|) for positive branch (y can be negative near x=2)
    # handle sign separately: use signed log
    pts = [(ax, _slog(ay)) for ax, ay in anchors]
    s = _interp_lin(pts, x)
    return _sexp(s)


def _interp_log_neg(anchors, x):
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
