def predict(probe):
    # Removes all spaces from the input string [E1]
    # Evidence: "test case " -> "testcase", "data a Python " -> "dataaPython",
    # "Mississippi Hello World data" -> "MississippiHelloWorlddata", "apple" -> "apple"
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
