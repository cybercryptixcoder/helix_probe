import math

def predict(probe):
    # Model hypothesis:
    # - For |x| < 1: f(x) = 0  [E6, E8: all outputs -0.0 for |x|<1]
    # - For |x| > 1: f(x) = sign(x) * C * |x|^p, with sign-dependent coefficient.
    #   From E12: positive x: y = C+ * x^p ; negative x: y = -C- * |x|^p.
    #   Fit exponent p and coefficients from E12 data.
    # - At |x| = 1 exactly: boundary; treat as power law (|x|>1 branch) since
    #   E8 shows values just above 1 follow power law, just below are 0.
    #
    # Determine p from E12 positive side:
    #   x=14 -> 3405025.4 ; x=70 -> 57387033823.0
    #   ratio = 16855.7 over factor 5 in x => p = ln(16855.7)/ln(5) ~ 6.0
    # Check: 14^6 = 7529536 ; 3405025.4/7529536 = 0.4522
    #   70^6 = 117649000000 ; 57387033823/117649000000 = 0.4878
    # Not constant -> exponent not exactly 6. Let's solve properly.
    #
    # Use two points to get p and C+:
    #   ln(y) = ln(C+) + p ln(x)
    #   p = (ln y2 - ln y1)/(ln x2 - ln x1)
    # x=14,y=3405025.4 ; x=70,y=57387033823.0
    # p = (ln(57387033823)-ln(3405025.4))/(ln70-ln14)
    #   = (24.7729 - 15.0408)/1.60944 = 9.7321/1.60944 = 6.0469
    # Hmm. Let's check with x=32: 32^6.0469 = ?
    # Better: fit across all points numerically in code.
    #
    # Negative side: x=-14 -> -4360925.8 ; x=-70 -> -60410784077.0
    # ratio = 13852.7 => p = ln(13852.7)/ln5 = 9.5363/1.60944 = 5.925
    # So p differs slightly? Likely same p, coefficients differ.
    #
    # Let's just fit p from positive and negative separately and average,
    # then fit coefficients. But to be safe, compute p per sign.

    xs = probe["x"]
    ys = []

    # Fit parameters from E12 data (hardcoded as calibration constants).
    # Positive side points (x, y):
    pos = [(14.0,3405025.4),(16.0,7655972.8),(18.0,15642369.0),(22.0,52799210.2),
           (26.0,145217001.8),(32.0,509990115.2),(38.0,1440734831.0),
           (45.0,3998710975.5),(55.0,13416083939.5),(70.0,57387033823.0)]
    neg = [(14.0,4360925.8),(16.0,9525262.4),(18.0,19017790.2),(22.0,62028725.0),
           (26.0,166525941.4),(32.0,570243664.0),(38.0,1583116400.2),
           (45.0,4330460299.5),(55.0,14321263335.5),(70.0,60410784077.0)]

    def fit(points):
        # linear regression ln y = ln C + p ln x
        n = len(points)
        sx = sum(math.log(x) for x,_ in points)
        sy = sum(math.log(y) for _,y in points)
        sxx = sum(math.log(x)**2 for x,_ in points)
        sxy = sum(math.log(x)*math.log(y) for x,y in points)
        p = (n*sxy - sx*sy)/(n*sxx - sx*sx)
        lnC = (sy - p*sx)/n
        return p, math.exp(lnC)

    ppos, Cpos = fit(pos)
    pneg, Cneg = fit(neg)

    for x in xs:
        ax = abs(x)
        if ax < 1.0:
            ys.append(-0.0)
        else:
            if x > 0:
                ys.append(Cpos * (ax ** ppos))
            elif x < 0:
                ys.append(-Cneg * (ax ** pneg))
            else:
                ys.append(-0.0)
    return {"y": ys}
