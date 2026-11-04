def predict(probe):
    # f(x) = null for x <= 0 [E1]
    # f(x) = 141.0873*log2(x) + 1.1 for x > 0 [E1,E2,E3,E4,E5]
    #   check: x=0.001 -> 141.0873*(-9.96578)+1.1 = -1404.95 [E5]
    #   x=1 -> 1.1, x=2 -> 142.1873, x=128 -> 988.7111 [E1,E2]
    import math
    out = []
    for x in probe["x"]:
        try:
            if x <= 0:
                out.append(None)
            else:
                out.append(141.0873 * math.log2(x) + 1.1)
        except Exception:
            out.append(None)
    return {"y": out}
