import math

def predict(probe):
    # Beliefs (mechanism):
    # Central positive bump: peak 0.3868 at x=0, asymmetric.
    #   Left flank (x<0): generalized Gaussian, p=1.5, s=1.30 [E22,E16]
    #     -0.25=0.3592,-0.5=0.3052,-1=0.1972,-1.5=0.1052,-2=0.0575,-2.5=0.0221,-3=0.008
    #   Right flank (x>0): NOT a single generalized Gaussian. E24 shows a kink near x=3:
    #     the flank decays faster than p=1.5 predicts beyond ~2.5.
    #     Data [E22,E10,E24]: 0.25=0.3563,0.5=0.3225,1=0.255,1.5=0.1875,2=0.12,
    #       2.5=0.0642,2.6=0.055,2.7=0.0465,2.8=0.0397,2.9=0.0362,3=0.0327,
    #       3.5=0.0185,4=0.0099,4.5=0.0043?,5=0.0012,6~0.0005,8~0.0001
    #     Fit right flank as generalized Gaussian p=1.5, s=1.79 up to x~2.2,
    #     then steeper p=2.0-ish tail beyond. Use two-segment: for x<=2.2 use s=1.79,p=1.5;
    #     for x>2.2 use a Gaussian-like decay anchored at 2.2 (0.086) with sigma~0.95.
    #     Check: 2.5: 0.086*exp(-(0.3)^2/(2*0.95^2))=0.086*0.951=0.0818 (obs 0.0642) high
    #     Use sigma=0.75: 2.5: 0.086*exp(-0.09/1.125)=0.086*0.923=0.0794 still high.
    #     Better: fit log-linear from 2.5 to 4: ln(0.0642/0.0099)/1.5=1.24 -> decay rate.
    #     Use exponential tail beyond 2.2: y=0.086*exp(-k*(x-2.2)), k=1.24:
    #       2.5:0.086*exp(-0.372)=0.0593 (obs 0.0642) ok
    #       3:0.086*exp(-0.992)=0.0319 (obs 0.0327) ok
    #       3.5:0.086*exp(-1.612)=0.0171 (obs 0.0185) ok
    #       4:0.086*exp(-2.232)=0.0092 (obs 0.0099) ok
    #       5:0.086*exp(-3.472)=0.0027 (obs 0.0012) a bit high
    #     Good enough.
    # Negative dip near x=12: min -0.0061 at 12, asymmetric [E18,E12]
    #   10=-0.0043,11=-0.0054,12=-0.0061,13=-0.0055,14=-0.0049,15=-0.0043,16=-0.0037,
    #   18=-0.0025,22=-0.0004
    #   Left sigma~2.4, right sigma~3.5 Gaussian.
    # Positive shoulder near -3 to -6: linear ramp 0 at -6 to 0.008 at -3 [E14,E16]
    # Broad negative left tail: piecewise linear, -0.0044 at -128 rising to 0 at -6 [E20,E16]
    # Far-right baseline: -0.0004 for 20<x<60, rising to -0.0001 at 120 [E18,E19]

    xs = probe["x"]
    ys = []
    for x in xs:
        # central bump
        if x <= 0:
            y = 0.3868 * math.exp(-abs(x/1.30)**1.5)
        else:
            if x <= 2.2:
                y = 0.3868 * math.exp(-(x/1.79)**1.5)
            else:
                y = 0.086 * math.exp(-1.24*(x-2.2))

        # shoulder ramp near -3 (0 at -6, 0.008 at -3)
        if -6.0 < x < -3.0:
            y += 0.008 * (x + 6.0) / 3.0

        # negative dip near 12
        sd = 2.4 if x < 12.0 else 3.5
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*sd*sd))

        # broad negative left tail
        if x <= -128:
            tail = -0.0044
        elif x <= -60:
            tail = -0.0044 + (x+128)*(0.0012/68)
        elif x <= -40:
            tail = -0.0032 + (x+60)*(0.0002/20)
        elif x <= -20:
            tail = -0.0030 + (x+40)*(0.0018/20)
        elif x <= -6:
            tail = -0.0012 + (x+20)*(0.0012/14)
        else:
            tail = 0.0
        y += tail

        # far-right baseline
        if x > 20.0:
            if x < 60.0:
                y += -0.0004
            elif x < 120.0:
                y += -0.0004 + (x-60.0)*(0.0003/60.0)
            else:
                y += -0.0001

        ys.append(y)
    return {"y": ys}
