def predict(probe):
    # f(x) = x + 17.8 for x > 0 [E2: 0.1->17.8, 0.5->17.8, 1->17.8, 3->19.8, 10->26.8]
    # f(x) = x - 8.4 for x < 0 [E2: -0.5->-8.4, -0.1->-8.4, -1->-9.4, -3->-11.4, -10->-18.4]
    # f(0) = 2058.0 [E2: 0->2058.0] -- special value at exactly 0
    # E1 offsets: +17.6/+16.8/+17.1/+17.5 (pos), -8.1/-7.7/-8.0/-8.4 (neg) consistent
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
        elif x == 0:
            ys.append(2058.0)
        elif x > 0:
            ys.append(x + 17.8)
        else:
            ys.append(x - 8.4)
    return {"y": ys}
