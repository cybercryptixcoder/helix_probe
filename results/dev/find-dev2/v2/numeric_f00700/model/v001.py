def predict(probe):
    # For x >= 0: f(x) = x + 1 [E1: 0->-1? no...]
    # Re-examine E1:
    #   x=-100 -> -101 = x-1
    #   x=-50  -> -51  = x-1
    #   x=-20  -> -21  = x-1
    #   x=-10  -> -11  = x-1
    #   x=-5   -> -6   = x-1
    #   x=-2   -> -3   = x-1
    #   x=-1   -> -2   = x-1
    #   x=-0.5 -> -1   = x-0.5? -0.5-0.5=-1 yes
    #   x=0    -> -1   = x-1
    #   x=0.5  -> 2    = ? 
    #   x=1    -> 2    = x+1
    #   x=2    -> 3    = x+1
    #   x=5    -> 6    = x+1
    #   x=10   -> 11   = x+1
    #   x=20   -> 21   = x+1
    #   x=50   -> 51   = x+1
    #   x=100  -> 101  = x+1
    #   x=128  -> 129  = x+1
    #   x=-128 -> -129 = x-1
    #   x=0.1  -> 2    = ? (not x+1=1.1, not x-1)
    #
    # Hypothesis: f(x) = x + sign(x), with sign(0) treated as -1?
    #   x=-0.5: -0.5 + (-1) = -1.5, but observed -1. Doesn't fit.
    # Hypothesis: f(x) = x - 1 for x <= 0, x + 1 for x > 0?
    #   x=0.5 -> 1.5, observed 2. No.
    # Hypothesis: f(x) = x + 1 for x > 0, x - 1 for x <= 0, but 0.5->2 and 0.1->2?
    #   Maybe rounding? 0.5+1=1.5 rounds to 2? 0.1+1=1.1 rounds to 2? No.
    # Hypothesis: f(x) = ceil(x) + 1 for x > 0? ceil(0.5)+1=2 yes, ceil(0.1)+1=2 yes,
    #   ceil(1)+1=2 yes, ceil(2)+1=3 yes, ceil(5)+1=6 yes. Fits positive!
    # For x <= 0: floor(x) - 1? floor(-0.5)-1 = -1-1 = -2, observed -1. No.
    #   floor(-0.5) = -1, -1-1=-2. No.
    #   Try ceil(x)-1 for x<=0: ceil(-0.5)-1 = 0-1 = -1 yes! ceil(-1)-1=-1-1=-2 yes,
    #   ceil(-2)-1=-2-1=-3 yes, ceil(0)-1=0-1=-1 yes, ceil(-128)-1=-128-1=-129 yes.
    # So: f(x) = ceil(x) + 1 for x > 0; f(x) = ceil(x) - 1 for x <= 0.
    # Equivalently: f(x) = ceil(x) + (1 if x > 0 else -1).
    import math
    out = []
    for x in probe.get("x", []):
        try:
            c = math.ceil(x)
            out.append(c + (1 if x > 0 else -1))
        except Exception:
            out.append(None)
    return {"y": out}
