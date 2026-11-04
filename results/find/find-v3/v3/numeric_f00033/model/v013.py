import math

def predict(probe):
    # Beliefs (mechanism, from all evidence):
    # Central positive bump: peak ~0.3868 at x=0, asymmetric.
    #   Left flank: -0.25=0.3592,-0.5=0.3052,-0.75=0.2512,-1=0.1972,-1.25=0.1467,
    #     -1.5=0.1052,-1.75=0.078,-2=0.0575,-2.5=0.0221,-3=0.008 [E22,E16]
    #   Right flank: 0.25=0.3563,0.5=0.3225,0.75=0.2888,1=0.255,1.25=0.2213,
    #     1.5=0.1875,1.75=0.1537,2=0.12,2.5=0.0642,3=0.0327,4=0.0099,5=0.0012 [E22,E10]
    #   Left flank is steeper than right. Fit asymmetric Gaussian:
    #     left: 0.3868*exp(-x^2/(2*s^2)); at x=-1: 0.1972 -> ratio .5098 -> s^2=1/(2*0.674)=0.742, s=0.861
    #       check -0.5: 0.3868*exp(-0.25/1.484)=0.3868*0.845=0.327 (obs 0.3052) a bit high
    #       check -2: 0.3868*exp(-4/1.484)=0.3868*0.0675=0.0261 (obs 0.0575) too low
    #     So left flank is not Gaussian; it's flatter far out. Use a generalized Gaussian
    #     exp(-|x/s|^p). Fit at -1 (ratio .5098) and -2 (ratio .1487):
    #       (1/s)^p*... : ln(.5098)=-0.674, ln(.1487)=-1.906. Ratio 1.906/0.674=2.83=2^p -> p=1.50
    #       then (1/s)^1.5=0.674 -> 1/s=0.769 -> s=1.30
    #       check -0.5: exp(-(0.5/1.30)^1.5)=exp(-0.238)=0.788 -> 0.305 (obs 0.3052) 
    #       check -1.5: exp(-(1.5/1.3)^1.5)=exp(-1.226)=0.293 -> 0.1134 (obs 0.1052) ok
    #       check -2.5: exp(-(2.5/1.3)^1.5)=exp(-2.63)=0.072 -> 0.0279 (obs 0.0221) ok
    #       check -3: exp(-(3/1.3)^1.5)=exp(-3.51)=0.0299 -> 0.0116 (obs 0.008) ok
    #     Right flank: fit at 1 (ratio .6593) and 2 (ratio .3102):
    #       ln(.6593)=-0.4165, ln(.3102)=-1.170. ratio 2.81=2^p -> p=1.49
    #       (1/s)^1.5=0.4165 -> 1/s=0.558 -> s=1.79
    #       check 0.5: exp(-(0.5/1.79)^1.5)=exp(-0.147)=0.863 -> 0.334 (obs 0.3225) ok
    #       check 1.5: exp(-(1.5/1.79)^1.5)=exp(-0.766)=0.465 -> 0.180 (obs 0.1875) ok
    #       check 2.5: exp(-(2.5/1.79)^1.5)=exp(-1.65)=0.192 -> 0.0743 (obs 0.0642) ok
    #       check 3: exp(-(3/1.79)^1.5)=exp(-2.17)=0.114 -> 0.0442 (obs 0.0327) a bit high
    #       check 4: exp(-(4/1.79)^1.5)=exp(-3.34)=0.0355 -> 0.0137 (obs 0.0099) ok
    #   Use generalized Gaussian with p=1.5, s_left=1.30, s_right=1.79, amp=0.3868.
    # Negative dip near x=12: min -0.0061 at 12, roughly symmetric, sigma~2.5 [E18,E12]
    #   10=-0.0043,11=-0.0054,12=-0.0061,13=-0.0055,14=-0.0049,15=-0.0043,16=-0.0037,
    #   18=-0.0025,22=-0.0004 [E18,E12]
    #   Fit Gaussian: at 10 (dx=-2): ratio .705 -> exp(-4/(2s^2))=.705 -> s^2=5.78, s=2.40
    #     at 16 (dx=4): exp(-16/11.56)=0.25 -> -0.00153 (obs -0.0037) too low
    #   Not Gaussian; flatter. Use generalized Gaussian: at dx=2 ratio .705, dx=4 ratio .607
    #     ln(.705)=-.349, ln(.607)=-.499. ratio 1.43=2^p -> p=0.516
    #     (2/s)^0.516=.349 -> 2/s=0.128 -> s=15.6 (very broad, p small)
    #     check dx=6 (x=18): exp(-(6/15.6)^0.516)=exp(-0.617)=0.539 -> -0.00329 (obs -0.0025) ok-ish
    #     check dx=10 (x=22): exp(-(10/15.6)^0.516)=exp(-0.80)=0.449 -> -0.00274 (obs -0.0004) too low
    #   The dip is asymmetric: sharp near 12, drops fast by 22. Use Gaussian with sigma~2.4 but
    #   the far points (18,22) are contaminated by the baseline. Actually 22=-0.0004 is baseline.
    #   So dip is roughly Gaussian sigma~2.4 but truncated; use Gaussian sigma=2.4.
    #   Recheck: 10: exp(-4/11.52)=.707 -> -0.00431 (obs -0.0043) 
    #     11: exp(-1/11.52)=.917 -> -0.00559 (obs -0.0054) ok
    #     13: same as 11 -> -0.00559 (obs -0.0055) ok
    #     14: exp(-4/11.52)=.707 -> -0.00431 (obs -0.0049) a bit low
    #     15: exp(-9/11.52)=.458 -> -0.00279 (obs -0.0043) too low
    #     16: exp(-16/11.52)=.249 -> -0.00152 (obs -0.0037) too low
    #   Right side is flatter. Use asymmetric: left sigma=2.4, right sigma=3.2:
    #     13: exp(-1/20.48)=.952 -> -0.00581 (obs -0.0055) ok
    #     14: exp(-4/20.48)=.823 -> -0.00502 (obs -0.0049) 
    #     15: exp(-9/20.48)=.644 -> -0.00393 (obs -0.0043) ok
    #     16: exp(-16/20.48)=.458 -> -0.00279 (obs -0.0037) a bit low
    #     18: exp(-36/20.48)=.172 -> -0.00105 (obs -0.0025) too low
    #   Right side even flatter. Use generalized Gaussian p=1.2 right, sigma=3.0:
    #     14: exp(-(2/3)^1.2)=exp(-0.617)=.539 -> -0.00329 (obs -0.0049) too low
    #   Hmm. Let me just use a piecewise/asymmetric Gaussian with sigma_right=3.5:
    #     14: exp(-4/24.5)=.849 -> -0.00518 (obs -0.0049) ok
    #     15: exp(-9/24.5)=.693 -> -0.00423 (obs -0.0043) 
    #     16: exp(-16/24.5)=.520 -> -0.00317 (obs -0.0037) ok
    #     18: exp(-36/24.5)=.230 -> -0.00140 (obs -0.0025) a bit low
    #   Good enough. Left sigma=2.4, right sigma=3.5.
    # Positive shoulder near -3 to -6: additive ramp, 0 at -6, 0.008 at -3 [E14,E16]
    #   E14: -5.8=0.0006,-5.6=0.0011,-5.4=0.0016,-5.2=0.0021,-5.0=0.0027,-4.8=0.0032,
    #     -4.6=0.0037,-4.4=0.0043,-4.2=0.0048,-4.0=0.0053,-3.8=0.0058,-3.6=0.0064,
    #     -3.4=0.0069,-3.2=0.0074,-3.0=0.008,-2.8=0.0089,-2.6=0.0177,-2.4=0.0264
    #   So ramp is linear from -6 (0) to -3 (0.008), then bump takes over.
    #   slope = 0.008/3 = 0.002667 per unit. Check -5: 0.00267 (obs 0.0027) 
    #   Check -4: 0.00533 (obs 0.0053) 
    # Broad negative left tail: smooth ramp, ~-0.0044 at -128 rising toward 0 [E2,E9,E15,E16,E20]
    #   E20: -128=-0.0044,-124=-0.0044,-120=-0.0043,-116=-0.0042,-112=-0.0041,-108=-0.0041,
    #     -104=-0.004,-100=-0.0039,-96=-0.0038,-92=-0.0038,-88=-0.0037,-84=-0.0036,
    #     -80=-0.0035,-76=-0.0035,-72=-0.0034,-68=-0.0033,-64=-0.0033,-60=-0.0032,
    #     -50=-0.0032,-40=-0.0030
    #   E16: -20=-0.0012,-16=-0.0009,-14=-0.0007,-12=-0.0005,-10=-0.0004,-9=-0.0003,
    #     -8=-0.0002,-7.5=-0.0001,-7=-0.0001,-6.5=-0.0,-6=0.0
    #   So it's a smooth ramp: roughly linear in x from -128 to -60, then steeper toward 0.
    #   -128=-0.0044, -60=-0.0032: slope 1.76e-5
    #   -60=-0.0032, -40=-0.0030: slope 1e-5
    #   -40=-0.0030, -20=-0.0012: slope 9e-5
    #   -20=-0.0012, -6=0: slope 8.6e-5
    #   Use piecewise linear through knots.
    # Far-right baseline: ~-0.0004 for x in 20..56, rising to ~-0.0001 at 120+ [E18,E19]
    #   -0.0004@22..56, -0.0003@72, -0.0002@96, -0.0001@120 [E18]
    #   Also -0.0001@128 [E19], -0.0001@115 [E19]
    #   Model: -0.0004 for 20<x<60, then rising linearly to -0.0001 at 120.

    xs = probe["x"]
    ys = []
    for x in xs:
        # central asymmetric generalized Gaussian bump (p=1.5)
        if x < 0:
            s = 1.30
        else:
            s = 1.79
        y = 0.3868 * math.exp(-abs(x/s)**1.5)

        # additive shoulder ramp near -3 (0 at -6, 0.008 at -3)
        if -6.0 < x < -3.0:
            y += 0.008 * (x + 6.0) / 3.0

        # negative dip near 12 (asymmetric Gaussian)
        if x < 12.0:
            sd = 2.4
        else:
            sd = 3.5
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*sd*sd))

        # broad negative left tail: piecewise linear through knots
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

        # far-right small negative baseline, rising toward 0
        if x > 20.0:
            if x < 60.0:
                y += -0.0004
            elif x < 120.0:
                y += -0.0004 + (x-60.0)*(0.0003/60.0)
            else:
                y += -0.0001

        ys.append(y)
    return {"y": ys}
