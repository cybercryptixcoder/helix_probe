def predict(probe):
    # f(x) = 5.2 - 2.5*x on a linear region [E2, E3, E4]
    # Left boundary: f(-2.1)=10.45 nonzero, f(-2.2)=0 [E4] -> region starts at -2.1 (or between -2.2 and -2.1)
    #   Note 5.2-2.5*(-2.1)=10.45 ✓, so linear formula holds at -2.1
    # Right boundary: f(2.01)=0.175 nonzero, f(2.1)=-0.05 nonzero, f(2.2)=0 [E4]
    #   At 2.1: 5.2-2.5*2.1 = -0.05 ✓; at 2.2: 5.2-2.5*2.2 = -0.3, but observed 0
    #   So right boundary is between 2.1 and 2.2; use 2.1 inclusive, else 0
    # Outside region: 0 [E1, E2, E3]
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}
