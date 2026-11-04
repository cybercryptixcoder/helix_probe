import math

def predict(probe):
    # Observations [E1]:
    # - x <= 0 (at least -0.5 and below): output null (undefined)
    # - x = 0.5: y = -139.9873
    # - x = 1: y = 1.1
    # - x >= 2: y appears linear with slope ~70.54365
    #   Check: 142.1873, 283.2746, 424.3619, ... differences = 141.0873 each per +2 x
    #   slope = 70.54365 per unit x
    #   At x=2: 142.1873. Intercept: 142.1873 - 2*70.54365 = 1.1
    #   So for x>=1: y = 70.54365*x + 1.1? Check x=1: 71.64365 != 1.1. No.
    #   Try y = 70.54365*(x-1) + 1.1: x=2 -> 71.64365, no.
    #   Actually 142.1873 - 1.1 = 141.0873 = 2*70.54365. So y = 70.54365*x + 1.1 - 70.54365*? 
    #   Let's fit: y = a*x + b. Using x=2,y=142.1873 and x=4,y=283.2746:
    #   a = 70.54365, b = 142.1873 - 2*70.54365 = 1.1
    #   So y = 70.54365*x + 1.1 for x>=2. Check x=1: 71.64365, but observed 1.1. So x=1 is special.
    # - x=1: y=1.1 (matches intercept, maybe piecewise)
    # - x=0.5: y=-139.9873. 
    # Hypothesis: for x>0, y = 70.54365*x + 1.1, except x=0.5 gives -139.9873?
    #   Check x=0.5 with formula: 36.371825, not -139.9873.
    # Alternative: maybe y = 70.54365*x + 1.1 for x>=1, and something else for 0<x<1.
    #   At x=0.5: -139.9873. At x=1: 1.1. Slope between: (1.1-(-139.9873))/0.5 = 282.1746.
    #   Hmm. Maybe y = 282.1746*x - 281.0746? At x=0.5: 141.0873-281.0746=-139.9873 ✓, at x=1: 282.1746-281.0746=1.1 ✓.
    #   So for 0<x<=1: y = 282.1746*x - 281.0746? But at x=0.5 works, x=1 works.
    #   But is it linear in (0,1]? Only two points. Could be.
    # - x<=0: null.
    # Best guess: piecewise linear.
    #   x <= 0: null
    #   0 < x <= 1: y = 282.1746*x - 281.0746
    #   x > 1: y = 70.54365*x + 1.1
    # Check continuity at x=1: both give 1.1. Good.
    # Check x=0.5: 141.0873 - 281.0746 = -139.9873 ✓
    # Check x=2: 141.0873+1.1=142.1873 ✓
    # Check x=128: 70.54365*128+1.1 = 9030.5872+1.1=9031.6872? But observed 988.7111.
    #   Wait 70.54365*128 = 9030.5872, but observed 988.7111. That's way off!
    #   Recheck: 988.7111 - 1.1 = 987.6111. /128 = 7.7157. Hmm.
    #   Let me recompute slope from x=64 to x=128: (988.7111-847.6238)/64 = 141.0873/64 = 2.20449.
    #   From x=32 to 64: (847.6238-706.5365)/32 = 141.0873/32 = 4.40898.
    #   From x=16 to 32: 141.0873/16 = 8.81795.
    #   From x=8 to 16: 141.0873/8 = 17.6359.
    #   From x=4 to 8: 141.0873/4 = 35.2718.
    #   From x=2 to 4: 141.0873/2 = 70.54365.
    #   So the increment per doubling is constant 141.0873! That's logarithmic/exponential.
    #   y(x) = a*log2(x) + b? Check: y(2)=142.1873, y(4)=283.2746, diff=141.0873 per doubling.
    #   So y = 141.0873*log2(x) + c. At x=2: 141.0873*1 + c = 142.1873 -> c=1.1.
    #   Check x=1: 141.0873*0+1.1=1.1 ✓
    #   Check x=0.5: 141.0873*(-1)+1.1 = -139.9873 ✓
    #   Check x=8: 141.0873*3+1.1 = 423.2619+1.1=424.3619 ✓
    #   Check x=128: 141.0873*7+1.1 = 987.6111+1.1=988.7111 ✓
    # So for x>0: y = 141.0873*log2(x) + 1.1. And x<=0: null.
    # 141.0873 = ? maybe 141.0873... could be 100*log2(e)? No. Just use constant.
    out = []
    for x in probe.get("x", []):
        try:
            if x is None or x <= 0:
                out.append(None)
            else:
                out.append(141.0873 * math.log2(x) + 1.1)
        except Exception:
            out.append(None)
    return {"y": out}
