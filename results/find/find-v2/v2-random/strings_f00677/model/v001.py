def predict(probe):
    # f(x) = x + "xI" for every input tested [E1]
    # No dependence on content observed: digits, spaces, case, words all get same suffix [E1]
    return {"outputs": [x + "xI" for x in probe["inputs"]]}
