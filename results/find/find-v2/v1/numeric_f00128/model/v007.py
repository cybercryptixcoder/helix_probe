def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            if x >= 0:
                if x >= 2.0:
                    # Linear law 11.0 - 16.9*x fits x>=2 well (E17)
                    ys.append(11.0 - 16.9 * x)
                elif x >= 1.0:
                    # Linear segment from x=1 to x=2 (E15,E18,E20)
                    # f(1) = -5.3245, f(2) = -22.6804
                    # Slight curvature: slope ~-17.5 near x=1, ~-17.0 near x=2
                    # Fit quadratic through (1,-5.3245),(1.5,-13.7572),(2,-22.6804)
                    # Use piecewise linear with midpoint anchor
                    if x <= 1.5:
                        # slope from 1 to 1.5: (-13.7572 - -5.3245)/0.5 = -16.8654
                        ys.append(-5.3245 + (-16.8654) * (x - 1.0))
                    else:
                        # slope from 1.5 to 2: (-22.6804 - -13.7572)/0.5 = -17.8464
                        ys.append(-13.7572 + (-17.8464) * (x - 1.5))
                else:
                    # Near-zero steep curve x in [0,1), fit to E19
                    # f(0)=5.4186, f(0.25)=4.4171, f(0.5)=2.1182, f(0.75)=-1.3675, f(1)=-5.3245
                    # Cubic fit through these
                    # f(x) = 5.4186 + a*x + b*x^2 + c*x^3
                    # Use least squares intuition from E19 points
                    # Try f(x) = 5.4186 - 3.5*x - 5.0*x^2 - 2.5*x^3
                    # x=0.25: 5.4186-0.875-0.3125-0.0391=4.192 (obs 4.417)
                    # x=0.5: 5.4186-1.75-1.25-0.3125=2.106 (obs 2.118) good
                    # x=0.75: 5.4186-2.625-2.8125-1.0547=-1.074 (obs -1.367)
                    # x=0.9: 5.4186-3.15-4.05-1.8225=-3.604 (obs -3.757)
                    # Try f(x) = 5.4186 - 3.0*x - 6.0*x^2 - 2.0*x^3
                    # x=0.25: 5.4186-0.75-0.375-0.03125=4.262 (obs 4.417)
                    # x=0.5: 5.4186-1.5-1.5-0.25=2.169 (obs 2.118)
                    # x=0.75: 5.4186-2.25-3.375-0.84375=-1.050 (obs -1.367)
                    # x=0.9: 5.4186-2.7-4.86-1.458=-3.599 (obs -3.757)
                    # x=1.0: 5.4186-3.0-6.0-2.0=-5.581 (obs -5.3245)
                    # Try f(x) = 5.4186 - 3.2*x - 5.5*x^2 - 2.0*x^3
                    # x=0.25: 5.4186-0.8-0.34375-0.03125=4.244 (obs 4.417)
                    # x=0.5: 5.4186-1.6-1.375-0.25=2.194 (obs 2.118)
                    # x=0.75: 5.4186-2.4-3.09375-0.84375=-0.919 (obs -1.367)
                    # x=0.9: 5.4186-2.88-4.455-1.458=-3.374 (obs -3.757)
                    # x=1.0: 5.4186-3.2-5.5-2.0=-5.281 (obs -5.3245) good
                    # Use f(x) = 5.4186 - 3.2*x - 5.5*x^2 - 2.0*x^3
                    val = 5.4186 - 3.2 * x - 5.5 * x * x - 2.0 * x * x * x
                    ys.append(val)
            else:
                # Negative side: exact linear law -6.8*x + 5.42, softened near zero
                b = -6.8
                c = 5.42
                ax = abs(x)
                g = b * x * ax / (ax + 0.6)
                ys.append(g + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
