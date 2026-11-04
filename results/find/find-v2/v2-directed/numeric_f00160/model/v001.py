def predict(probe):
    # f(x) = floor(x) - 39 [E1: all 20 points match floor(x-39)]
    import math
    return {"y": [math.floor(x) - 39 for x in probe["x"]]}
