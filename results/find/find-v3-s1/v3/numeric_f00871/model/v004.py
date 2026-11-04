def predict(probe):
    # Almost all outputs are 0.0/-0.0 [E1,E3,E5,E7,E9]
    # Nonzero region is a ramp: y = 5.2 - 2.5*x [E2,E4,E6]
    # Ramp is active for x in [-2.1, 2.0] [E10: x=-2.1 -> 10.45, x=-2.2 -> 0]
    #   At x=-2.1: 5.2 - 2.5*(-2.1) = 10.45 ✓ [E10]
    #   At x=-2.2: 5.2 + 5.5 = 10.7 but observed 0 -> cutoff at -2.1 [E10]
    #   At x=2.0: 0.2 ✓ [E8]; x=2.1: -0.05 ✓ [E8]
    # Just past x=2.1 (e.g. 2.2) y is 0 [E8] -> ramp ends at 2.1
    # Outside: 0.0 [E1,E4,E8,E10]
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}
