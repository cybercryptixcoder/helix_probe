def predict(probe):
    # f is piecewise smooth with a kink at x=0 [E2, E4].
    # For x >= 0: f(x) = 106.0528 + 111.42781*x  (exact, linear) [E2, E3, E5]
    # For x <= -10: f(x) = 235.2718 + 26.0717*(-10 - x)  (slope -26.0717) [E2, E4]
    # For -10 < x < 0: smooth valley with minimum near x=-1.05, value ~6.4 [E4, E6]
    #   E6 dense data shows a smooth rounded minimum (not a V-kink):
    #   x=-1.0:6.85, -1.1:6.44, -0.95:8.30, -1.2:7.47, -0.9:10.63, -1.3:9.06
    #   Minimum ~ x=-1.05, y~6.4. Left side rises slowly, right side steeply.
    #   Left of min: slope ~ -26 near x=-2 (matches left branch), steepening.
    #   Right of min: rises steeply toward f(0)=106.05.
    #   Fit a smooth curve. Use a quadratic-ish valley anchored at min (-1.05, 6.4).
    #   Right side: from (-1.05,6.4) to (0,106.05): steep, roughly quadratic.
    #   Left side: from (-10,235.27) down to min, then back up.
    #   Model the valley as: f = 6.4 + A*(x+1.05)^2 on the right, and
    #   blend to the left linear branch near x=-2.
    # Check right side with quadratic through (-1.05,6.4),(0,106.05) and slope at 0 ~111:
    #   f = 6.4 + a*(x+1.05)^2 ; at x=0: 6.4+a*1.1025=106.05 => a=90.4
    #   slope at 0 = 2a*1.05=189.8, too steep vs 111. Use asymmetric.
    # Simpler: fit quadratic through (-2,26.70),(-1.05,6.4),(0,106.05):
    #   c=106.05; a*4+b*(-2)=-79.35 => 2a-b=-39.675
    #   a*1.1025+b*(-1.05)=-99.65 => 1.05a-b=-94.90
    #   subtract: 0.95a=55.22 => a=58.13, b=2a+39.675=155.94
    #   Check -1.0: 58.13-155.94+106.05=8.24 vs 6.85 (ok-ish)
    #   Check -0.5: 14.53-77.97+106.05=42.6 vs 50.34 (ok-ish)
    #   Check -1.5: 130.8-233.9+106.05=2.95 vs 13.66 (low)
    # Better: use piecewise quadratic on each side of min.
    # Left of min (-2 to -1.05): from (-2,26.70) to (-1.05,6.4), slope ~ -26 at -2.
    #   quadratic: f(-2)=26.70, f(-1.05)=6.4, f'(-2)=-26.07
    #   f=a x^2+b x+c; f'=2ax+b; at -2: -4a+b=-26.07
    #   f(-2)=4a-2b+c=26.70; f(-1.05)=1.1025a-1.05b+c=6.4
    #   subtract: 2.8975a-0.95b=20.30 => b=(2.8975a-20.30)/0.95
    #   from -4a+b=-26.07: b=-26.07+4a
    #   -26.07+4a=(2.8975a-20.30)/0.95 => -24.77+3.8a=2.8975a-20.30 => 0.9025a=4.47 => a=4.95
    #   b=-26.07+19.8=-6.27; c=26.70-4*4.95+2*(-6.27)=26.70-19.8-12.54=-5.64
    #   Check -1.5: 4.95*2.25-6.27*(-1.5)-5.64=11.14+9.41-5.64=14.9 vs 13.66 (good)
    #   Check -1.2: 7.13+7.52-5.64=9.01 vs 7.47 (ok)
    # Right of min (-1.05 to 0): from (-1.05,6.4) to (0,106.05), slope at 0 ~111.
    #   f=a x^2+b x+c; c=106.05; b=111.43 (slope at 0)
    #   f(-1.05)=1.1025a-1.05*111.43+106.05=6.4 => 1.1025a-117.0+106.05=6.4 => 1.1025a=17.35 => a=15.74
    #   Check -0.5: 3.94-55.7+106.05=54.3 vs 50.34 (ok)
    #   Check -0.9: 12.75-100.3+106.05=18.5 vs 10.63 (high)
    #   Check -0.8: 10.07-89.1+106.05=27.0 vs 18.22 (high)
    #   Hmm right side steeper near min. Try slope at min ~0 and fit through (-1.05,6.4),(-0.5,50.34),(0,106.05):
    #   c=106.05; 0.25a-0.5b=-55.71 => 0.5a-b=-111.42
    #   1.1025a-1.05b=-99.65 => 1.05a-b=-94.90
    #   subtract: 0.55a=16.52 => a=30.04, b=0.5*30.04+111.42=126.44
    #   Check -0.9: 24.33-113.8+106.05=16.6 vs 10.63 (high)
    #   Check -0.8: 19.23-101.2+106.05=24.1 vs 18.22 (high)
    #   The valley is asymmetric and steep. Use quadratic through (-1.05,6.4),(-0.9,10.63),(-0.5,50.34):
    #   c: 1.1025a-1.05b=-99.65
    #   0.81a-0.9b=-95.42
    #   0.25a-0.5b=-55.71 => b=0.5a+111.42
    #   1.1025a-1.05*(0.5a+111.42)=-99.65 => 1.1025a-0.525a-117.0=-99.65 => 0.5775a=17.35 => a=30.04
    #   b=0.5*30.04+111.42=126.44 (same as above)
    #   Check -0.7: 14.72-88.5+106.05=32.3 vs 28.06 (ok)
    #   Check -0.6: 10.81-75.9+106.05=41.0 vs 39.20 (good)
    #   Check -0.4: 4.81-50.6+106.05=60.3 vs 61.48 (good)
    #   Check -0.3: 2.70-37.9+106.05=70.8 vs 72.62 (good)
    #   Check -0.2: 1.20-25.3+106.05=82.0 vs 83.77 (good)
    #   Good enough. Use this quadratic for -1.05<x<0.
    # For -10<x<=-2: linear slope -26.0717 from (-10,235.2718) [E4]
    #   f(-2)=26.6982 matches.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x >= 0:
                y = 106.0528 + 111.42781 * x
            elif x <= -10:
                y = 235.2718 + 26.0717 * (-10 - x)
            elif x <= -2:
                y = 26.6982 + 26.0717 * (-2 - x)
            elif x <= -1.05:
                # quadratic left of min: a=4.95, b=-6.27, c=-5.64
                y = 4.95*x*x - 6.27*x - 5.64
            else:
                # quadratic right of min: a=30.04, b=126.44, c=106.05
                y = 30.04*x*x + 126.44*x + 106.05
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
