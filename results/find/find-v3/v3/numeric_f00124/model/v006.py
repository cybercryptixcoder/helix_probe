def predict(probe):
    # Beliefs:
    # x>=0: y = 106.0528 + 111.4278*x [E2,E3,E4,E5,E7]
    # x<=-2: y = -25.4452 - 26.0717*x (linear tail) [E2,E6,E8]
    # Transition region -2<x<0: smooth curve, minimum near x=-1.05 (y~6.42).
    # E12 gives fresh intermediate samples that reveal the curve is NOT the
    #   quadratic v5 assumed. E12 points (x,y):
    #   -1.98:26.1768,-1.92:24.6125,-1.88:23.5696,-1.82:22.0053,-1.78:20.9625,
    #   -1.72:19.3982,-1.68:18.3553,-1.62:16.791,-1.58:15.7481,-1.52:14.1838,
    #   -1.48:13.141,-1.42:11.6851,-1.38:10.803,-1.32:9.4799,-1.28:8.6817,
    #   -1.22:7.7579,-1.18:7.2043,-1.12:6.5611,-1.08:6.3684,-1.02:6.5888
    # Compare with E10 at same/near x:
    #   -1.95:25.3946 (E10) vs interp E12 ~25.4 ✓
    #   -1.85:22.7875 (E10) vs E12 -1.88:23.57,-1.82:22.01 -> interp -1.85:22.79 ✓
    #   -1.75:20.1803 (E10) vs E12 -1.78:20.96,-1.72:19.40 -> interp -1.75:20.18 ✓
    #   -1.65:17.5731 (E10) vs E12 -1.68:18.36,-1.62:16.79 -> interp -1.65:17.57 ✓
    #   -1.55:14.966 (E10) vs E12 -1.58:15.75,-1.52:14.18 -> interp -1.55:14.97 ✓
    #   -1.45:12.3588 (E10) vs E12 -1.48:13.14,-1.42:11.69 -> interp -1.45:12.41 ✓
    #   -1.35:10.1415 (E10) vs E12 -1.38:10.80,-1.32:9.48 -> interp -1.35:10.14 ✓
    #   -1.25:8.2083 (E10) vs E12 -1.28:8.68,-1.22:7.76 -> interp -1.25:8.22 ✓
    #   -1.15:6.8547 (E10) vs E12 -1.18:7.20,-1.12:6.56 -> interp -1.15:6.88 ✓
    #   -1.05:6.4189 (E10) vs E12 -1.08:6.37,-1.02:6.59 -> interp -1.05:6.48 ✓
    # So E10 and E12 are CONSISTENT; the curve is smooth and well-determined.
    # The v5 quadratic was simply a poor fit; the true curve is steeper on the
    #   left branch (near -2) than a quadratic through 3 points suggested.
    # Build a dense monotone interpolation table from E8+E10+E12 combined.
    # Merge all transition points, sort, and linearly interpolate.
    pts = [
        (-2.0,26.6982),(-1.98,26.1768),(-1.95,25.3946),(-1.92,24.6125),
        (-1.88,23.5696),(-1.85,22.7875),(-1.82,22.0053),(-1.78,20.9625),
        (-1.75,20.1803),(-1.72,19.3982),(-1.68,18.3553),(-1.65,17.5731),
        (-1.62,16.791),(-1.58,15.7481),(-1.55,14.966),(-1.52,14.1838),
        (-1.48,13.141),(-1.45,12.3588),(-1.42,11.6851),(-1.38,10.803),
        (-1.35,10.1415),(-1.32,9.4799),(-1.28,8.6817),(-1.25,8.2083),
        (-1.22,7.7579),(-1.18,7.2043),(-1.15,6.8547),(-1.12,6.5611),
        (-1.08,6.3684),(-1.05,6.4189),(-1.02,6.5888),(-1.0,6.8494),
        (-0.95,8.2994),(-0.9,10.6298),(-0.85,14.0401),(-0.8,18.223),
        (-0.75,22.8773),(-0.72,25.9521),(-0.7,28.0616),(-0.68,30.2818),
        (-0.65,33.6247),(-0.6,39.1961),(-0.5,50.3388),
    ]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    def interp(x):
        # linear interpolation on sorted table
        if x <= xs[0]:
            # extrapolate using first segment slope
            s = (ys[1]-ys[0])/(xs[1]-xs[0])
            return ys[0] + s*(x-xs[0])
        if x >= xs[-1]:
            # extrapolate using last segment slope
            s = (ys[-1]-ys[-2])/(xs[-1]-xs[-2])
            return ys[-1] + s*(x-xs[-1])
        # binary search
        lo, hi = 0, len(xs)-1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if xs[mid] <= x:
                lo = mid
            else:
                hi = mid
        t = (x-xs[lo])/(xs[hi]-xs[lo])
        return ys[lo] + t*(ys[hi]-ys[lo])

    def f(x):
        if x >= -0.5:
            return 106.0528 + 111.4278*x
        elif x > -2.0:
            return interp(x)
        else:
            return -25.4452 - 26.0717*x
    return {"y": [f(x) for x in probe["x"]]}
