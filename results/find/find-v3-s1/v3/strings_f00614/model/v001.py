def predict(probe):
    # Removes all spaces from input, then appends "F" [E1]
    # Evidence: "test case " -> "testcaseF", "data a Python " -> "dataaPythonF",
    # "Mississippi Hello World data" -> "MississippiHelloWorlddataF"
    return {"outputs": [s.replace(" ", "") + "F" for s in probe["inputs"]]}
