def predict(probe):
    # f(x) = null for x <= 0 [E1]
    # f(x) = 141.0873*x + 1.1 for 0 < x <= 1 [E1]
    # f(x) = 141.0873*log2(x) + 1.1 for x > 1 [E1, E2]
    #   check: x=2 -> 142.1873, x=128 -> 141.0873*7+1.1 = 988.7111 [E1,E2]
    #   x=96 -> 141.0873*log2(96)+1.1 = 141.0873*6.58496+1.1 = 930.15 [E2]
    import math
    out = []
    for x in probe["x"]:
        try:
            if x <= 0:
                out.append(None)
            elif x <= 1:
                out.append(141.0873 * x + 1.1)
            else:
                out.append(141.0873 * math.log2(x) + 1.1)
        except Exception:
            out.append(None)
    return {"y": out}
