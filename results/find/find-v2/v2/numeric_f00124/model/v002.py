def predict(probe):
    # f is piecewise linear in x [E2]:
    #   For x <= 0: slope = (235.2718-106.0528)/(-10-0) = -12.9219 per unit
    #               f(0)=106.0528, so f(x)=106.0528 - 12.9219*x  (x<=0)
    #   For x >= 0: slope = (1220.3309-106.0528)/10 = 111.42781 per unit
    #               f(x)=106.0528 + 111.42781*x  (x>=0)
    # Check E1: f(88.2)=106.0528+111.42781*88.2=9933.99 ✓
    #           f(-61.7)=106.0528+12.9219*61.7=1583.18 ✓
    #           f(-6)=106.0528+12.9219*6=183.58? observed 130.985 -- slight mismatch,
    #           but overall piecewise-linear with kink at 0 fits well.
    # Refine: use two-line fit from E2 grid.
    # Left line through (-120,3103.1582) and (0,106.0528): slope=-24.9759? 
    #   (3103.1582-106.0528)/(-120) = -24.9759. But (-10,235.27): (235.27-106.05)/(-10)=-12.92.
    #   Not a single line on the left! Check (-40,1017.42): (1017.42-106.05)/(-40)=-22.78.
    #   (-20,495.99): -19.50. (-30,756.71): -21.69. (-60,1538.86): -23.88. (-80,2060.29):-24.43.
    #   (-100,2581.72):-24.76. (-120,3103.16):-24.98.
    #   So left side is NOT linear; it's curved. Looks like it approaches slope -25 far left.
    # Right side: (10,1220.33):slope 111.43; (20,2334.61):111.43; (120,13477.39):111.43.
    #   Right side is perfectly linear with slope 111.42781.
    # Left side: differences: -120->-100: -521.43 (per 20 => -26.07/unit)
    #   -100->-80: -521.43; -80->-60: -521.43; -60->-40: -521.43; -40->-30: -260.72;
    #   -30->-20: -260.72; -20->-10: -260.72; -10->0: -129.22.
    #   So slope changes: -26.07 (x<=-40), -26.07? wait -40->-30 is -260.72/10=-26.07.
    #   Actually all left differences are -26.07 per unit except -10->0 which is -12.92.
    #   Hmm: -20->-10: -260.72/10 = -26.07. -10->0: -129.22/10=-12.92.
    #   So left is linear slope -26.07 except last segment near 0.
    #   Let me recompute: 235.2718-106.0528=129.219 over 10 => 12.92. 
    #   But -20->-10: 495.9887-235.2718=260.7169 over 10 => 26.07.
    #   So there's a kink at x=-10 too? Or rounding. Actually maybe left slope is -26.07
    #   and the -10->0 segment is different. Let's check -10 value: 106.0528+26.07*10=366.75,
    #   but observed 235.27. So no.
    #   Alternative: left is quadratic-ish. Fit: f(x)=a*x^2+b*x+c for x<=0.
    #   Using (0,106.0528),(-10,235.2718),(-120,3103.1582):
    #   c=106.0528
    #   100a-10b=129.219 => 10a-b=12.9219
    #   14400a-120b=2997.1054 => 120a-b=24.9759
    #   subtract: 110a=12.054 => a=0.10958, b=10a-12.9219=1.0958-12.9219=-11.826
    #   Check (-20): 0.10958*400 -11.826*(-20)+106.05=43.83+236.52+106.05=386.4 vs 495.99. No.
    #   Try quadratic through (-120,3103.16),(-60,1538.86),(0,106.05):
    #   c=106.05
    #   3600a-60b=1432.81 => 60a-b=23.88
    #   14400a-120b=2997.11 => 120a-b=24.976
    #   subtract: 60a=1.096 => a=0.01827, b=60a-23.88=1.096-23.88=-22.78
    #   Check (-20): 0.01827*400+22.78*20+106.05=7.31+455.6+106.05=568.96 vs 495.99. Close-ish.
    #   Check (-10): 0.01827*100+227.8+106.05=1.83+227.8+106.05=335.68 vs 235.27. Off.
    #   The left side seems to have slope -26.07 mostly, then bends near 0.
    #   Actually maybe it's a smooth curve (MLP approximating). 
    #   Simplest robust model: piecewise linear with kink at 0, but left slope varies.
    #   Given MLP, left side is likely a smooth transition. Let me just use:
    #   right (x>=0): 106.0528 + 111.42781*x  (exact)
    #   left (x<0): interpolate. The data: 
    #     x: 0,-10,-20,-30,-40,-60,-80,-100,-120
    #     y: 106.05,235.27,495.99,756.71,1017.42,1538.86,2060.29,2581.72,3103.16
    #   Differences per 10: 129.22,260.72,260.72,260.72,260.72(x2),260.72(x2),260.72(x2)
    #   Wait -40->-60 is 20 units, diff 521.43 => 26.07/unit. -60->-80 same.
    #   So from -10 to -120 slope is -26.07/unit, and -10->0 slope is -12.92/unit.
    #   That's odd. Unless there's a kink at -10.
    #   Check: f(-10)=235.27. If slope -26.07 from -10 leftward: f(-20)=235.27+260.72=495.99 ✓
    #   f(0) would be 235.27-260.72=-25.45, but observed 106.05. So kink between -10 and 0.
    #   Maybe the kink is at x=-5? Or the MLP has a smooth bend.
    #   I'll model left as: slope -26.07 for x<=-10, and linear from (-10,235.27) to (0,106.05)
    #   for -10<x<0. That's a piecewise linear with two kinks (at -10 and 0).
    #   Actually simpler: the whole thing could be a smooth MLP. But piecewise linear fits well.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x >= 0:
                y = 106.0528 + 111.42781 * x
            elif x <= -10:
                y = 235.2718 + 26.0717 * (-10 - x)  # slope -26.07 going left
            else:
                # -10 < x < 0: linear from (-10,235.2718) to (0,106.0528)
                y = 235.2718 + (106.0528 - 235.2718) * (x + 10) / 10.0
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
