def predict(probe):
    # Removes spaces from input [E1: "Hello World function lazy" -> "HelloWorldfunctionlazy"]
    # Removes leading spaces [E1: " Zebralower" -> "Zebralower"]
    # Otherwise returns input unchanged [E1: abc123, level, bananaUPPER, Zebra unchanged]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
