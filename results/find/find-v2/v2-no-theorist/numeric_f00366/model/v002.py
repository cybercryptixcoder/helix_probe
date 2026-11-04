def predict(probe):
    # Output takes a few discrete values depending on x's sign and magnitude [E1, E2]
    # Positive x: -11.4 for small x (<=4), -12.4 for larger x (>=5) [E2, E1]
    #   E2: 0.1..4.0 -> -11.4; 5.0 -> -12.4
    #   E1: 21.3,66.0,72.7,88.2 -> -12.4; 2.9 -> -11.4
    # Negative x: 9.8 for small |x| (<=4), 8.8 for larger |x| (>=5) [E2, E1]
    #   E2: -0.1..-4.0 -> 9.8; -5.0 -> 8.8
    #   E1: -6.0,-20.3,-24.3,-50.4,-61.7 -> 8.8
    # Threshold appears to be around |x|=5 (between 4 and 5) [?]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(-11.4 if x < 5 else -12.4)
        else:
            out.append(9.8 if -x < 5 else 8.8)
    return {"y": out}
