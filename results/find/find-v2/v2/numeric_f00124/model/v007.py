import math

# Beliefs (evidence-based):
# - For x >= 0, f is essentially quadratic: f(x) ≈ 106 + 0.155*x + 0.0008*x^2? Let's fit.
#   E2: x=0 -> 106.05; x=10 -> 1220.33; x=20 -> 2334.61; x=100 -> 11248.83; x=120 -> 13477.39
#   Differences: 0->10: 1114.28; 10->20: 1114.28; linear in x! So f(x) = 106.05 + 111.428*x for x>=0?
#   Check x=120: 106.05 + 111.428*120 = 13477.4 ✓. x=88.2: 106.05+111.428*88.2=9934.0 ✓.
#   So for x>=0: f(x) = 106.0528 + 111.4280*x  (linear!)
# - For x <= -10 (approx), f is also linear: E2 x=-10:235.27, -20:495.99, -40:1017.42, -60:1538.86,
#   -80:2060.29, -100:2581.72, -120:3103.16. Slope: (3103.16-235.27)/(-110) = -26.0717. 
#   f(x) = 235.2718 + 26.0717*(-10 - x)? Actually f(x)= -26.0717*x + (-25.44)? Check x=-10: 260.717-25.44=235.27 ✓
#   So for x <= -10: f(x) = 26.0717*(-x) - 25.44, i.e. -26.0717*x - 25.44. Check x=-128: 3337.18-25.44=3311.73 ✓
# - For -10 < x < 0, there's a dip/valley: f has a minimum around x=-1.05 (~6.37), rises to ~106 at x=0
#   and to ~235 at x=-10. This is a smooth curve (looks like a parabola or Gaussian-ish).
#   E10: x=-9.5:222.24, -9:209.20, -8.5:196.16, ... -5:104.91, ... -1:6.85
#   Differences per 0.5: -13.04 each, constant! So linear from -9.5 to -2.5? 
#   Check: -9.5->222.24, -9->209.20 diff -13.04; -2.5->39.73, -2.2->31.91 diff -7.82 over 0.3 => -26.07/unit.
#   Hmm, actually from -9.5 to -2.5: slope = (39.73-222.24)/(7) = -26.07. Same as outer slope!
#   So for -9.5 <= x <= -2.5, f(x) = -26.0717*x - 25.44? Check x=-5: 130.36-25.44=104.92 ✓
#   So the left linear region extends to about x=-2.5!
#   Wait but x=-2.5: -26.0717*(-2.5)-25.44 = 65.18-25.44=39.74 ✓
#   x=-2.2: 57.36-25.44=31.92 ✓. x=-2.0: 52.14-25.44=26.70 ✓ (E4)
#   x=-1.9: 49.54-25.44=24.10 ✓ (E14). x=-1.8: 46.93-25.44=21.49 ✓ (E6)
#   x=-1.6: 41.71-25.44=16.27 ✓. x=-1.4: 36.50-25.44=11.06? E6 says 11.24. Close but off.
#   x=-1.2: 31.29-25.44=5.85? E6 says 7.47. Off.
#   So the linear left region ends around x=-1.5 or so, then there's a smooth minimum.
# - Minimum around x=-1.05, value ~6.37. Then rises to the right, reaching x=0 at 106.05.
#   For -1.5 to 0, curve: x=-1.5:13.66, -1.25:8.21, -1.1:6.44, -1.05:6.42, -1.0:6.85, -0.9:10.63,
#   -0.8:18.22, -0.5:50.34, -0.1:94.91, 0:106.05.
#   This looks like a parabola with min at ~-1.05. Fit: f(x) = a*(x+1.05)^2 + 6.37?
#   At x=0: a*1.1025+6.37=106.05 => a=90.4. At x=-0.5: a*0.3025+6.37=27.3+6.37=33.7? But actual 50.34.
#   Not a simple parabola. Maybe it's smooth (MLP approximation of something).
#   Let's just interpolate smoothly. Actually the data from -1.5 to 0 looks like it could be a 
#   quadratic-ish or Gaussian. Let's try f(x) = A*exp(-((x-c)/w)^2)+B? No, it's not symmetric.
#   Better: use a piecewise linear interpolation of the dense data we have in [-1.5, 0].
# - For x in [-2.5, -1.5], transition from linear (slope -26.07) to the valley.
#   Data: -2.5:39.73, -2.2:31.91, -2.0:26.70, -1.9:24.09, -1.8:21.48, -1.7:18.88, -1.6:16.27, -1.5:13.66
#   From -2.5 to -1.5 slope: (13.66-39.73)/1 = -26.07. Still linear! 
#   So linear extends to -1.5. Then -1.5 to -1.05 is the curve down to min.
#   x=-1.4:11.24, -1.3:9.06, -1.25:8.21, -1.2:7.47, -1.15:6.85, -1.1:6.44, -1.05:6.42, -1.0:6.85
#   So minimum ~6.37 at x~-1.05.
# - Conclusion: 
#   x >= 0: f = 106.0528 + 111.4280*x
#   x <= -1.5: f = -26.0717*x - 25.44  (linear)
#   -1.5 < x < 0: smooth valley, minimum ~6.37 at x≈-1.05.
#   Wait, but x=0 gives 106.05 from linear formula: 106.05+0=106.05 ✓. So right linear starts at x=0.
#   Actually let's check: is x=0 the boundary? For x slightly negative, e.g. -0.1: 94.91, but linear 
#   would give -26.07*(-0.1)-25.44 = 2.61-25.44 = -22.8. No. So valley region is -1.5 to 0.
#   And right linear is x>=0.
# - The valley: I'll model with a smooth function. Let's try a Gaussian-ish bump on top of a line?
#   Actually, simplest: fit a cubic or use interpolation. But we need to predict ANY x in (-1.5, 0).
#   Let's look at shape: min at -1.05 (6.37), rises to 13.66 at -1.5, and to 106.05 at 0.
#   The rise to the right is much steeper. Could be f(x) = a*(x+1.05)^2 + b for the right side?
#   At x=0: a*1.1025+b=106.05; at x=-0.5: a*0.3025+b=50.34 => subtract: a*0.8=55.71 => a=69.64, b=29.3.
#   Check x=-0.8: 69.64*0.0625+29.3=4.35+29.3=33.65? Actual 18.22. No.
#   Try f(x) = A*exp(k*(x+1.05)) + B? At x=-1.05: A+B=6.37. At x=0: A*exp(1.05k)+B=106.05.
#   At x=-0.5: A*exp(0.55k)+B=50.34. 
#   Let's solve: let u=exp(0.5k). Then exp(0.55k)=u^1.1, exp(1.05k)=u^2.1.
#   A*u^2.1+B=106.05; A*u^1.1+B=50.34; A+B=6.37.
#   Subtract: A(u^2.1-1)=99.68; A(u^1.1-1)=43.97. Ratio: (u^2.1-1)/(u^1.1-1)=2.267.
#   Try u=3: (3^2.1-1)/(3^1.1-1)=(9.79-1)/(3.35-1)=8.79/2.35=3.74. Too big.
#   Try u=2: (4.29-1)/(2.14-1)=3.29/1.14=2.89. Still big.
#   Try u=1.5: (2.34-1)/(1.56-1)=1.34/0.56=2.39. Close.
#   u=1.45: (2.19-1)/(1.51-1)=1.19/0.51=2.33. u=1.4: (2.06-1)/(1.45-1)=1.06/0.45=2.36.
#   u=1.42: ~2.34. Hmm target 2.267. u=1.35: (1.88-1)/(1.39-1)=0.88/0.39=2.26. 
#   So u≈1.35, k=2*ln(1.35)=0.60. A=43.97/(1.35^1.1-1)=43.97/(1.39-1)=43.97/0.39=112.7.
#   B=6.37-112.7=-106.3. Check x=-1.5: A*exp(0.60*(-0.45))+B=112.7*exp(-0.27)-106.3=112.7*0.763-106.3=86.0-106.3=-20.3. Actual 13.66. No.
#   The exponential doesn't fit the left side. So it's asymmetric.
#   Let's just use piecewise linear interpolation with the dense data points we have. That's a 
#   reasonable model of the mechanism (the MLP approximates a smooth function; linear interp is close).
#   Actually, better: fit a smooth function. But given data density, linear interp is fine.
# - Also check: is there really a "dip" or is it just the two lines meeting? The two lines:
#   Left: y=-26.07x-25.44, at x=-1.05 gives 27.38-25.44=1.94. Right: y=106.05+111.43x, at x=-1.05 gives 106.05-117.0=-10.95. 
#   They cross somewhere: -26.07x-25.44=106.05+111.43x => -137.5x=131.49 => x=-0.956. 
#   At x=-0.956, y=-26.07*(-0.956)-25.44=24.92-25.44=-0.52.
#   But actual f(-0.956)≈7. So the function doesn't follow either line in the dip; it's a smooth 
#   valley that's above both lines. This is the "different behavior" interval: roughly (-1.5, 0).
#   Actually the left line matches down to -1.5, and right line matches from 0. In between, valley.
# - So model:
#   if x >= 0: 106.0528 + 111.4280*x
#   elif x <= -1.5: -26.0717*x - 25.44
#   else: interpolate the valley.
#   Wait, check x=-1.5: left gives 39.11-25.44=13.67 ✓ (E14:13.6624). Good.
#   Check x=-1.6: left gives 41.71-25.44=16.27 ✓. So left linear valid up to -1.5.
#   Check x=-1.4: left gives 36.50-25.44=11.06, actual 11.24. Slight off. So boundary ~-1.5.
#   For valley, use data points:
#   (-1.5,13.6624),(-1.45,12.3588),(-1.4,11.2441),(-1.35,10.1415),(-1.3,9.0565),(-1.25,8.2083),
#   (-1.2,7.4701),(-1.15,6.8547),(-1.1,6.436),(-1.08,6.3684),(-1.06,6.3832),(-1.05,6.42?),
#   (-1.04,6.4589),(-1.02,6.5888),(-1.0,6.8494),(-0.98,7.2943),(-0.96,7.9129),(-0.94,8.703),
#   (-0.92,9.5811),(-0.9,10.6298),(-0.88,11.8704),(-0.86,13.2846),(-0.84,14.7957),(-0.82,16.4569),
#   (-0.8,18.223),(-0.78,20.0345),(-0.76,21.9288),(-0.74,23.8685),(-0.72,25.9521),(-0.7,28.0616),
#   (-0.68,30.2818),(-0.65,33.6247),(-0.6,39.1961),(-0.55,44.7675),(-0.5,50.3388),(-0.4,61.4816),
#   (-0.3,72.6244),(-0.2,83.7672),(-0.1,94.91),(-0.02,103.8242),(0,106.0528)
#   Linear interpolation between these.
# - Also check: is the right side really linear all the way? E2 shows 10->1220.33, 20->2334.61: 
#   slope 111.428. Yes. And x=88.2: 106.05+111.428*88.2=9934.0 ✓.
# - What about x between 0 and 10? E11 x=2.0: 328.91. Formula: 106.05+111.428*2=328.91 ✓.
#   x=1.2: 106.05+133.71=239.76 ✓ (E3). x=2.9: 106.05+323.14=429.19 ✓.
# - Great. So the model is piecewise linear with a smooth valley.

