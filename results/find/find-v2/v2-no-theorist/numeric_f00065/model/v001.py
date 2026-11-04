def predict(probe):
    # Model: f(x) is approximately linear over the whole domain.
    # Fit from E1: slope ~ -2.6, intercept ~ 0.5 (rough).
    # Check E1 points: x=88.2 -> -228.97; x=66 -> -173.49; x=-20.3 -> 26.97;
    #   x=-61.7 -> 99.56; x=2.9 -> -15.84; x=-24.3 -> 33.98; x=72.7 -> -190.23;
    #   x=-50.4 -> 79.75; x=-6 -> 1.91; x=21.3 -> -61.81
    # Slope estimates: (-228.97 - (-173.49))/(88.2-66) = -55.48/22.2 = -2.499
    #   (-173.49 - 26.97)/(66 - (-20.3)) = -200.46/86.3 = -2.323
    #   (26.97 - 99.56)/(-20.3 - (-61.7)) = -72.59/41.4 = -1.753
    #   Not perfectly linear; slope varies. Try fitting y = a*x + b.
    # Using x=88.2,y=-228.97 and x=-61.7,y=99.56: a = (-228.97-99.56)/(88.2+61.7)
    #   = -328.53/149.9 = -2.192; b = -228.97 + 2.192*88.2 = -228.97+193.3 = -35.6
    # Check x=66: -2.192*66 - 35.6 = -144.7-35.6 = -180.3 vs -173.49 (off 7)
    # Check x=-20.3: 44.5-35.6 = 8.9 vs 26.97 (off 18)
    # Check x=2.9: -6.36-35.6 = -41.9 vs -15.84 (off 26)
    # Not linear. Try quadratic? Let's look at residuals vs x.
    # x: 88.2, 66, -20.3, -61.7, 2.9, -24.3, 72.7, -50.4, -6, 21.3
    # y: -228.97,-173.49,26.97,99.56,-15.84,33.98,-190.23,79.75,1.91,-61.81
    # y/x roughly: -2.596, -2.629, -1.329, -1.614, -5.46, -1.398, -2.617, -1.582, -0.318, -2.902
    # Hmm. Try y = -2.6*x + something? 
    # x=88.2: -2.6*88.2 = -229.3 vs -228.97 (close!)
    # x=66: -171.6 vs -173.49 (close)
    # x=-20.3: 52.78 vs 26.97 (off)
    # x=-61.7: 160.4 vs 99.56 (off)
    # x=2.9: -7.54 vs -15.84
    # x=-24.3: 63.18 vs 33.98
    # x=72.7: -189.0 vs -190.23 (close)
    # x=-50.4: 131.0 vs 79.75 (off)
    # x=-6: 15.6 vs 1.91
    # x=21.3: -55.38 vs -61.81
    # For positive x it's close to -2.6x. For negative x it's less negative (smaller magnitude).
    # Maybe f(x) = -2.6*x for x>0, and something else for x<0?
    # x=-20.3: 26.97 / -20.3 = -1.329
    # x=-61.7: 99.56/-61.7 = -1.614
    # x=-24.3: 33.98/-24.3 = -1.398
    # x=-50.4: 79.75/-50.4 = -1.582
    # x=-6: 1.91/-6 = -0.318
    # Not constant. Maybe f(x) = -2.6*x for x>0, and for x<0 something like -1.5*x + c?
    # x=-20.3: -1.5*-20.3 = 30.45 vs 26.97
    # x=-61.7: 92.55 vs 99.56
    # x=-24.3: 36.45 vs 33.98
    # x=-50.4: 75.6 vs 79.75
    # x=-6: 9 vs 1.91
    # Roughly -1.5x for negative. But x=-6 gives 1.91, -1.5*-6=9. Hmm.
    # Maybe it's a smooth curve. Let's try y = -2.6*x for x>0 and y = -1.5*x - 3 for x<0?
    # x=-20.3: 30.45-3=27.45 vs 26.97 (close)
    # x=-61.7: 92.55-3=89.55 vs 99.56 (off 10)
    # x=-24.3: 36.45-3=33.45 vs 33.98 (close)
    # x=-50.4: 75.6-3=72.6 vs 79.75 (off 7)
    # x=-6: 9-3=6 vs 1.91 (off 4)
    # Try y = -2.6x for x>0, y = -1.6x - 2 for x<0:
    # x=-20.3: 32.48-2=30.48 vs 26.97
    # x=-61.7: 98.72-2=96.72 vs 99.56
    # x=-24.3: 38.88-2=36.88 vs 33.98
    # x=-50.4: 80.64-2=78.64 vs 79.75
    # x=-6: 9.6-2=7.6 vs 1.91
    # Hmm, x=-6 is the outlier. Maybe there's a kink near 0.
    # Let's just do a piecewise linear fit: for x>=0, slope -2.6, intercept ~0.
    # For x<0, fit through (-20.3,26.97) and (-61.7,99.56): slope = (99.56-26.97)/(-61.7+20.3)
    #   = 72.59/-41.4 = -1.753; intercept = 26.97 + 1.753*(-20.3) = 26.97-35.59 = -8.62
    # Check x=-24.3: -1.753*-24.3 - 8.62 = 42.6-8.62 = 33.98 (exact!)
    # Check x=-50.4: -1.753*-50.4 - 8.62 = 88.35-8.62 = 79.73 vs 79.75 (close!)
    # Check x=-6: -1.753*-6 - 8.62 = 10.52-8.62 = 1.9 vs 1.91 (exact!)
    # Great! So for x<0: y = -1.753*x - 8.62.
    # For x>0: check x=88.2: -2.6*88.2 = -229.3 vs -228.97
    #   x=66: -171.6 vs -173.49
    #   x=72.7: -189.0 vs -190.23
    #   x=2.9: -7.54 vs -15.84
    #   x=21.3: -55.38 vs -61.81
    # Hmm, x=2.9 and 21.3 are off. Maybe slope is different.
    # Fit through (66,-173.49) and (88.2,-228.97): slope = -55.48/22.2 = -2.499
    #   intercept = -173.49 + 2.499*66 = -173.49+164.9 = -8.55
    # Check x=72.7: -2.499*72.7 - 8.55 = -181.7-8.55 = -190.2 vs -190.23 (exact!)
    # Check x=2.9: -2.499*2.9 - 8.55 = -7.25-8.55 = -15.8 vs -15.84 (exact!)
    # Check x=21.3: -2.499*21.3 - 8.55 = -53.2-8.55 = -61.77 vs -61.81 (exact!)
    # So for x>=0: y = -2.499*x - 8.55.
    # And for x<0: y = -1.753*x - 8.62.
    # Both intercepts ~ -8.6. Maybe it's a single function with a kink at 0.
    # Actually maybe f(x) = -2.5*x - 8.6 for x>0, and -1.75*x - 8.6 for x<0.
    # Let's use those.
    import math
    out = []
    for x in probe["x"]:
        try:
            if x >= 0:
                y = -2.499 * x - 8.55
            else:
                y = -1.753 * x - 8.62
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
