import math

def predict(probe):
    # f is piecewise linear in x with slope 2.6 outside a special interval [E1]
    # slope: (y(128)-y(96))/(128-96) = (342.2-259.0)/32 = 2.6 [E1]
    # also (y(64)-y(32))/32 = (175.8-92.6)/32 = 2.6 [E1]
    # intercept: y = 2.6x + b; at x=128: 342.2 = 332.8 + b => b = 9.4 [E1]
    # check x=-128: 2.6*(-128)+9.4 = -332.8+9.4 = -323.4 vs -318.6 (close-ish)
    # The x=0 value is 444.28, a huge spike, not on the line [E1]
    # Around x=0 the values are small: x=-1 -> 11.6, x=1 -> 12.0, x=-2 -> 9.0, x=2 -> 14.6
    # These don't fit 2.6x+9.4 either (would give 6.8, 12.0, 4.2, 14.6)
    # So there's a special interval near 0 where behavior differs [E1]
    # Hypothesis: outside a central interval, f(x) = 2.6x + 9.4 (approximately)
    # Inside, something else. Let's fit inside points.
    # x=0: 444.28 (spike)
    # x=+-1: ~11.8, x=+-2: ~11.8, x=+-4: ~11.8, x=+-8: ~11.8
    # Actually: -8:-6.6, -4:3.8, -2:9.0, -1:11.6, 1:12.0, 2:14.6, 4:19.8, 8:30.2
    # These look like 2.6x+9.4 too! Check: x=-8: -20.8+9.4=-11.4 vs -6.6. Not quite.
    # Hmm, x=8: 20.8+9.4=30.2 ✓. x=4: 10.4+9.4=19.8 ✓. x=2: 5.2+9.4=14.6 ✓
    # x=1: 2.6+9.4=12.0 ✓. x=-1: -2.6+9.4=6.8 vs 11.6 ✗
    # x=-2: -5.2+9.4=4.2 vs 9.0 ✗. x=-4: -10.4+9.4=-1.0 vs 3.8 ✗
    # x=-8: -20.8+9.4=-11.4 vs -6.6 ✗
    # So for x>=0, f=2.6x+9.4. For x<0, offset differs by ~4.8?
    # x=-1: 11.6 vs 6.8, diff 4.8. x=-2: 9.0 vs 4.2, diff 4.8. x=-4: 3.8 vs -1.0, diff 4.8
    # x=-8: -6.6 vs -11.4, diff 4.8. x=-16: -27.4 vs -32.2, diff 4.8
    # x=-32: -69.0 vs -73.8, diff 4.8. x=-48: -110.6 vs -115.4, diff 4.8
    # x=-64: -152.2 vs -157.0, diff 4.8. x=-96: -235.4 vs -240.2, diff 4.8
    # x=-128: -318.6 vs -323.4, diff 4.8
    # So for x<0: f = 2.6x + 9.4 + 4.8 = 2.6x + 14.2
    # And x=0: 444.28 is a special spike (maybe 1/0 or something)
    # Hypothesis: f(x) = 2.6x + 14.2 for x<0, 2.6x+9.4 for x>0, and 444.28 at x=0
    # The spike at 0 might be a special value. Could be 1/x-ish? But 444.28...
    # Maybe f(0) is defined specially. Or maybe it's a discontinuity.
    # Let's just model: x<0 -> 2.6x+14.2, x>0 -> 2.6x+9.4, x==0 -> 444.28
    # The 4.8 offset for x<0 suggests a step/breakpoint at 0.
    
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x < 0:
            out.append(2.6*x + 14.2)
        elif x > 0:
            out.append(2.6*x + 9.4)
        else:
            out.append(444.28)
    return {"y": out}