def predict(probe):
    try:
        xs = probe["x"]
    except Exception:
        return {"y": []}
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x >= 0:
            y = 106.0528 + 111.4280 * x
        elif x <= -1.5:
            y = -26.0717 * x - 25.44
        else:
            y = valley(x)
        ys.append(round(y, 4))
    return {"y": ys}

# Valley data points (x, y) from experiments, sorted
_VALLEY = [
    (-1.5, 13.6624), (-1.45, 12.3588), (-1.4, 11.2441), (-1.35, 10.1415),
    (-1.3, 9.0565), (-1.25, 8.2083), (-1.2, 7.4701), (-1.15, 6.8547),
    (-1.1, 6.436), (-1.08, 6.3684), (-1.06, 6.3832), (-1.04, 6.4589),
    (-1.02, 6.5888), (-1.0, 6.8494), (-0.98, 7.2943), (-0.96, 7.9129),
    (-0.94, 8.703), (-0.92, 9.5811), (-0.9, 10.6298), (-0.88, 11.8704),
    (-0.86, 13.2846), (-0.84, 14.7957), (-0.82, 16.4569), (-0.8, 18.223),
    (-0.78, 20.0345), (-0.76, 21.9288), (-0.74, 23.8685), (-0.72, 25.9521),
    (-0.7, 28.0616), (-0.68, 30.2818), (-0.65, 33.6247), (-0.6, 39.1961),
    (-0.55, 44.7675), (-0.5, 50.3388), (-0.4, 61.4816), (-0.3, 72.6244),
    (-0.2, 83.7672), (-0.1, 94.91), (-0.02, 103.8242), (0.0, 106.0528),
]

def valley(x):
    # linear interpolation
    pts = _VALLEY
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i+1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]
