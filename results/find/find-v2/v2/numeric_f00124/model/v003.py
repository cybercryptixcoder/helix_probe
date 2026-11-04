def predict(probe):
    # f is piecewise linear with a kink at x=0 [E2, E4].
    # For x >= 0: f(x) = 106.0528 + 111.42781*x  (exact, linear) [E2, E3]
    # For x <= -10: f(x) = 235.2718 + 26.0717*(-10 - x)  (slope -26.0717) [E2, E4]
    # For -10 < x < 0: NOT linear from (-10,235.27) to (0,106.05).
    #   E4 shows a smooth curve: f(-5)=104.91, f(-3)=52.77, f(-1)=6.85,
    #   f(-0.5)=50.34, f(-0.1)=94.91, f(-2)=26.70, f(-7.5)=170.09, f(-9)=209.20.
    #   Note f(0)=106.05 and f(-0.1)=94.91, f(-0.5)=50.34: rises steeply near 0.
    #   Looks like a smooth (quadratic-ish) dip between -10 and 0, minimum near x=-1.
    #   Fit quadratic through (-10,235.2718),(-1,6.8494),(0,106.0528):
    #     c=106.0528
    #     100a-10b=129.219 => 10a-b=12.9219
    #     a-b=6.8494-106.0528=-99.2034
    #     subtract: 9a=112.1253 => a=12.4584, b=a+99.2034=111.6618
    #   Check (-5): 12.4584*25 -111.6618*5 +106.0528 = 311.46-558.31+106.05=-140.8. No.
    #   Try quadratic through (-10,235.27),(-5,104.91),(0,106.05):
    #     c=106.05
    #     25a-5b=-1.14 => 5a-b=-0.228
    #     100a-10b=129.22 => 10a-b=12.922
    #     subtract: 5a=13.15 => a=2.630, b=5a+0.228=13.378
    #   Check (-1): 2.630-13.378+106.05=95.30 vs 6.85. No.
    #   The dip is sharp near x=-1. Maybe it's |x|-like or a V-shape.
    #   Values: x=-10:235.27, -9:209.20, -7.5:170.09, -5:104.91, -3:52.77,
    #           -2:26.70, -1:6.85, -0.5:50.34, -0.1:94.91, 0:106.05
    #   From -10 to -1: roughly linear slope ~ -25.4/unit (235.27-6.85)/9=25.38.
    #   From -1 to 0: rises from 6.85 to 106.05, slope ~99/unit.
    #   So there's a sharp V (minimum) near x=-1! Kink at x=-1.
    #   Check -0.5: 6.85+99*0.5=56.35 vs 50.34. -0.1: 6.85+9.9=16.75 vs 94.91. No.
    #   Hmm -0.1 is 94.91, close to 106. So near 0 it's steep.
    #   Let's reconsider: maybe minimum is between -1 and 0.
    #   -1:6.85, -0.5:50.34, -0.1:94.91, 0:106.05. Differences: 43.49/0.5=87,
    #   44.57/0.4=111, 11.14/0.1=111. So slope ~111 near 0 (matches right slope!).
    #   Left of -1: -2:26.70, -1:6.85 => slope 19.85/unit. -3:52.77,-2:26.70 => 26.07.
    #   -5:104.91,-3:52.77 => 26.07/unit. -7.5:170.09,-5:104.91 => 26.07/unit.
    #   -9:209.20,-7.5:170.09 => 26.07/unit. -10:235.27,-9:209.20 => 26.07/unit.
    #   So slope -26.07 down to about x=-2, then bends up.
    #   -2:26.70, -1:6.85: slope 19.85 (bending).
    #   Minimum near x=-1 (value 6.85). Then rises with slope ~111 (same as right branch).
    #   So model: for x in [-1,0]: f = 6.85 + 111.42781*(x+1)? Check -0.5: 6.85+55.7=62.6 vs 50.34. No.
    #   Check -0.1: 6.85+100.3=107.1 vs 94.91. Close-ish.
    #   Actually maybe minimum is at x=-1 with value ~6.85, and right of it slope ~99.
    #   Given noise/MLP, use: left branch slope -26.0717 for x<=-2, then a smooth
    #   quadratic from -2 to 0 through (-2,26.70),(-1,6.85),(0,106.05).
    #   Fit: c=106.05; a-b=-99.20; 4a-2b=-79.35 => 2a-b=-39.675
    #   subtract: a=-59.53, b=a+99.20=39.67
    #   Check -0.5: -59.53*0.25+39.67*(-0.5)+106.05=-14.88-19.84+106.05=71.3 vs 50.34.
    #   Not great but reasonable. Use this quadratic for -2<x<0.
    # Simpler robust: piecewise linear with kink at -2 and -1:
    #   x<=-2: 26.0717 slope (f(-2)=26.70)
    #   -2<x<-1: from (26.70) to (6.85)
    #   -1<=x<0: from (6.85) to (106.05)  [slope 99.2]
    # Check -0.5: 6.85+99.2*0.5=56.45 vs 50.34 (ok). -0.1: 6.85+9.92=16.77 vs 94.91 (bad).
    # The -0.1 value 94.91 is odd. Maybe near 0 it accelerates. 
    # Given uncertainty, use quadratic through (-2,26.70),(-1,6.85),(0,106.05) for -2<x<0.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x >= 0:
                y = 106.0528 + 111.42781 * x
            elif x <= -2:
                y = 26.6982 + 26.0717 * (-2 - x)
            else:
                # -2 < x < 0: quadratic through (-2,26.6982),(-1,6.8494),(0,106.0528)
                a = -59.53
                b = 39.67
                c = 106.0528
                y = a*x*x + b*x + c
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
