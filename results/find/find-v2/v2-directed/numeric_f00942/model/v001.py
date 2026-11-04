import math

def predict(probe):
    # For x>0: y = -404.2*x - 154.8  [E1]
    # For x<0: y = -35.72*x - 17.1   [E1]
    # At x=0: y = -5401.17 (special point, matches neither branch)  [E1]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(-404.2 * x - 154.8)
        elif x < 0:
            out.append(-35.72 * x - 17.1)
        else:
            out.append(-5401.17)
    return {"y": out}
