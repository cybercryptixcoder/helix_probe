import math

def predict(probe):
    # y = floor(x - 39) [E1: all 10 points match exactly]
    # ? only one experiment; region-specific behavior not yet observed
    out = []
    for x in probe["x"]:
        try:
            out.append(math.floor(x - 39))
        except Exception:
            out.append(None)
    return {"y": out}
