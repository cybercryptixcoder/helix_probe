def predict(probe):
    # f(x) looks like a polynomial-ish growth: |y| grows fast with |x| [E1,E2,E3]
    # Sign of y matches sign of x (negative x -> negative y, positive x -> positive y) [E1,E2,E3]
    # Try y = x^3 * something? Check ratios.
    # E1: x=88.2 -> y=-7.47e7 ; x^3=6.86e5 ; y/x^3 ~ -108.9
    #     x=66.0 -> -2.36e7 ; x^3=2.87e5 ; ratio ~ -82.3
    #     x=72.7 -> -3.47e7 ; x^3=3.84e5 ; ratio ~ -90.3
    #     x=21.3 -> -2.76e5 ; x^3=9663 ; ratio ~ -28.5
    #     x=2.9 -> -191.9 ; x^3=24.4 ; ratio ~ -7.87
    #     x=-6.0 -> -876.9 ; x^3=-216 ; ratio ~ 4.06 (sign flip!)
    # Hmm sign: x=-6 gives y=-876.9 (negative), x^3=-216, ratio positive.
    # x=-20.3 -> -178293 ; x^3=-8365 ; ratio ~ 21.3
    # x=-24.3 -> -374808 ; x^3=-14349 ; ratio ~ 26.1
    # x=-50.4 -> -7.36e6 ; x^3=-1.28e5 ; ratio ~ 57.5
    # x=-61.7 -> -1.67e7 ; x^3=-2.35e5 ; ratio ~ 71.0
    # So ratio grows with |x|. Maybe y = x^3 * (a + b*x)? or x^4-ish?
    # Try y = x^3 * x = x^4? x=88.2: x^4=6.05e7, y=-7.47e7 -> ratio -1.23
    # x=66: x^4=1.90e7, y=-2.36e7 -> -1.24
    # x=72.7: x^4=2.79e7, y=-3.47e7 -> -1.24
    # x=21.3: x^4=2.06e5, y=-2.76e5 -> -1.34
    # x=2.9: x^4=70.7, y=-191.9 -> -2.71
    # x=-6: x^4=1296, y=-876.9 -> -0.68
    # Not constant.
    # Try y = x^5? x=88.2: x^5=5.34e9, no.
    # Try y = x^3*(x+c)? Let's fit: y/x^3 = a + b*x.
    # x=88.2: -108.9 = a + 88.2b
    # x=66: -82.3 = a + 66b
    # diff: -26.6 = 22.2b -> b=-1.198, a = -82.3+66*1.198 = -82.3+79.1=-3.2
    # Check x=72.7: a+b*72.7 = -3.2-87.1=-90.3 ✓
    # Check x=21.3: -3.2-25.5=-28.7 vs -28.5 ✓
    # Check x=2.9: -3.2-3.47=-6.67 vs -7.87 close-ish
    # Check x=-6: -3.2+7.19=3.99 vs 4.06 ✓
    # Check x=-20.3: -3.2+24.3=21.1 vs 21.3 ✓
    # Check x=-50.4: -3.2+60.4=57.2 vs 57.5 ✓
    # So y ≈ x^3 * (b*x + a) with b≈-1.2, a≈-3.2. That's y = -1.2 x^4 - 3.2 x^3.
    # Check E2: x=104.5: x^4=1.192e8, x^3=1.141e6
    #   y = -1.2*1.192e8 - 3.2*1.141e6 = -1.430e8 - 3.65e6 = -1.467e8 vs -1.465e8 ✓✓
    # x=1.2: x^4=2.074, x^3=1.728; y=-2.49-5.53=-8.02 vs -45.1. Off.
    # x=65.5: x^4=1.842e7,x^3=2.812e5; y=-2.21e7-9.0e5=-2.30e7 vs -2.29e7 ✓
    # x=30.3: x^4=8.43e5,x^3=2.78e4; y=-1.01e6-8.9e4=-1.10e6 vs -1.094e6 ✓
    # x=-63.9: x^4=1.667e7,x^3=-2.609e5; y=-2.00e7+8.35e5=-1.917e7 vs -1.922e7 ✓
    # x=104.9: x^4=1.211e8,x^3=1.154e6; y=-1.453e8-3.69e6=-1.490e8 vs -1.488e8 ✓
    # x=123.6: x^4=2.334e8,x^3=1.888e6; y=-2.801e8-6.04e6=-2.861e8 vs -2.857e8 ✓
    # x=79.4: x^4=3.976e7,x^3=5.006e5; y=-4.771e7-1.602e6=-4.931e7 vs -4.919e7 ✓
    # x=103.0: x^4=1.126e8,x^3=1.093e6; y=-1.351e8-3.50e6=-1.386e8 vs -1.383e8 ✓
    # E3: x=-48.6: x^4=5.58e6,x^3=-1.148e5; y=-6.70e6+3.67e5=-6.33e6 vs -6.35e6 ✓
    # x=58.8: x^4=1.196e7,x^3=2.033e5; y=-1.435e7-6.51e5=-1.50e7 vs -1.495e7 ✓
    # x=102.1: x^4=1.086e8,x^3=1.064e6; y=-1.303e8-3.40e6=-1.337e8 vs -1.336e8 ✓
    # x=47.1: x^4=4.92e6,x^3=1.045e5; y=-5.90e6-3.34e5=-6.24e6 vs -6.22e6 ✓
    # x=-7.1: x^4=2541,x^3=-358; y=-3049+1145=-1904 vs -1930 ✓
    # x=-102.2: x^4=1.091e8,x^3=-1.067e6; y=-1.309e8+3.42e6=-1.275e8 vs -2.497e7 ✗✗✗
    # x=-16.9: x^4=81573,x^3=-4827; y=-97888+15446=-82442 vs -83135 ✓
    # x=28.4: x^4=6.51e5,x^3=2.29e4; y=-7.81e5-7.33e4=-8.54e5 vs -8.49e5 ✓
    # x=105.7: x^4=1.248e8,x^3=1.181e6; y=-1.498e8-3.78e6=-1.536e8 vs -1.533e8 ✓
    # x=119.5: x^4=2.039e8,x^3=1.706e6; y=-2.447e8-5.46e6=-2.502e8 vs -2.498e8 ✓
    # So x=-102.2 is an outlier: y=-2.497e7 instead of -1.275e8.
    # -2.497e7 / x^4 = -2.497e7/1.091e8 = -0.229. Hmm.
    # Maybe there's a region where behavior differs. x=-102.2 is the only failure.
    # Check E1 x=-61.7: predicted -1.2*1.449e7-3.2*(-2.348e5)=-1.739e7+7.51e5=-1.664e7 vs -1.668e7 ✓
    # So only x=-102.2 fails. Could be a special region for x < -100? or x in some range.
    # -102.2 gives y=-2.497e7. What formula? -2.497e7/102.2^3 = -2.497e7/1.067e6 = -23.4
    # Hmm. Or maybe it's a different branch. Let's just note it as uncertain.
    # Actually maybe the region is x < -100 or so. We only have one data point there.
    # Let's use the main formula and add a note.
    x = probe["x"]
    out = []
    for v in x:
        try:
            y = -1.2 * v**4 - 3.2 * v**3
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
