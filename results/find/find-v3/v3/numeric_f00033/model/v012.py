import math

def predict(probe):
    # Beliefs (mechanism, from all evidence):
    # Central positive bump: peak ~0.387 at x=0, asymmetric.
    #   Left flank: -0.5=0.3052, -1=0.1972, -1.5=0.105, -2=0.0575, -2.5=0.0221 [E16,E6,E8]
    #   Right flank: 1.5=0.1875, 2=0.12, 2.5=0.0642, 3=0.0327, 3.5=0.0185, 4=0.0099,
    #     4.5=0.0029, 5=0.0012, 5.5=0.0006, 6=0.0001 [E6,E10]
    #   Fit asymmetric Gaussian: sigma_left~0.72, sigma_right~0.95 [E16,E10]
    # Positive shoulder near -3 to -6: additive ramp, 0 at -6, 0.008 at -3, then merges [E14,E16]
    #   E14: -5.8=0.0006,-5.6=0.0011,...-3.2=0.0074,-3.0=0.008,-2.8=0.0089,-2.6=0.0177,-2.4=0.0264
    #   So ramp is linear from -6 (0) to -3 (0.008), then bump takes over.
    # Negative dip near x=12: min -0.0061 at 12, roughly symmetric, sigma~2.5 [E18,E12]
    #   10=-0.0043,11=-0.0054,12=-0.0061,13=-0.0055,14=-0.0049,15=-0.0043,16=-0.0037,
    #   18=-0.0025,22=-0.0004 [E18,E12]
    # Broad negative left tail: plateau ~-0.0044 at -128, rising to 0 near 0 [E2,E9,E15,E16,E20]
    #   E20: -128=-0.0044,-100=-0.0039,-80=-0.0035,-60=-0.0032,-50=-0.0032,-40=-0.0030
    #   -28=-0.0019,-20=-0.0012,-12=-0.0005 [E2,E16]
    #   So it's a smooth ramp, not a flat plateau: roughly linear in x from -128 to -40,
    #   then rising faster toward 0. Model as sigmoid-ish tail.
    # Far-right baseline: ~-0.0004 for x in 20..56, rising to ~-0.0001 at 120+ [E18,E19]
    #   -0.0004@22..56, -0.0003@72, -0.0002@96, -0.0001@120 [E18]

    xs = probe["x"]
    ys = []
    for x in xs:
        # central asymmetric Gaussian bump
        sig = 0.72 if x < 0 else 0.95
        y = 0.387 * math.exp(-(x*x) / (2*sig*sig))

        # additive shoulder ramp near -3 (0 at -6, 0.008 at -3)
        if -6.0 < x < -3.0:
            y += 0.008 * (x + 6.0) / 3.0

        # negative dip near 12
        y += -0.0061 * math.exp(-((x-12.0)**2) / (2*2.5*2.5))

        # broad negative left tail: smooth ramp, ~-0.0044 at -128 rising toward 0
        # Use a sigmoid centered so that value at -128 ~ -0.0044 and at -40 ~ -0.0030.
        # A logistic: -A / (1 + exp((x - c)/s)). At x=-128: -A/(1+exp((-128-c)/s)) ~ -0.0044
        # At x=-40: ~-0.0030, at x=-20: ~-0.0012, at x=0: ~0.
        # Try A=0.0044, c=-30, s=18: at -128: -0.0044/(1+exp(-98/18))=-0.0044*(1/(1+0.0043))~-0.00438 ok
        #   at -40: -0.0044/(1+exp(-10/18))=-0.0044/(1+0.574)=-0.00280 (want -0.0030, close)
        #   at -20: -0.0044/(1+exp(10/18))=-0.0044/(1+1.74)=-0.00161 (want -0.0012, a bit high)
        # Try c=-25, s=15: at -128: -0.0044/(1+exp(-103/15))~-0.0044
        #   at -40: -0.0044/(1+exp(-15/15))=-0.0044/1.368=-0.00322 (want -0.0030)
        #   at -20: -0.0044/(1+exp(5/15))=-0.0044/1.396=-0.00315 (want -0.0012) too high
        # The tail is steeper near 0. Use two-piece: linear-ish far, steeper near 0.
        # Simpler: -0.0044 * exp(-((x+128)/something))? No, it's not exponential.
        # Fit: values (-128,-0.0044),(-80,-0.0035),(-40,-0.0030),(-20,-0.0012),(-12,-0.0005),(0,0)
        # This looks like a Gaussian tail: -0.0044*exp(-((x+128)^2)/(2*sigma^2))? 
        # At -80: -0.0044*exp(-(48^2)/(2s^2))=-0.0035 -> exp(-1152/s^2)=0.795 -> s^2=1152/0.229=5030, s=71
        # At -40: -0.0044*exp(-(88^2)/(2*5030))=-0.0044*exp(-0.77)=-0.00204 (want -0.0030) no.
        # Try linear from -128 to -40: slope=(-0.0030+0.0044)/88=1.59e-5
        #   at -80: -0.0044+48*1.59e-5=-0.00364 (want -0.0035) ok
        #   at -60: -0.0044+68*1.59e-5=-0.00332 (want -0.0032) ok
        #   at -50: -0.0044+78*1.59e-5=-0.00316 (want -0.0032) ok
        # Then from -40 to 0 steeper. At -40=-0.0030, -20=-0.0012, -12=-0.0005, 0=0.
        # Use a smooth blend: tail = -0.0044 * sigmoid-like. 
        # Let's use: tail = -0.0044 * exp(-((x+128)/L)^p) won't work well.
        # Use piecewise linear with smoothing via max/min is ugly. Use a logistic with variable:
        # tail = -0.0044 / (1 + exp((x - c)/s)) with c=-45, s=22:
        #   at -128: -0.0044/(1+exp(-83/22))=-0.0044/(1+0.023)=-0.00430 (want -0.0044) ok-ish
        #   at -80: -0.0044/(1+exp(-35/22))=-0.0044/(1+0.204)=-0.00365 (want -0.0035) ok
        #   at -40: -0.0044/(1+exp(5/22))=-0.0044/1.255=-0.00351 (want -0.0030) too high
        # Hmm. The data is closer to linear far out then steepening. 
        # Let's just use a Gaussian centered far left: tail = -0.0044 * exp(-((x+128)^2)/(2*sigma^2))
        # with sigma chosen so at -20 it's -0.0012: exp(-(108^2)/(2s^2))=0.273 -> 11664/(2s^2)=1.30 -> s^2=4486, s=67
        #   at -80: -0.0044*exp(-(48^2)/8972)=-0.0044*exp(-0.257)=-0.00340 (want -0.0035) ok
        #   at -40: -0.0044*exp(-(88^2)/8972)=-0.0044*exp(-0.863)=-0.00186 (want -0.0030) too low
        # The shape is not Gaussian. It's more like linear then steeper. 
        # Use a softplus/linear blend: tail = -0.0044 + slope*(x+128) for x<-40, then steeper.
        # Simplest robust: piecewise linear interpolated smoothly.
        # Use: tail = -0.0044 * (1 - smoothstep) where smoothstep goes 0 at -128 to 1 at 0.
        # Actually let me just use a two-segment linear with a smooth join via a logistic gate.
        # Segment A (far): linear from (-128,-0.0044) to (-40,-0.0030): slope=1.59e-5
        # Segment B (near): from (-40,-0.0030) to (0,0): roughly -0.0030*(1 - (x+40)/40)? at -20: -0.0015 (want -0.0012)
        #   at -12: -0.0009 (want -0.0005). Steeper near 0. Use quadratic: -0.0030*((x+40)/40)^2? at -20: -0.00075 no.
        # Use -0.0030*((x+40)/40)^1.5? at -20: -0.0030*0.354=-0.00106 (want -0.0012) ok
        #   at -12: -0.0030*(28/40)^1.5=-0.0030*0.586=-0.00176 no, want -0.0005.
        # Hmm -12 is -0.0005, that's very close to 0. So it drops fast between -20 and -12.
        # -20=-0.0012, -12=-0.0005, 0=0. That's roughly linear from -20 to 0: slope=6e-5.
        #   at -12: -0.0012+8*6e-5=-0.00072 (want -0.0005) ok-ish
        # So: far linear (-128 to -40), then steeper linear (-40 to -20), then steep (-20 to 0).
        # Let me just use a smooth function: tail = -0.0044 * exp(-((x+128)/100)^1.5 * something)
        # I'll use a logistic with c=-35, s=13:
        #   at -128: -0.0044/(1+exp(-93/13))=-0.0044/(1+0.0008)=-0.00440 ok
        #   at -80: -0.0044/(1+exp(-45/13))=-0.0044/(1+0.031)=-0.00427 (want -0.0035) too high
        # The far tail is NOT flat, it rises. So logistic centered at -35 with s=13 gives too flat far tail.
        # The data: -128=-0.0044, -80=-0.0035. That's a rise of 0.0009 over 48 units.
        # -80 to -40: -0.0035 to -0.0030, rise 0.0005 over 40.
        # -40 to -20: -0.0030 to -0.0012, rise 0.0018 over 20.
        # -20 to 0: -0.0012 to 0, rise 0.0012 over 20.
        # So it's roughly linear far, steepening near 0. 
        # Use: tail = -0.0044 * (1 - t)^2 where t = (x+128)/128 (t from 0 to 1).
        #   at -128: t=0, tail=-0.0044 ok
        #   at -80: t=0.375, tail=-0.0044*0.625^2=-0.00172 (want -0.0035) no.
        # Use tail = -0.0044 * (1 - t^2)? at -80: t=0.375, 1-0.14=0.86, -0.00378 (want -0.0035) ok
        #   at -40: t=0.6875, 1-0.473=0.527, -0.00232 (want -0.0030) too low
        # Use tail = -0.0044 * (1 - t^3)? at -80: 1-0.0527=0.947, -0.00417 (want -0.0035) too high
        # Use tail = -0.0044 * (1 - t)^0.5? at -80: 0.625^0.5=0.79, -0.00348 (want -0.0035) ok!
        #   at -40: 0.3125^0.5=0.559, -0.00246 (want -0.0030) too low
        # Hmm. Let me try tail = -0.0044 * (1 - t^1.5)? at -80: t=0.375, t^1.5=0.229, 1-0.229=0.771, -0.00339 (want -0.0035) ok
        #   at -40: t=0.6875, t^1.5=0.570, 1-0.570=0.430, -0.00189 (want -0.0030) too low
        # The problem is the far tail is flatter than any simple power. Let me just do piecewise linear.
        # Piecewise linear through the data points, with linear interpolation:
        # knots: (-128,-0.0044),(-80,-0.0035),(-40,-0.0030),(-20,-0.0012),(0,0)
        # This is a clean mechanism: a piecewise-linear tail. That's fine.
        if x <= -128:
            tail = -0.0044
        elif x <= -80:
            tail = -0.0044 + (x+128)*(0.0009/48)
        elif x <= -40:
            tail = -0.0035 + (x+80)*(0.0005/40)
        elif x <= -20:
            tail = -0.0030 + (x+40)*(0.0018/20)
        elif x <= 0:
            tail = -0.0012 + (x+20)*(0.0012/20)
        else:
            tail = 0.0
        y += tail

        # far-right small negative baseline, rising toward 0
        if x > 20.0:
            y += -0.0004 * math.exp(-(x-20.0)/80.0)

        ys.append(y)
    return {"y": ys}
