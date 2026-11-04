def predict(probe):
    # f(x) is a smooth function, not a hard floor + quadratic.
    # Evidence: f(2.9)=-22.8021, f(-6.0)=-22.8021, f(1.2)=-22.8021
    #   -> flat minimum ~ -22.8 near x=0 (a well/bowl bottom).
    # Large |x|: f grows ~ 3.5*x^2 but slightly sub-quadratic.
    #   f(123.6)=47994.4 -> 47994/123.6^2=3.14
    #   f(104.9)=36952.1 -> 3.36; f(104.5)=36715.9 -> 3.36
    #   f(88.2)=27090.8 -> 3.48; f(66)=15014 -> 3.45
    #   f(30.3)=3107.5 -> 3.38; f(21.3)=1532.7 -> 3.38
    #   f(20.3)=1545.2 -> 3.75 (noisy)
    # So a*x^2 + c with a~3.4, c~-22.8 fits large |x| well; the ratio
    # drifts, suggesting a mild quartic or |x| term. Use a*x^2 + b*x^4 + c.
    # Fit: at x=123.6: a*15277+b*2.33e8+c=47994
    #      at x=66:    a*4356 +b*1.90e7+c=15014
    #      at x=30.3:  a*918  +b*8.4e5 +c=3107.5
    # Solve roughly: subtract -> a~3.5, b~ -1.5e-6? Let's just fit a smooth
    # even function: f(x)=c + a*x^2 + b*x^4 with c=-22.8021.
    # Using x=30.3: a*918+b*8.43e5=3130.3
    #       x=66:   a*4356+b*1.897e7=15036.8
    #       x=123.6:a*15277+b*2.334e8=48017.2
    # From first two: a=(3130.3-8.43e5 b)/918
    #   plug: 4356*(3130.3-8.43e5 b)/918 +1.897e7 b=15036.8
    #   4.745*(3130.3-8.43e5 b)+1.897e7 b=15036.8
    #   14853 -4.0e6 b +1.897e7 b=15036.8 -> 1.497e7 b=183.8 -> b=1.23e-5
    #   a=(3130.3-8.43e5*1.23e-5)/918=(3130.3-10.37)/918=3.398
    # Check x=123.6: 3.398*15277+1.23e-5*2.334e8-22.8=51911+2871-22.8=54759
    #   too high. So quartic overfits; ratio actually DECREASES with x.
    # Better: a*x^2 with slowly varying -> maybe a*|x|^p, p<2.
    #   log-log: x=30.3 y=3130; x=123.6 y=48017
    #   p=log(48017/3130)/log(123.6/30.3)=log(15.34)/log(4.079)=2.73/1.406=1.94
    # So p~1.94, near-quadratic. Use f=c+A*|x|^p with p~1.94.
    # Fit A: at x=66: (15014+22.8)/66^1.94 = 15036.8/66^1.94
    #   66^1.94=exp(1.94*4.19)=exp(8.13)=3400 -> A=4.42
    #   at x=123.6: 123.6^1.94=exp(1.94*4.817)=exp(9.345)=11400 -> A=48017/11400=4.21
    #   at x=30.3: 30.3^1.94=exp(1.94*3.411)=exp(6.617)=748 -> A=3130/748=4.18
    #   at x=88.2: 88.2^1.94=exp(1.94*4.48)=exp(8.69)=5940 -> A=27113/5940=4.56
    # A~4.3, p~1.94. Good enough.
    # Near 0 it's flat at -22.8021; the power law would give -22.8 at x=0 too,
    # but for small x the power term is tiny so it stays near -22.8 anyway.
    # Add a smooth transition: use max of the bowl? Actually power law already
    # gives ~-22.8 for small x. But observed f(2.9)=f(6)=f(1.2)=-22.8021 exactly
    # (flat), while power law gives -22.8+4.3*2.9^1.94=-22.8+4.3*7.8=+10.8.
    # So there IS a flat region for small |x|. Boundary between 6 and 20.3.
    # f(20.3)=1545 -> power law: 4.3*20.3^1.94-22.8=4.3*exp(1.94*3.01)=4.3*exp(5.84)=4.3*344=1479-22.8=1456, close.
    # So boundary ~ where power law departs from floor. Guess |x|<~10 flat.
    # Use smooth: f = -22.8021 + A*max(0,|x|-r)^p with r~8? 
    #   at x=20.3: (12.3)^1.94=exp(1.94*2.51)=exp(4.87)=130 -> 4.3*130=559, too low.
    # Simpler: floor for |x|<10, power law above, with A,p fit on large.
    import math
    c = -22.8021
    A = 4.3
    p = 1.94
    r = 10.0
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        ax = abs(x)
        if ax < r:
            out.append(c)
        else:
            out.append(c + A * (ax ** p))
    return {"y": out}
