def predict(probe):
    # f(x) is null for x < 0 [E1: -20.3, -61.7, -24.3, -50.4, -6.0 all null]
    # f(x) is defined for x >= 0 [E1: 88.2, 66.0, 2.9, 72.7, 21.3 all non-null]
    # Values are large and grow with x; try a quadratic-ish fit [E1]
    # Points: (2.9,217.8175),(21.3,623.6874),(66.0,853.8872),(72.7,873.5674),(88.2,912.9058)
    # Looks like sqrt-like / concave. Try a*sqrt(x)+b or a*x^p+b.
    # Fit roughly: at x=2.9 ->217.8; x=88.2 ->912.9. Concave.
    # Try a*sqrt(x)+b: sqrt(2.9)=1.703, sqrt(88.2)=9.392.
    #   a*1.703+b=217.8; a*9.392+b=912.9 -> a=90.3, b=64.0
    # Check x=21.3: sqrt=4.615 -> 90.3*4.615+64=480.8 (obs 623.7) no.
    # Try a*x^p+b. Use two points and check.
    # (2.9,217.8),(88.2,912.9): ratio 912.9/217.8=4.19, x ratio 30.4 -> p=ln4.19/ln30.4=0.42
    # Check x=21.3: (21.3/2.9)^0.42=2.36 -> 217.8*2.36=514 (obs 623.7) no.
    # Maybe log: a*ln(x)+b: ln2.9=1.065, ln88.2=4.480. a*1.065+b=217.8; a*4.480+b=912.9
    #   a=203.4, b=1.2. Check x=21.3: ln=3.059 -> 203.4*3.059+1.2=623.4 (obs 623.7!) yes!
    # Check x=66: ln=4.190 -> 203.4*4.190+1.2=853.5 (obs 853.9) yes!
    # Check x=72.7: ln=4.286 -> 203.4*4.286+1.2=873.1 (obs 873.6) yes!
    # So f(x) = 203.4*ln(x) + 1.2 for x>0. Refine constants.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x is None or x <= 0:
                out.append(None)
            else:
                out.append(203.4 * math.log(x) + 1.2)
        except Exception:
            out.append(None)
    return {"y": out}
