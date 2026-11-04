def predict(probe):
    # f(x) = x + "ny" for every input seen [E1]
    # No transformation of x itself observed; suffix "ny" appended [E1]
    return {"outputs": [x + "ny" for x in probe["inputs"]]}
