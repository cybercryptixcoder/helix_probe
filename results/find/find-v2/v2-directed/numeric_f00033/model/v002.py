def predict(probe):
    # f is a smooth, asymmetric bump centered at x=0 [E1, E2]
    # Peak ~0.387 at x=0 [E1, E2]
    # Right side: 0.255 at 1, 0.12 at 2, 0.0327 at 3, ~0 at 5-6 [E2]
    # Left side: 0.197 at -1, 0.0575 at -2, 0.008 at -3, ~0 at -6 [E2]
    # Left side is narrower than right side [E1, E2]
    # Small negative baseline far out on both sides (~-0.004 at -128) [E1]
    # Shape looks like a Gaussian-ish bump; fit widths separately per side
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                # right side: fit 0.387*exp(-(x/w)^2); at x=1 ->0.255 => w^2=1/ln(0.387/0.255)=2.63
                # check x=2: 0.387*exp(-4/2.63)=0.387*0.218=0.084 (obs 0.12) -> need wider
                # try w=2.0: x=1:0.387*0.779=0.301 (obs .255); w=1.9: x=1 .293
                # use w=1.85: x=1 .289, x=2 .121, x=3 .0275, x=5 .00026
                y = 0.387 * math.exp(-(x/1.85)**2)
            else:
                # left: at -1 ->0.197 => w^2=1/ln(.387/.197)=1.44 -> w=1.20
                # check -2: .387*exp(-4/1.44)=.387*.062=.024 (obs .0575) -> wider
                # w=1.45: -1: .387*exp(-1/2.10)=.387*.621=.240 (obs .197)
                # w=1.35: -1: .387*exp(-1/1.82)=.387*.577=.223
                # w=1.30: -1: .387*exp(-1/1.69)=.387*.554=.214
                # w=1.25: -1: .387*exp(-1/1.5625)=.387*.527=.204
                # w=1.22: -1: .387*exp(-1/1.488)=.387*.511=.198 ok
                # -2: .387*exp(-4/1.488)=.387*.068=.0263 (obs .0575) still low
                # The left side isn't Gaussian; it has a longer tail. Use a different form.
                # Try 0.387*exp(-(|x|/a)^p). At -1: .197 -> (1/a)^p = ln(.387/.197)=.676
                # at -2: .0575 -> (2/a)^p = ln(.387/.0575)=1.907
                # ratio: 2^p = 1.907/.676=2.82 -> p=1.50, a: (1/a)^1.5=.676 -> a=1.30
                # check -3: .387*exp(-(3/1.30)^1.5)=.387*exp(-3.51)=.0116 (obs .008) close
                # -4: .387*exp(-(4/1.3)^1.5)=.387*exp(-5.4)=.0017 (obs .0053) low
                # -5: .387*exp(-(5/1.3)^1.5)=.387*exp(-7.55)=.0002 (obs .0027) low
                # tail is heavier still. Add small negative/positive baseline? obs -6 is 0.
                # Use p=1.3, a=1.25: -1: .387*exp(-(0.8)^1.3)=.387*exp(-.748)=.183
                # -2: .387*exp(-(1.6)^1.3)=.387*exp(-1.85)=.0607 good
                # -3: .387*exp(-(2.4)^1.3)=.387*exp(-3.11)=.0172 (obs .008)
                # -4: .387*exp(-(3.2)^1.3)=.387*exp(-4.55)=.0041 (obs .0053) ok
                # -5: .387*exp(-(4)^1.3)=.387*exp(-6.06)=.0009 (obs .0027)
                # -6: .387*exp(-(4.8)^1.3)=.387*exp(-7.66)=.00018 (obs 0)
                a = 1.25
                p = 1.30
                y = 0.387 * math.exp(-((abs(x)/a)**p))
            # small negative baseline far out (both sides) [E1]
            if abs(x) > 20:
                y -= 0.004 * min(1.0, (abs(x)-20)/40.0)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
