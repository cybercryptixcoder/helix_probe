import math

def predict(probe):
    # y = floor(x - 39) fits all 10 points of E1 exactly [E1]
    # ? possible special interval not yet observed; no evidence for one yet
    out = []
    for x in probe["x"]:
        out.append(math.floor(x - 39))
    return {"y": out}
