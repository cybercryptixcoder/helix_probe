import math

def predict(probe):
    # Observations:
    # - For |x| >= ~0.8: y looks like a smooth oscillatory function of x,
    #   roughly bounded in [-1, 1]. Values: f(1)=0.16, f(2)=-0.84, f(4)=0.83,
    #   f(8)=-0.96, f(16)=-0.96, f(32)=-0.10, f(64)=0.61, f(100)=-0.26,
    #   f(127)=-0.77, f(-127)=0.64, f(-100)=1.0, f(-64)=0.72, f(-32)=-0.94,
    #   f(-16)=-0.29, f(-8)=0.14, f(-4)=0.04, f(-2)=-0.23, f(-1)=-0.63,
    #   f(0.9)=0.72, f(0.8)=-0.92, f(1.25)=-0.93, f(1.5)=-0.13, f(3)=-0.39,
    #   f(-0.5)=-0.39.  This is consistent with something like sin(a*x+b)
    #   with a ~ 0.5-1 and some phase; hard to pin down exactly. [E1, E2]
    # - For 0 < x < ~0.75: y is a large positive plateau ~13-14. [E2]
    # - For x <= 0 small (x=-0.01): y~6.7, x=-0.5: y~7.0 -> another plateau
    #   ~7 on the negative side near zero. [E2]
    # - At x=0: y=474.5, a huge spike. [E1]
    # Hypothesis: f(x) = g(x) + spike/plateau terms near zero.
    #   spike: A/x^2 or A/|x| near 0 (huge at 0, ~13 at 0.01-0.7 positive,
    #   ~7 at -0.01..-0.5).  Actually 1/x^2 at 0.01 = 10000, too big.
    #   Try A/(x^2+c): at x=0 -> A/c = 474.5; at x=0.01 -> ~13.4.
    #   A/(0.0001+c)=13.4 and A/c=474.5 -> c ~ 474.5*c... solve:
    #   A=474.5c; 474.5c/(0.0001+c)=13.4 -> 474.5c=13.4*0.0001+13.4c
    #   -> 461.1c=0.00134 -> c=2.9e-6, A=0.00138. Then at x=0.5:
    #   0.00138/0.25=0.0055, not 12.6. So not that.
    # Alternative: plateau is a separate term active in a window near 0.
    #   Positive window (0, ~0.75): +13; negative window [-0.5,0): +7;
    #   at exactly 0: +474.5.  And g(x) is the oscillatory part.
    # Let's estimate g from points outside windows: g(0.8)=-0.92, g(0.9)=0.72,
    #   g(1)=0.16, g(1.25)=-0.93, g(1.5)=-0.13, g(2)=-0.84, g(3)=-0.39.
    #   This looks like sin of something. Try g(x)=sin(k*x): sin(0.8k)=-0.92,
    #   sin(0.9k)=0.72 -> k~? sin(0.9k)=0.72 -> 0.9k~0.80 or 2.34; k~0.89 or 2.6.
    #   sin(0.8*2.6)=sin(2.08)=0.87 not -0.92. k~0.89: sin(0.71)=0.65 not -0.92.
    #   Try g(x)=sin(x^2 * c)? Hard. Given uncertainty, use a rough fit.
    # Given the difficulty, I'll model: g(x) = sin(x) * something? 
    #   sin(1)=0.84 vs 0.16. No.
    # Honestly the oscillatory part is not identifiable from these samples.
    # Best guess: g(x) = sin(0.9*x + phase) won't fit all. Use a smooth
    #   interpolation-free guess: g(x) = sin(x)*cos(x/3)? Just guess.
    # I'll go with g(x) = sin(x) * cos(x/2) type... let's just pick
    #   g(x) = sin(x) for |x|>=0.75 and hope. Actually check: sin(1)=0.84 vs 0.16.
    #   sin(2)=0.91 vs -0.84. sin(4)=-0.76 vs 0.83. Sign flipped-ish.
    #   -sin(x): -0.84 vs 0.16, -0.91 vs -0.84 (close!), 0.76 vs 0.83 (close!),
    #   -sin(8)=-0.99 vs -0.96 (close!), -sin(16)=-0.29 vs -0.96 (no).
    #   -sin(x) fits x=2,4,8 well. x=16: -sin(16)=0.29 vs -0.96. Hmm.
    #   -sin(x/2)? x=2: -sin(1)=-0.84 yes! x=4: -sin(2)=-0.91 vs 0.83 no.
    #   Try -sin(x) with period issues... 
    # Let's try g(x) = -sin(x): 
    #   x=0.8: -0.717 vs -0.92; x=0.9: -0.783 vs 0.72 (no).
    # The data is too sparse to identify. I'll use -sin(x) as best guess
    #   for the oscillatory part and mark with "?".
    # Windows: positive plateau for 0<x<0.75 (value ~13.2), negative plateau
    #   for -0.75<x<0 (value ~7), spike at x=0 (~474.5).
    # Boundary between plateau and oscillatory: at x=0.8 it's oscillatory
    #   (-0.92), at x=0.7 it's plateau (13.2). So boundary ~0.75. [E2]
    # At x=0.9 oscillatory (0.72). At x=-0.5 plateau (7.0). At x=-0.01 plateau
    #   (6.74). Where does negative plateau end? Unknown; assume symmetric ~0.75.
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            if v == 0:
                y = 474.5058
            elif 0 < v < 0.75:
                y = 13.2
            elif -0.75 < v < 0:
                y = 7.0
            else:
                y = -math.sin(v)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
