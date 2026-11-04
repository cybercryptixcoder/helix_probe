def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2, 0]  [E1: x=-2->10.2, -1->7.7, -0.5->6.45, 0->5.2]
    # f(x) = 5.2 - 2.5*x for x in [0, 2]   [E1: x=0.5->3.95, 1->2.7, 2->0.2] (same line, slope -2.5)
    # f(x) = 0 for x < -2 and x > 2         [E1: all outer samples -> 0.0]
    # So f(x) = max(0, 5.2 - 2.5*x) on [-2,2], else 0.  [E1]
    out = []
    for x in probe["x"]:
        if -2 <= x <= 2:
            out.append(max(0.0, 5.2 - 2.5 * x))
        else:
            out.append(0.0)
    return {"y": out}
