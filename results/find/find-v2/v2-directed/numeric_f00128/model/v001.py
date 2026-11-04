import math

def predict(probe):
    # f is approximately linear outside a small region near 0 [E1]
    # slope ~ -16.8 per unit for large |x| (e.g. -128->867.7, 128->-2152) [E1]
    # near 0 the function is smooth and passes through ~5.4 at x=0 [E1]
    # there is a kink/transition region around |x| < ~2 where slope changes [E1]
    # Model: piecewise-linear-ish smooth curve. Use a tanh-like blend:
    #   f(x) = a*x + b + c*tanh(x/s)  -- captures linear tails + smooth center
    # Fit from E1 points.
    xs = probe.get("x", [])
    out = []
    # Parameters estimated from E1
    # Large-x slope: (867.6846 - (-2151.9921))/(-128-128) = 3020.6767/-256 = -11.7995
    # Actually check: at -128 y=867.68, at 128 y=-2151.99 => slope = -11.80
    # But local slope near 64->128: (-2151.99+1070.40)/64 = -16.90
    # near -128->-96: (651.36-867.68)/32 = -6.76  -- so slope grows with |x|? nonlinear
    # Try cubic-ish: y = p*x + q*x^3? At x=128: p*128+q*128^3 = -2152
    # At x=64: p*64+q*64^3 = -1070.4
    # Solve: 128p + 2097152q = -2151.99
    #        64p + 262144q = -1070.40
    # From 2nd: p = (-1070.40 - 262144q)/64 = -16.725 - 4096q
    # Sub: 128(-16.725-4096q)+2097152q = -2151.99
    #      -2140.8 - 524288q + 2097152q = -2151.99
    #      1572864q = -11.19 => q = -7.114e-6
    #      p = -16.725 - 4096*(-7.114e-6) = -16.725 + 0.02914 = -16.696
    # Check x=32: -16.696*32 -7.114e-6*32768 = -534.27 - 0.233 = -534.5 vs -529.6 ok
    # Check x=16: -267.1 - 0.0291 = -267.2 vs -259.2 (bit off)
    # Check x=8: -133.6 - 0.00364 = -133.6 vs -124.0 (off)
    # So cubic not great near center. There's a smooth transition.
    # Use: y = A*x + B*tanh(x/s) + C
    # At x=0: C = 5.4186
    # Large x: slope -> A + B/s (for x>>s) ; small x: slope -> A + B/s (same!) 
    # Hmm tanh derivative at 0 is 1/s, at inf is 0. So slope decreases with |x|. But data shows slope increases with |x|.
    # So use sinh-like: y = A*x + B*sinh(x/s)? 
    # Let's just fit a smooth odd-ish function. Note f(0)=5.42, f(-x) vs f(x):
    # x=1: -5.32, x=-1: 9.35 => sum=4.03
    # x=2: -22.68, x=-2: 15.91 => sum=-6.77
    # x=4: -56.33, x=-4: 29.43 => sum=-26.9
    # x=8: -124.0, x=-8: 56.47 => sum=-67.5
    # x=16: -259.2, x=-16: 110.56 => sum=-148.6
    # x=32: -529.6, x=-32: 218.72 => sum=-310.9
    # x=64: -1070.4, x=-64: 435.04 => sum=-635.4
    # x=128: -2152.0, x=-128: 867.68 => sum=-1284.3
    # So f(x)+f(-x) is negative and grows ~ -10*x for large x. 
    # f(x)-f(-x) is odd part: at 128: -2152-867.68=-3019.7 => odd slope -11.8
    # even part: (f(x)+f(-x))/2 at 128: -642.15 => even slope -5.0
    # So f(x) ≈ -11.8*x_odd... let's model f(x) = g(x) where g has both even and odd parts.
    # Simpler: fit polynomial through points. Use least squares mentally is hard.
    # Use interpolation via numpy-free: fit y = a*x + b*x^2 + c*x^3 + d (odd+even+cubic)
    # 4 unknowns, use x=0,1,2,4 and x=-1,-2,-4 etc. Actually just do a reasonable fit.
    # From x=0: d=5.4186
    # x=1: a+b+c = -5.3245-5.4186 = -10.7431
    # x=-1: -a+b-c = 9.3469-5.4186 = 3.9283
    # x=2: 2a+4b+8c = -22.6804-5.4186 = -28.099
    # x=-2: -2a+4b-8c = 15.9142-5.4186 = 10.4956
    # From 1&2: 2b = -10.7431+3.9283 = -6.8148 => b=-3.4074
    # 2a+2c = -10.7431-3.9283 = -14.6714 => a+c=-7.3357
    # From 3&4: 8b = -28.099+10.4956 = -17.6034 => b=-2.2004 (inconsistent, so cubic insufficient)
    # The function isn't a low-order polynomial. It's an MLP approximation.
    # Best bet: piecewise linear interpolation on a dense grid, but we only have E1 points.
    # Use monotone cubic / linear interp on E1 grid, extrapolate linearly.
    pts = [(-128,867.6846),(-96,651.3619),(-64,435.0393),(-48,326.878),(-32,218.7167),
           (-16,110.5554),(-8,56.4747),(-4,29.4344),(-2,15.9142),(-1,9.3469),(0,5.4186),
           (1,-5.3245),(2,-22.6804),(4,-56.3287),(8,-124.0066),(16,-259.2056),
           (32,-529.6037),(48,-800.0018),(64,-1070.3998),(128,-2151.9921)]
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None); continue
        if x <= pts[0][0]:
            # extrapolate with slope from first two
            s = (pts[1][1]-pts[0][1])/(pts[1][0]-pts[0][0])
            out.append(pts[0][1] + s*(x-pts[0][0]))
        elif x >= pts[-1][0]:
            s = (pts[-1][1]-pts[-2][1])/(pts[-1][0]-pts[-2][0])
            out.append(pts[-1][1] + s*(x-pts[-1][0]))
        else:
            for i in range(len(pts)-1):
                x0,y0 = pts[i]; x1,y1 = pts[i+1]
                if x0 <= x <= x1:
                    t = (x-x0)/(x1-x0)
                    out.append(y0 + t*(y1-y0))
                    break
    return {"y": out}
