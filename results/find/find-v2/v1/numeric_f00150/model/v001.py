import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            # Rough empirical model based on E1.
            # Large |x|: super-exponential growth, positive.
            # Small |x|: small values, sign change near x=1.
            if abs(x) >= 2:
                # Fit-ish: y ~ exp(a*|x|^p) with p>2.
                # Use log-interpolation from observed points.
                # Observed: x=2 ->36, 4->6364, 8->505723.2, 16->34874780.8,
                # 32->2301076128, 64->149291043136, 128->9616222410163.2
                # log y vs log x roughly linear with slope ~ 4.5-5.
                # Try y = exp(k * |x|^q). Estimate q.
                # Use two anchor points: x=4 (6364) and x=64 (1.4929e11)
                # ln(6364)=8.758, ln(1.4929e11)=25.73
                # ratio of logs = 2.938 over x ratio 16 -> q = log(2.938)/log(16) ~ 0.39? no.
                # Actually check power law: y ~ C*|x|^p
                # 6364 = C*4^p, 1.4929e11 = C*64^p
                # ratio = 2.345e7 = 16^p -> p = ln(2.345e7)/ln(16) ~ 16.97/2.77 ~ 6.12
                # So y ~ C*|x|^6.1
                # C = 6364/4^6.1 = 6364/4^6.1. 4^6.1 = exp(6.1*1.386)=exp(8.456)=4700 -> C~1.35
                # Check x=2: 1.35*2^6.1=1.35*68.6=92.6 vs 36. Not great.
                # Try exponential in x: y = A*exp(b*|x|)
                # 6364=A*exp(4b), 1.4929e11=A*exp(64b)
                # ratio=2.345e7=exp(60b) -> b=ln(2.345e7)/60=16.97/60=0.283
                # A=6364/exp(1.132)=6364/3.10=2053
                # Check x=8: 2053*exp(2.264)=2053*9.62=19750 vs 505723. No.
                # Try y = A*exp(b*|x|^2)
                # 6364=A*exp(16b), 1.4929e11=A*exp(4096b)
                # ratio=2.345e7=exp(4080b) -> b=16.97/4080=0.00416
                # A=6364/exp(0.0666)=6364/1.069=5953
                # Check x=8: 5953*exp(0.266)=5953*1.305=7770 vs 505723. No.
                # Try y = A*exp(b*|x|^3)
                # 6364=A*exp(64b), 1.4929e11=A*exp(262144b)
                # ratio=2.345e7=exp(262080b) -> b=16.97/262080=6.475e-5
                # A=6364/exp(0.004144)=6364/1.00415=6338
                # Check x=8: 6338*exp(6.475e-5*512)=6338*exp(0.03315)=6338*1.0337=6551 vs 505723. No.
                # Hmm, growth is faster than exp(b*x^3)? Check x=16: 6338*exp(6.475e-5*4096)=6338*exp(0.2652)=6338*1.3036=8262 vs 3.49e7. Way off.
                # So growth between x=8 and x=16 is huge: 505723 -> 3.49e7, ratio 69 over x doubling.
                # Between 16 and 32: 3.49e7 -> 2.30e9, ratio 66.
                # Between 32 and 64: 2.30e9 -> 1.49e11, ratio 65.
                # Between 64 and 128: 1.49e11 -> 9.62e12, ratio 64.5.
                # So each doubling multiplies by ~65. That's y ~ |x|^p with 2^p=65 -> p=6.02.
                # So y ~ C*|x|^6.0. Check C: at x=64, 1.49e11/64^6 = 1.49e11/6.87e10=2.17
                # at x=32: 2.30e9/32^6=2.30e9/1.07e9=2.15
                # at x=16: 3.49e7/16^6=3.49e7/1.678e7=2.08
                # at x=8: 505723/8^6=505723/262144=1.93
                # at x=4: 6364/4096=1.55
                # at x=2: 36/64=0.5625
                # So roughly y ~ 2*|x|^6 for large |x|, with coefficient growing toward 2.
                # But sign: for negative x, y is positive too (all positive for |x|>=2).
                # Actually check: x=-2 -> 83.2, x=2 -> 36. Different! So not even function.
                # x=-4 -> 9472.8, x=4 -> 6364. x=-8 -> 614392, x=8 -> 505723.2
                # x=-16 -> 38418480, x=16 -> 34874780.8
                # x=-32 -> 2414990483.2, x=32 -> 2301076128
                # x=-64 -> 152940401548.8, x=64 -> 149291043136
                # x=-100 -> 2.2166e12, x=100 -> 2.1826e12
                # x=-128 -> 9.733e12, x=128 -> 9.616e12
                # So for negative x, slightly larger. Ratio approaches 1 for large |x|.
                # Maybe y = something like (x^2 + a*x + b)^3? Let's test.
                # At x=0: y=0. So b=0? Then y=(x^2+a*x)^3 = x^3(x+a)^3.
                # At x=1: -0.2. (1+a)^3 = -0.2 -> 1+a = -0.585 -> a=-1.585
                # At x=2: (4+2a)^3 = (4-3.17)^3=0.83^3=0.57 vs 36. No.
                # Try y = x^2 * (x-1)^2 * something? At x=1, y=-0.2 not 0.
                # Hmm f(1)=-0.2, f(0)=0, f(0.5)=2.9625.
                # Let's just use a piecewise empirical fit.
                # For |x|>=2, use y ~ c*|x|^6 with slight asymmetry.
                # Fit c for positive: at x=128, 9.616e12/128^6 = 9.616e12/4.398e12=2.187
                # at x=100: 2.1826e12/1e12=2.1826
                # at x=64: 149291043136/6.87e10=2.173
                # at x=32: 2301076128/1.0737e9=2.143
                # at x=16: 34874780.8/16777216=2.079
                # at x=8: 505723.2/262144=1.929
                # at x=4: 6364/4096=1.554
                # at x=2: 36/64=0.5625
                # So coefficient approaches ~2.19 for large x.
                # For negative: at x=-128: 9.733e12/4.398e12=2.213
                # at x=-100: 2.2166e12/1e12=2.2166
                # at x=-64: 152940401548.8/6.87e10=2.226
                # at x=-32: 2414990483.2/1.0737e9=2.249
                # at x=-16: 38418480/16777216=2.290
                # at x=-8: 614392/262144=2.344
                # at x=-4: 9472.8/4096=2.313
                # at x=-2: 83.2/64=1.3
                # So negative side coefficient ~2.22-2.34 for |x|>=8.
                # Let's use: for |x|>=2, y = c(x)*|x|^6 where c interpolates.
                # Simple: c = 2.2 for |x|>=8, and interpolate for 2<=|x|<8.
                # Actually let's just do a smooth fit: y = A*|x|^6 + B*|x|^4 + C*|x|^2 + D*x + E?
                # Too complex. Let's use log-linear interpolation in log|x| for |x|>=2.
                # Anchor points (positive): (2,36),(4,6364),(8,505723.2),(16,34874780.8),(32,2301076128),(64,149291043136),(128,9616222410163.2)
                # Anchor points (negative): (2,83.2),(4,9472.8),(8,614392),(16,38418480),(32,2414990483.2),(64,152940401548.8),(128,9733034614144)
                # Use log-log interpolation.
                pos_anchors = [(2,36.0),(4,6364.0),(8,505723.2),(16,34874780.8),(32,2301076128.0),(64,149291043136.0),(128,9616222410163.2)]
                neg_anchors = [(2,83.2),(4,9472.8),(8,614392.0),(16,38418480.0),(32,2414990483.2),(64,152940401548.8),(128,9733034614144.002)]
                anchors = pos_anchors if x >= 0 else neg_anchors
                ax = abs(x)
                if ax >= 128:
                    # extrapolate using last two
                    x1,y1 = anchors[-2]; x2,y2 = anchors[-1]
                    slope = (math.log(y2)-math.log(y1))/(math.log(x2)-math.log(x1))
                    val = math.exp(math.log(y2) + slope*(math.log(ax)-math.log(x2)))
                    ys.append(val)
                else:
                    # find bracketing
                    for i in range(len(anchors)-1):
                        x1,y1 = anchors[i]; x2,y2 = anchors[i+1]
                        if x1 <= ax <= x2:
                            t = (math.log(ax)-math.log(x1))/(math.log(x2)-math.log(x1))
                            val = math.exp(math.log(y1) + t*(math.log(y2)-math.log(y1)))
                            ys.append(val)
                            break
                    else:
                        ys.append(None)
            else:
                # small |x| < 2: interpolate from known points
                # known: (-1,-12), (0,0), (0.5,2.9625), (1,-0.2)
                # also (2,36) and (-2,83.2) as boundaries
                pts = [(-2,83.2),(-1,-12.0),(0,0.0),(0.5,2.9625),(1,-0.2),(2,36.0)]
                # linear interpolation
                if x <= pts[0][0]:
                    ys.append(pts[0][1])
                elif x >= pts[-1][0]:
                    ys.append(pts[-1][1])
                else:
                    for i in range(len(pts)-1):
                        x1,y1 = pts[i]; x2,y2 = pts[i+1]
                        if x1 <= x <= x2:
                            t = (x-x1)/(x2-x1)
                            ys.append(y1 + t*(y2-y1))
                            break
                    else:
                        ys.append(None)
        return {"y": ys}
    except Exception:
        return {"y": [None]*len(probe.get("x", []))}
