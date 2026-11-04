def predict(probe):
    # f(x) = 141.0873*x + 1.1 for x > 0 [E1]
    # f(x) = null for x <= 0 [E1]
    # (slope from (1,1.1)->(2,142.1873): 141.0873; intercept 1.1-141.0873 = -139.9873)
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(141.0873 * x + 1.1)
        else:
            out.append(None)
    return {"y": out}
