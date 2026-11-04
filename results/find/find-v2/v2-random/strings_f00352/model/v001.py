def predict(probe):
    # f appends "T" to the input string [E1]
    # (all six inputs in E1 got exactly "T" appended, including digits,
    #  spaces, mixed case, and long sentences)
    return {"outputs": [x + "T" for x in probe["inputs"]]}
