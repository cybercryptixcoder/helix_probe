import math

def predict(probe):
    # x=0 gives 2058.0 [E1]
    # x>0: y = ceil(x) + 16.8 [E1,E2,E3,E4,E6]
    # x<0: y = ceil(x) - 8.4 [E1,E2,E3,E4,E5,E6]
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(2058.0)
            elif x > 0:
                out.append(float(math.ceil(x)) + 16.8)
            else:
                out.append(float(math.ceil(x)) - 8.4)
        except Exception:
            out.append(None)
    return {"y": out}
