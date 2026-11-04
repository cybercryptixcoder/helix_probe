def predict(probe):
    # y = floor(x) + sign(x)  [E1, E2, E3]
    #   x > 0: y = floor(x) + 1  (88.2->89, 66.0->67, 2.9->3, 103.0->104) [E1,E2,E3]
    #   x < 0: y = floor(x) - 1  (-20.3->-22, -6.0->-7, -102.2->-104) [E1,E3]
    #   x = 0: y = 0 (?) no direct evidence; sign(0)=0 assumed
    # No special interval found; rule holds across [-102, 124] [E1,E2,E3]
    import math
    out = []
    for x in probe["x"]:
        try:
            s = 1 if x > 0 else (-1 if x < 0 else 0)
            out.append(float(math.floor(x) + s))
        except Exception:
            out.append(None)
    return {"y": out}
