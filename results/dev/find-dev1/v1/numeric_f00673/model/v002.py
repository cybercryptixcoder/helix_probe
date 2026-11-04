def predict(probe):
    # f(x) = a*x^2 + c + bump(x), even, with a localized bump near 0.
    # Fit from data: large |x|: f(128)=2151.2 -> a*16384+c=2151.2
    #               f(96)=1611.8  -> a*9216+c=1611.8
    #               => a*(16384-9216)=539.4 => a=0.0753? Let's refit properly.
    # Use two points: (96,1611.8),(128,2151.2): a=(2151.2-1611.8)/(16384-9216)=539.4/7168=0.07525
    # c=1611.8-0.07525*9216=1611.8-693.5=918.3 -- too big, so pure quadratic doesn't fit.
    # Try a*x^2 + b*x + c? Even so b=0. Check (48,806.4),(96,1611.8),(128,2151.2):
    # a*2304+c=806.4; a*9216+c=1611.8 -> a*6912=805.4 -> a=0.11652; c=806.4-268.5=537.9
    # predict 128: 0.11652*16384+537.9=1909+537.9=2447 -- off by 300. So not pure quadratic.
    # Try a*x^2 with a from 128: 2151.2/16384=0.13130; from 96:1611.8/9216=0.17489; from 48:806.4/2304=0.35
    # Ratio not constant -> there's a linear-ish term? Try a*x^2+b*x (odd) but f is even.
    # Try a*|x|^p: log-log. (48,806.4),(96,1611.8): ratio 2 -> 2^p=2 -> p=1?? no, 1611.8/806.4=1.999
    # (96,1611.8),(128,2151.2): 2151.2/1611.8=1.3347; 128/96=1.3333 -> p=1.0004. So f ~ linear for large x!
    # Check (48,806.4): linear through (96,1611.8) slope 16.79 -> at 48: 806.4. Yes! f(x)≈16.79*|x| for large x.
    # Check (12,203.4): 16.79*12=201.5 close. (6,100.9): 16.79*6=100.7 close. (3,50.36): 50.4 close!
    # (2.5,42.78): 16.79*2.5=41.97 close. (1.5,27.58): 16.79*1.5=25.2 close-ish.
    # (1,16.53): 16.79 close. (0.5,8.66): 8.4 close. (0.25,5.07): 4.2 off. (0,0.755).
    # So f(x) ≈ 16.79*|x| + small correction near 0.
    # Near 0: f(0)=0.755, f(0.25)=5.07 vs 4.2 -> bump ~0.9; f(0.5)=8.66 vs 8.4 -> 0.26.
    # Actually looks like f(x) = 16.79*|x| + 0.755*exp(-(x/0.3)^2)? f(0)=0.755, f(0.25)=4.2+0.755*exp(-0.69)=4.2+0.38=4.58 vs 5.07.
    # Simpler: f(x) = 16.79*|x| + 0.755 for small, but f(0.25)=4.2+0.755=4.96 vs 5.07 close.
    # f(0.5)=8.4+0.755=9.15 vs 8.66. Hmm.
    # Best simple: f(x) = 16.79*|x| + 0.755*exp(-(x/0.5)^2)
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            ax = abs(float(x))
            base = 16.79 * ax
            bump = 0.755 * math.exp(-(ax / 0.5) ** 2)
            out.append(base + bump)
        except Exception:
            out.append(None)
    return {"y": out}
