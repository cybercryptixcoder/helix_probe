import math

def predict(probe):
    # Observations [E1]:
    # For x >= 1: y = x + 11.6 (e.g. x=1 -> 12.0, x=128 -> 342.2? no: 128+11.6=139.6, but observed 342.2)
    # Let's recheck. x=1 -> 12.0, x=2 -> 14.6, x=4 -> 19.8, x=8 -> 30.2, x=16 -> 51.0, x=32 -> 92.6, x=50 -> 139.4, x=100 -> 269.4, x=128 -> 342.2
    # Differences: 1->2: 2.6, 2->4: 5.2, 4->8: 10.4, 8->16: 20.8, 16->32: 41.6, 32->50: 46.8, 50->100: 130, 100->128: 72.8
    # Looks like y = 2.6*x + 9.4? Check x=1: 12.0 yes. x=2: 14.6 yes. x=4: 19.8 yes. x=8: 30.2 yes. x=16: 51.0 yes. x=32: 92.6 yes.
    # x=50: 2.6*50+9.4 = 139.4 yes. x=100: 269.4 yes. x=128: 342.2 yes.
    # So for x >= 1: y = 2.6*x + 9.4
    # For x <= -1: x=-1 -> 11.6, x=-2 -> 9.0, x=-4 -> 3.8, x=-8 -> -6.6, x=-16 -> -27.4, x=-32 -> -69.0, x=-50 -> -115.8, x=-75 -> -180.8, x=-100 -> -245.8, x=-128 -> -318.6
    # Check y = 2.6*x + 14.2? x=-1: 11.6 yes. x=-2: 9.0 yes. x=-4: 3.8 yes. x=-8: -6.6 yes. x=-16: -27.4 yes. x=-32: -69.0 yes. x=-50: -115.8 yes. x=-75: -180.8 yes. x=-100: -245.8 yes. x=-128: -318.6 yes.
    # So for x <= -1: y = 2.6*x + 14.2
    # At x=0: y = 444.28 (outlier / special value)
    # So: piecewise linear with slope 2.6, intercept 9.4 for x>=1, intercept 14.2 for x<=-1, and f(0)=444.28.
    # This is a "special interval" at x=0? Or maybe f(0) is just a spike.
    # Hypothesis: f(x) = 2.6*x + 9.4 for x>0, 2.6*x + 14.2 for x<0, and f(0)=444.28.
    # The intercept difference (9.4 vs 14.2) suggests a jump of 4.8 at 0, plus a spike at 0.
    # Alternative: f(x) = 2.6*x + 9.4 + 4.8*(x<0) + (444.28 - 9.4)*(x==0)
    # Let's write it cleanly.
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(444.28)
        elif x > 0:
            out.append(2.6 * x + 9.4)
        else:
            out.append(2.6 * x + 14.2)
    return {"y": out}
