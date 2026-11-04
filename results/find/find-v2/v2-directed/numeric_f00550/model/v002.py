def predict(probe):
    # f is zero for |x| >= 1 [E1, E2]
    # Nonzero only on (-1, 1), a bump [E1, E2]
    # f(-0.5)=-3.425, f(0)=-1.7, f(0.5)=-1.625 [E1]
    # Fine shape: f(-0.75)=-4.9062, f(-0.6)=-3.968, f(0.6)=-1.808, f(0.75)=-2.2062 [E2]
    # Not a quadratic: at -0.75 the quadratic overshoots (-6.7 vs -4.9) [E2]
    # Looks like a smooth bump that is zero at |x|>=1 and dips to ~-4.9 near -0.75
    # Try a form: f(x) = A * (1 - x^2) * something? Let's fit a quartic-ish shape.
    # Observed values suggest a bump peaked around x=-0.7 to -0.75 with value ~-4.9
    # and asymmetric: left side steeper/deeper than right.
    # Guess: f(x) = (1 - x^2) * (a + b*x + c*x^2) ... but must be zero at |x|=1.
    # Fit through points: use a polynomial times (1-x^2).
    # Let g(x) = f(x)/(1-x^2) for interior points.
    # x=-0.75: 1-x^2=0.4375, g=-11.214
    # x=-0.6: 0.64, g=-6.2
    # x=-0.4: 0.84, g=-3.5095
    # x=-0.2: 0.96, g=-2.2833
    # x=0: 1, g=-1.7
    # x=0.2: 0.96, g=-1.5333
    # x=0.4: 0.84, g=-1.7952
    # x=0.6: 0.64, g=-2.825
    # x=0.75: 0.4375, g=-5.0427
    # g looks like a quadratic in x? g(0)=-1.7, g(-0.75)=-11.2, g(0.75)=-5.04
    # Not symmetric. Try g(x) = a + b*x + c*x^2.
    # From g(0)=-1.7 -> a=-1.7
    # g(0.75)=-5.0427: -1.7 + 0.75b + 0.5625c = -5.0427 -> 0.75b+0.5625c=-3.3427
    # g(-0.75)=-11.214: -1.7 -0.75b + 0.5625c = -11.214 -> -0.75b+0.5625c=-9.514
    # add: 1.125c = -12.857 -> c=-11.428; then 0.75b = -3.3427+6.428=3.085 -> b=4.114
    # Check g(0.6): -1.7+4.114*0.6-11.428*0.36 = -1.7+2.468-4.114=-3.346 vs actual -2.825. Off.
    # Try cubic in g? Let's just fit a polynomial to f directly with (1-x^2) factor and cubic g.
    # Use least squares mentally is hard; instead use a smooth interpolation.
    # Simpler: piecewise linear interpolation through observed points, zero outside.
    import math
    pts = [(-0.9,0.0),(-0.75,-4.9062),(-0.6,-3.968),(-0.4,-2.948),(-0.3,-2.537),
           (-0.2,-2.192),(-0.1,-1.913),(-0.05,-1.7982),(0.05,-1.6182),(0.1,-1.553),
           (0.2,-1.472),(0.3,-1.457),(0.4,-1.508),(0.6,-1.808),(0.75,-2.2062),(0.9,0.0)]
    out = []
    for x in probe.get("x", []):
        try:
            if x is None or x <= -1 or x >= 1:
                out.append(-0.0)
            else:
                # linear interpolation
                if x <= pts[0][0]:
                    out.append(0.0)
                elif x >= pts[-1][0]:
                    out.append(0.0)
                else:
                    for i in range(len(pts)-1):
                        x0,y0 = pts[i]; x1,y1 = pts[i+1]
                        if x0 <= x <= x1:
                            t = (x-x0)/(x1-x0)
                            out.append(y0 + t*(y1-y0))
                            break
                    else:
                        out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
