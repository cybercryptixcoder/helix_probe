def predict(probe):
    # f(x) = max(0, 5.2 - x) for x in [-3, 3] roughly? Let's check [E2]
    # E2: x=-3 -> 0.0 ; -2 -> 10.2 ; -1 -> 7.7 ; -0.5 -> 6.45 ; -0.1 -> 5.45
    #     0 -> 5.2 ; 0.1 -> 4.95 ; 0.5 -> 3.95 ; 1 -> 2.7 ; 2 -> 0.2 ; 3 -> -0.0
    # Looks like y = 5.2 - x for x in [-2, 2]? Check: -2 -> 7.2 but observed 10.2. No.
    # Try y = 5.2 - x: 0->5.2 ok, 0.1->5.1 vs 4.95, 0.5->4.7 vs 3.95, 1->4.2 vs 2.7, 2->3.2 vs 0.2. Not linear.
    # Differences: 0->5.2, 0.1->4.95 (slope -2.5), 0.5->3.95 (slope -2.5 from 0.1? (4.95-3.95)/0.4=2.5)
    #   1->2.7 (slope (3.95-2.7)/0.5=2.5), 2->0.2 (slope (2.7-0.2)/1=2.5), 3->0 (slope 0.2/1=0.2)
    # So y = 5.2 - 2.5*x for x in [0,2], then 0 for x>=2? At x=2: 5.2-5=0.2 ok. x=3: 5.2-7.5=-2.3 -> clamped 0.
    # Negative side: 0->5.2, -0.1->5.45 (slope -2.5), -0.5->6.45 (slope (6.45-5.45)/0.4=2.5), -1->7.7 (slope 2.5), -2->10.2 (slope 2.5)
    #   -3->0.0 (would be 12.7, but observed 0). So negative side: y=5.2-2.5x for x in [-2,0], then 0 for x<=-2? At -2: 10.2 ok. -3: 0.
    # So f(x) = max(0, 5.2 - 2.5*x) for x in [-2, 2], and 0 outside? But E2 x=0.25 -> 4.575 = 5.2-0.625 ok.
    # Check E1: all x outside [-2,2] -> 0. Yes.
    # Check E3: x=1.2 -> 5.2-3=2.2 ok. Others outside -> 0. Yes.
    # So f(x) = max(0, 5.2 - 2.5*x) if -2 <= x <= 2 else 0.
    # Wait, at x=-2 gives 10.2, at x=2 gives 0.2, at x=3 gives 0 (outside). At x=-3 gives 0 (outside).
    # Boundary: inside [-2,2] use formula, outside 0. But at x=2 formula gives 0.2, at x=3 gives 0. 
    # Is it max(0, ...) everywhere? At x=3: 5.2-7.5=-2.3 -> max 0 = 0. At x=-3: 5.2+7.5=12.7 -> max 0 = 12.7, but observed 0.
    # So negative side is cut at -2. Positive side could be max(0,...) but at x=2.1 would be 5.2-5.25=-0.05->0. 
    # Need to test boundary. But simplest: f(x)=max(0,5.2-2.5x) for -2<=x, and 0 for x<-2.
    # Actually at x=-2 exactly 10.2. At x=-2.1? unknown. Let's assume interval [-2, 2] with formula, else 0.
    # But positive side: at x=2.5 formula gives -1.05 -> 0, consistent with 0. So could be x>=-2 with max(0,...).
    # Let's use: if x < -2: 0 else max(0, 5.2-2.5*x). This matches all data.
    # Check x=100 -> max(0, negative)=0 ok. x=-100 -> 0 ok.
    out = []
    for x in probe["x"]:
        if x < -2:
            out.append(0.0)
        else:
            v = 5.2 - 2.5 * x
            out.append(v if v > 0 else 0.0)
    return {"y": out}
