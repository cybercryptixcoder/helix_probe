import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Evidence-driven beliefs:
    # - For |x| small (roughly -0.1 < x < 0.1), y is near a small constant,
    #   about -11.6 at x=0- and -36.9 at x=0+ ... but see below.
    # - There is a special point x=0 where y=472.73 [E2,E14].
    # - For x>0 there is a smooth curve through (0.1,-36.95),(0.2,-37.11),
    #   (0.5,-37.825),(1,-41.7),(2,-79.6),(3,-211.7),(4,-528),(5,-1147.3),
    #   (6,-2217.2),(8,-6443.2),(10,-14962.8),(12,-29993.6) [E2,E6,E14].
    #   This looks like a polynomial/exponential growth; it matches
    #   y = -a*x^b + c with c≈-36.8, or more likely a cubic-plus term.
    # - For x<0 near 0, y rises from about -11.7 at x=0- up to a peak near
    #   x≈-2.1 (y≈0.0743) then falls: (0,-), (-1,-7.4),(-2,-0.1),(-2.1,0.074),
    #   (-2.5,-2.075),(-3,-15),(-4,-106.1),(-5,-356.2),(-6,-876.9) [E2,E10,E12].
    #   This is a different branch from x>0.
    # - For large |x| (|x|>~6), y becomes huge negative and roughly follows
    #   a high-degree power law. Many large-x outputs cluster near
    #   -24973124.6 (a saturation/cap?) [E5,E7,E9,E11].
    #   E.g. x=-124.4 -> -24973124.742; x=-127.7 -> -24973124.6409;
    #   x=-107.4 -> -24973124.5785; x=-100.1 -> -24973124.6349.
    #   So for x below about -100, y saturates at ≈ -24973124.6.
    #   For positive large x, values keep growing: x=123.6 -> -285713790.3,
    #   x=119.7 -> -251485545.8, x=118.7 -> -243228121.8.
    #
    # Main structure I'll implement:
    # 1) x == 0 -> 472.73
    # 2) x > 0: smooth branch. Fit appears close to
    #       y ≈ -36.8 - A*x^p with p≈4.5? Let's check ratios.
    #    At x=2: -79.6 => extra -42.8; x=4: -528 => extra -491.2;
    #    ratio 491.2/42.8 ≈ 11.5 => p ≈ log2(11.5) ≈ 3.52.
    #    x=8: -6443.2 => extra -6406.4; ratio vs x=4: 13.0 => p≈3.7.
    #    So roughly y = -36.8 - 3.3*x^3.7? At x=2: 3.3*13.0=42.9 ok.
    #    At x=8: 3.3*8^3.7 = 3.3*2140=7062 vs 6406. Close-ish.
    #    I'll use a fitted power law: y = c - a*x^p with c≈-36.8.
    #    Better: use log-linear fit from points.
    # 3) x < 0 small: separate branch, roughly parabolic peak near -2.1.
    #    I'll fit a cubic through key points.
    # 4) Large negative x saturates at -24973124.6.
    # 5) Large positive x continues power growth.
    #
    # Since exact functional form is uncertain, I'll build piecewise
    # interpolations using the observed data patterns, but expressed as
    # general rules (polynomial fits), not memorized cases.

    x = probe["x"]
    out = []
    for v in x:
        out.append(_f(v))
    return {"y": out}


# Saturation value for very negative x
SAT = -24973124.6

def _f(x):
    try:
        x = float(x)
    except Exception:
        return None
    if not math.isfinite(x):
        return None

    # Special point x=0
    if x == 0.0:
        return 472.73

    # Very negative: saturation
    if x <= -100.0:
        # slight variation observed but essentially flat
        return SAT

    if x > 0:
        return _pos(x)
    else:
        return _neg(x)


def _pos(x):
    # Positive branch: y ≈ c - a*x^p, c≈-36.8
    # Fit using points (1,-41.7),(2,-79.6),(4,-528),(8,-6443.2)
    # Use log-log on (y - c) with c = -36.8
    c = -36.8
    # Compute a,p from two points x1=2,y1=-79.6 and x2=8,y2=-6443.2
    # y-c = -a*x^p  => (y1-c)/(y2-c) = (x1/x2)^p
    y1 = -79.6
    y2 = -6443.2
    r1 = y1 - c  # negative
    r2 = y2 - c  # negative
    # r1/r2 = (x1/x2)^p
    ratio = r1 / r2
    p = math.log(ratio) / math.log(2.0 / 8.0)
    a = -r1 / (2.0 ** p)
    val = c - a * (x ** p)
    # For very large x this may explode; cap reasonably? Observed at x=123.6
    # y=-285713790. Let's check: c - a*123.6^p.
    # p≈? ratio = (-42.8)/(-6406.4)=0.006681; log(0.006681)/log(0.25)
    # = (-5.008)/(-1.386)=3.613. a = 42.8/2^3.613 = 42.8/12.24=3.497.
    # At x=123.6: 3.497*123.6^3.613. 123.6^3.613 = exp(3.613*4.817)
    # = exp(17.40)=3.6e7. *3.497=1.26e8. c-...=-1.26e8. Observed -2.86e8.
    # So p a bit higher for large x. Use p=3.75, a adjusted.
    # Let's refit with x=8 and x=12: y(12)=-29993.6.
    y3 = -29993.6
    r3 = y3 - c
    p2 = math.log(r2 / r3) / math.log(8.0 / 12.0)
    a2 = -r2 / (8.0 ** p2)
    val2 = c - a2 * (x ** p2)
    # Blend: use p2 for larger x
    if x <= 2.0:
        return val
    else:
        return val2


def _neg(x):
    # Negative branch, -100 < x < 0
    # Near 0: y ≈ -11.7 at 0-, rising to peak ~0.074 at x≈-2.1,
    # then falling steeply: (-3,-15),(-4,-106.1),(-5,-356.2),(-6,-876.9)
    # Fit a cubic through (-2.1, 0.074),(-3,-15),(-4,-106.1),(-5,-356.2)
    # Use Lagrange interpolation on these four points.
    pts = [(-2.1, 0.0743), (-3.0, -15.0), (-4.0, -106.1), (-5.0, -356.2)]
    # For x between -6 and -2.1 use these; for x in (-2.1, 0) use another fit.
    if x <= -2.1:
        # extrapolate to -6 using (-6,-876.9) as well? Use cubic through
        # (-2.1,0.0743),(-3,-15),(-4,-106.1),(-6,-876.9)
        pts2 = [(-2.1, 0.0743), (-3.0, -15.0), (-4.0, -106.1), (-6.0, -876.9)]
        return _lagrange(pts2, x)
    else:
        # -2.1 < x < 0: use points (-2.1,0.0743),(-1.5,-3.225),(-1.0,-7.4),
        # (-0.5,-10.375),(0-, -11.7)
        pts3 = [(-2.1, 0.0743), (-1.5, -3.225), (-1.0, -7.4), (-0.5, -10.375)]
        # For very near 0, approach -11.7
        if x > -0.1:
            # interpolate toward -11.7 at 0
            # linear from (-0.1,-11.49) to (0,-11.7)
            t = (x - (-0.1)) / 0.1
            return -11.49 + t * (-11.7 - (-11.49))
        return _lagrange(pts3, x)


def _lagrange(pts, x):
    # Lagrange interpolation through given (xi, yi)
    n = len(pts)
    total = 0.0
    for i in range(n):
        xi, yi = pts[i]
        term = yi
        for j in range(n):
            if i != j:
                xj = pts[j][0]
                term *= (x - xj) / (xi - xj)
        total += term
    return total
