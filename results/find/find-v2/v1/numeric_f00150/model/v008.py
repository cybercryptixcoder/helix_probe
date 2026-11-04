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
            ax = abs(x)
            # Flat zero region: (-1.0, 0.0]; at x=-1.0 f=-12.0
            if -1.0 < x <= 0.0:
                ys.append(0.0)
                continue
            if x == -1.0:
                ys.append(-12.0)
                continue
            if ax >= 2:
                # fit a*|x|^6 + b*|x|^4 + c*|x|^2 form; use a*|x|^6 with correction
                if x > 0:
                    a = 2.19
                else:
                    a = 2.22
                # correction term: at |x|=2 ratio ~0.83, at |x|=4 ratio ~0.97, at |x|=10 ~1.0
                # approximate with a*(|x|^6 - k*|x|^4) where k chosen to match
                # From E9: f(2.1)=81.5414, a*2.1^6=2.19*85.766=187.8 -> ratio 0.434
                # Use f = a*|x|^6 * (1 - m/|x|^2) with m fit
                # at |x|=2.1: ratio 0.434 -> m/4.41=0.566 -> m=2.5
                # at |x|=4: 6364/(2.19*4096)=0.709 -> m/16=0.291 -> m=4.66
                # Not clean; use direct power fit: log-log slope
                # E9 pos: f(2.1)=81.54, f(100)=2.1826e12 -> ratio 2.677e10 over (100/2.1)^p
                # (47.6)^p = 2.677e10 -> p = log(2.677e10)/log(47.6) = 23.71/3.86 = 6.14
                # Try f = a*|x|^6 + b*|x|^5 form
                # Simpler: use a*|x|^6 with a adjusted per magnitude via smooth blend
                # Use two-term: f = a*|x|^6 + b*|x|^4, fit from E9
                # pos: 81.5414 = a*85.766 + b*19.448 ; 913.2 = a*729 + b*81
                # From 2.1 and 3: solve
                # 85.766a + 19.448b = 81.5414
                # 729a + 81b = 913.2
                # From second: a = (913.2 - 81b)/729
                # 85.766*(913.2-81b)/729 + 19.448b = 81.5414
                # 107.44 - 9.529b + 19.448b = 81.5414 -> 9.919b = -25.9 -> b=-2.61, a=(913.2+211.4)/729=1.543
                # Check at 4: 1.543*4096 - 2.61*256 = 6320 - 668 = 5652 vs 6364. close-ish
                # Check at 10: 1.543e6 - 2.61e4 = 1.517e6 vs 1.992e6. off
                # Try a*|x|^6 + b*|x|^5: 
                # 85.766a + 40.84b = 81.5414
                # 729a + 243b = 913.2
                # a = (913.2-243b)/729
                # 85.766*(913.2-243b)/729 + 40.84b = 81.5414
                # 107.44 - 28.59b + 40.84b = 81.5414 -> 12.25b = -25.9 -> b=-2.114, a=(913.2+513.7)/729=1.957
                # Check at 4: 1.957*4096 - 2.114*1024 = 8016 - 2165 = 5851 vs 6364
                # Check at 10: 1.957e6 - 2.114e5 = 1.746e6 vs 1.992e6
                # Check at 100: 1.957e12 - 2.114e10 = 1.936e12 vs 2.1826e12
                # Not great. Use pure power fit per side from large values.
                # pos: f(100)=2.1826e12, f(50)=3.3819e10 -> ratio 64.54 over 2^p -> p=6.01
                # So a_pos = 2.1826e12/1e12 = 2.1826
                # neg: f(-100)=2.2166e12 -> a_neg=2.2166
                # Use a*|x|^6 with small correction for moderate x
                if x > 0:
                    a = 2.1826
                else:
                    a = 2.2166
                # correction: at |x|=2, ratio ~0.83; blend factor
                # f(2.1)=81.5414, a*2.1^6=2.1826*85.766=187.2 -> ratio 0.436
                # f(3)=913.2, a*729=1591 -> ratio 0.574
                # f(4)=6364, a*4096=8940 -> ratio 0.712
                # f(6)=84676.8, a*46656=101830 -> ratio 0.831
                # f(10)=1.992e6, a*1e6=2.18e6 -> ratio 0.913
                # f(20)=1.347e8, a*6.4e7=1.397e8 -> ratio 0.964
                # ratio = 1 - c/|x|^q; at 2.1: 0.564=c/2.1^q; at 10: 0.087=c/10^q
                # ratio: 0.564/0.087 = 6.48 = (10/2.1)^q = 4.76^q -> q=1.24
                # c = 0.564*2.1^1.24 = 0.564*2.49 = 1.40
                corr = 1.0 - 1.40 / (ax ** 1.24)
                if corr < 0.3:
                    corr = 0.3
                ys.append(a * (ax ** 6) * corr)
                continue
            if x > 0:
                pts = [
                    (0.01, 4.9573), (0.02, 4.915), (0.04, 4.8319),
                    (0.05, 4.791), (0.06, 4.7505),
                    (0.1, 4.5919), (0.15, 4.3993), (0.2, 4.21),
                    (0.25, 4.0205), (0.35, 3.628), (0.4, 3.419), (0.5, 2.9625),
                    (0.6, 2.4428), (0.75, 1.5342), (0.8, 1.2006), (0.9, 0.5037),
                    (1.0, -0.2), (1.1, -1.7077), (1.2, -2.7576), (1.25, -3.123),
                    (1.35, -3.3794), (1.4, -3.1972), (1.5, -2.0), (1.6, 0.6391),
                    (1.65, 2.6403), (1.75, 8.3293), (1.9, 22.1992), (2.0, 36.0)
                ]
                if x < pts[0][0]:
                    x1, y1 = pts[0]; x2, y2 = pts[1]
                    ys.append(y1 + (x - x1) * (y2 - y1) / (x2 - x1))
                else:
                    for i in range(len(pts) - 1):
                        x1, y1 = pts[i]; x2, y2 = pts[i + 1]
                        if x1 <= x <= x2:
                            t = (x - x1) / (x2 - x1)
                            ys.append(y1 + t * (y2 - y1))
                            break
                    else:
                        ys.append(pts[-1][1])
            else:
                # Negative side, x < -1.0
                pts = [
                    (-2.0, 83.2), (-1.95, 33.6784), (-1.9, 26.6367),
                    (-1.85, 20.4069), (-1.8, 14.9244), (-1.7, 5.9594),
                    (-1.65, 2.364), (-1.6, -0.7102), (-1.55, -3.312),
                    (-1.45, -7.2797), (-1.4, -8.7292), (-1.35, -9.8736),
                    (-1.3, -10.7482), (-1.2, -11.8166), (-1.15, -12.0687),
                    (-1.1, -12.1679), (-1.05, -12.1378), (-1.02, -12.0668),
                    (-1.01, -12.0352), (-1.005, -12.0181), (-1.003, -12.0109),
                    (-1.002, -12.0073), (-1.0008, -12.0029), (-1.0005, -12.0018),
                    (-1.0002, -12.0007), (-1.0001, -12.0004), (-1.00005, -12.0002),
                    (-1.00001, -12.0), (-1.0, -12.0)
                ]
                if x <= pts[0][0]:
                    ys.append(pts[0][1])
                else:
                    for i in range(len(pts) - 1):
                        x1, y1 = pts[i]; x2, y2 = pts[i + 1]
                        if x1 <= x <= x2:
                            t = (x - x1) / (x2 - x1)
                            ys.append(y1 + t * (y2 - y1))
                            break
                    else:
                        ys.append(pts[-1][1])
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
