import math

def predict(probe):
    # Observations from E1:
    # For x >= 0: y looks like 0.125*x^2 + 2.5? Check:
    #   x=0 -> 2.5; x=1 -> 13.9 (not 2.625); x=3 -> 46.7; x=10 -> 161.5; x=25 -> 407.5
    # Try y = 0.125*x^2 + 2.5 + something. x=25: 0.125*625=78.125+2.5=80.6, not 407.5.
    # Try y = a*x^2 + b: x=25 -> 407.5, x=50 -> 817.5, x=75 -> 1227.5, x=100 -> 1637.5, x=128 -> 2096.7
    # Differences: 50->25: 410 over 25 -> slope ~16.4; 75->50: 410; 100->75: 410; 128->100: 459.2 over 28
    # Looks linear for large x! y = 16.4*x + something? x=50: 16.4*50=820, y=817.5. x=100: 1640 vs 1637.5.
    # So y ≈ 16.4*x - 2.5 for x>=25? x=25: 410-2.5=407.5 yes! x=75: 1230-2.5=1227.5 yes!
    # x=128: 16.4*128=2099.2-2.5=2096.7 yes!
    # For small x>=0: x=10 -> 161.5. 16.4*10-2.5=161.5 yes! x=3: 49.2-2.5=46.7 yes!
    # x=1: 16.4-2.5=13.9 yes! x=0: -2.5? but observed 2.5.
    # So for x>0: y = 16.4*x - 2.5. At x=0: 2.5 (special).
    # For x<0: x=-1 -> 10.7; x=-3 -> 27.1; x=-10 -> 84.5; x=-25 -> 207.5; x=-50 -> 412.5
    # Try y = -16.4*x - 2.5? x=-1: 16.4-2.5=13.9, no (10.7).
    # Try y = -16.4*x + something. x=-25: 410+? =207.5 -> ?=-202.5. Hmm.
    # Differences for negative: -25->-10: 207.5-84.5=123 over 15 -> 8.2; -50->-25: 205 over 25 -> 8.2
    # -75->-50: 205 over 25 -> 8.2; -100->-75: 205 over 25 -> 8.2; -128->-100: 229.6 over 28 -> 8.2
    # So for x<0: y = -8.2*x + c? x=-50: 410+c=412.5 -> c=2.5. x=-25: 205+2.5=207.5 yes!
    # x=-10: 82+2.5=84.5 yes! x=-3: 24.6+2.5=27.1 yes! x=-1: 8.2+2.5=10.7 yes!
    # x=-128: 1049.6+2.5=1052.1 yes!
    # So: x<0: y = -8.2*x + 2.5; x>0: y = 16.4*x - 2.5; x=0: y=2.5
    # Note 16.4 = 2*8.2. And at x=0 both give ±2.5, observed 2.5.
    # Hypothesis: y = 8.2*|x| + 2.5 for x<=0, and 16.4*x-2.5 for x>0.
    # Equivalently: y = 8.2*|x| + 2.5 when x<=0; y = 16.4*x - 2.5 when x>0.
    # Or: y = 8.2*x + 2.5 for x<=0; y = 16.4*x - 2.5 for x>0. Check x=-1: -8.2+2.5=-5.7 no.
    # So it's |x| on negative side. Maybe y = 8.2*|x| + 2.5 - 5*(x>0)? x>0: 8.2x+2.5-5=8.2x-2.5, but observed 16.4x-2.5.
    # So slope doubles for x>0: y = 8.2*|x| + 2.5 + 8.2*x*(x>0) = 8.2*(|x|+x*(x>0)) + 2.5
    # For x>0: 8.2*(x+x)+2.5 = 16.4x+2.5, but observed 16.4x-2.5. Off by 5.
    # Just use piecewise.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        try:
            if x > 0:
                y = 16.4 * x - 2.5
            else:
                y = -8.2 * x + 2.5
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
