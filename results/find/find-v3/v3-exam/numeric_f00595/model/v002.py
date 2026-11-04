def predict(probe):
    # f(x) = floor(x) - 1 for x <= 0, and floor(x) + 1 for x > 0 [E2]
    # Equivalently: round away from zero, but always at least 1 away from x.
    # Evidence E2: -128->-129, -127.5->-129, -127.4->-129, -100.5->-102,
    #   -100.4->-102, -2.5->-4, -2.4->-4, -1.5->-3, -1.4->-3, -0.5->-2,
    #   0->-1, 0.5->1, 0.6->1, 1.5->2, 1.6->2, 2.5->3, 99.5->100,
    #   100.5->101, 127.5->128, 128->129.
    # E1: 88.2->89, 66.0->67, -20.3->-22, -61.7->-63, 2.9->3, -24.3->-26,
    #   72.7->73, -50.4->-52, -6.0->-7, 21.3->22.
    # Rule: for x>0, result = floor(x)+1; for x<=0, result = floor(x)-1.
    # Check: 88.2 -> 88+1=89 ✓; 66.0 -> 66+1=67 ✓; -20.3 -> -21-1=-22 ✓;
    #   -61.7 -> -62-1=-63 ✓; 2.9 -> 2+1=3 ✓; -24.3 -> -25-1=-26 ✓;
    #   72.7 -> 72+1=73 ✓; -50.4 -> -51-1=-52 ✓; -6.0 -> -6-1=-7 ✓;
    #   21.3 -> 21+1=22 ✓.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        fl = math.floor(x)
        if x > 0:
            out.append(float(fl + 1))
        else:
            out.append(float(fl - 1))
    return {"y": out}
