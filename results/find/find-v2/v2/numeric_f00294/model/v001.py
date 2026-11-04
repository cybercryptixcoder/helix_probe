def predict(probe):
    # f(x) = x + 17.6 [E1: 88.2->105.8 (+17.6), 66.0->82.8 (+16.8), -20.3->-28.4 (-8.1)...]
    # Wait: check offsets: 88.2->105.8 = +17.6; 66.0->82.8 = +16.8; -20.3->-28.4 = -8.1;
    # -61.7->-69.4 = -7.7; 2.9->19.8 = +16.9; -24.3->-32.4 = -8.1; 72.7->89.8 = +17.1;
    # -50.4->-58.4 = -8.0; -6.0->-14.4 = -8.4; 21.3->38.8 = +17.5
    # Offsets are +17 for positives, -8 for negatives => f(x) = x + 17.6 if x>=0 else x - 8.1
    # ? boundary near 0; use sign of x
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
        elif x >= 0:
            ys.append(x + 17.6)
        else:
            ys.append(x - 8.1)
    return {"y": ys}
