def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-2, 2]  [E1: x=-2->10.2, -1->7.7, 0->5.2, 1->2.7, 2->0.2]
    # f(x) = 0 outside [-2, 2]  [E1: all outer samples -> 0.0]
    # Boundary is exactly at x=-2 and x=2: at -2.1 -> 10.45 (on line), -1.99 -> 10.175 (on line)
    #   and 2.05 -> 0.075 (on line), 2.1 -> -0.05 (line goes negative, but observed -0.05!) [E2]
    # Wait: at x=2.1, line gives 5.2-5.25 = -0.05, observed -0.05. At x=2.2 line gives -0.3, observed -0.0.
    # So the line continues slightly past 2 but clipped at 0? At 2.05 -> 0.075 (line), 2.1 -> -0.05 (line, negative!),
    #   2.2 -> -0.0 (clipped to 0). So f = 5.2-2.5x on [-2, 2.1], then 0 beyond? Check -2.1: line gives 10.45, observed 10.45.
    #   -2.2: line gives 10.7, observed 0.0. So left boundary between -2.2 and -2.1.
    # Hmm, asymmetric. Let's reconsider: maybe f = max(0, 5.2-2.5x) but only on a window, and window is [-2.1, 2.1]?
    #   At -2.1: 10.45 (line). At -2.2: 0 (outside). At 2.1: -0.05 (line, negative). At 2.2: 0 (outside).
    #   But then at 2.05 -> 0.075 (line), 2.1 -> -0.05 (line). So on [-2.1, 2.1] use raw line (can be negative),
    #   outside -> 0. Check -2.05 -> 10.325 (line), -1.99 -> 10.175 (line). Consistent.
    #   Check E1: x=2 -> 0.2 (line), x=4 -> 0 (outside). x=-2 -> 10.2 (line). Consistent.
    #   So: f(x) = 5.2 - 2.5*x if -2.1 <= x <= 2.1 else 0.  [E1, E2]
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}
