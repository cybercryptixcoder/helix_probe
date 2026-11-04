import math

def predict(probe):
    # f(x) = 1.1 + 141.0873*log2(x) for x > 0 [E2,E4,E6]
    # f(x) undefined (null) for x <= 0 [E1,E3,E5 show negatives null; x=0 assumed null]
    # slope 141.0873 and intercept 1.1 fit all positive evidence exactly [E2,E4,E6]
    out = []
    for x in probe["x"]:
        if x is None or x <= 0:
            out.append(None)
        else:
            out.append(1.1 + 141.0873 * math.log2(x))
    return {"y": out}
