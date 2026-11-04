def predict(probe):
    # f(x) = 0 for x <= -4 [E1, E2]
    # f(x) = 10.2 - x for -4 < x <= 0? Check: f(-2)=10.2, f(-1)=7.7, f(-0.5)=6.45, f(-0.1)=5.45, f(0)=5.2
    #   -2 -> 10.2, -1 -> 7.7 (diff 2.5), -0.5 -> 6.45, -0.1 -> 5.45, 0 -> 5.2
    # Looks like f(x) = 5.2 - 2.5*x for x in [-2, 0]: f(-2)=10.2, f(-1)=7.7, f(-0.5)=6.45, f(-0.1)=5.45, f(0)=5.2 ✓
    # f(x) = 5.2 - 2.5*x for 0 < x? f(0.1)=4.95, f(0.5)=3.95, f(1)=2.7, f(2)=0.2
    #   5.2-2.5*0.1=4.95 ✓, 5.2-2.5*0.5=3.95 ✓, 5.2-2.5*1=2.7 ✓, 5.2-2.5*2=0.2 ✓
    # So f(x) = 5.2 - 2.5*x for -2 <= x <= 2, and 0 outside [-2,2]? But f(-4)=0, f(-2)=10.2.
    # Wait f(-2)=10.2 but 5.2-2.5*(-2)=10.2 ✓. f(-4): 5.2-2.5*(-4)=15.2, but observed 0.
    # So the linear region is [-2, 2], zero outside. Check f(4)=0 ✓, f(8)=0 ✓.
    # But f(-2)=10.2 and f(2)=0.2 — asymmetric? 5.2-2.5*2=0.2 ✓, 5.2-2.5*(-2)=10.2 ✓. Consistent.
    # Hypothesis: f(x) = 5.2 - 2.5*x for -2 <= x <= 2, else 0.
    # Check E1: all |x|>2 except 2.9 (|2.9|>2) -> 0 ✓. -6.0 -> 0 ✓. All zero ✓.
    out = []
    for x in probe["x"]:
        if -2 <= x <= 2:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}
