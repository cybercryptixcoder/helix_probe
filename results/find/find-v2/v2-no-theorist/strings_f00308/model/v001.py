def predict(probe):
    # Removes spaces from input [E1: "Hello World function lazy" -> "HelloWorldfunctionlazy"]
    # Leading space also removed [E1: " Zebralower" -> "Zebralower"]
    # Other characters unchanged [E1: "abc123", "level", "bananaUPPER", "Zebra" unchanged]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
