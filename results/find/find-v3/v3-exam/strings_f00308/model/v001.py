def predict(probe):
    # Removes all spaces from input [E1: "Hello World function lazy" -> "HelloWorldfunctionlazy"]
    # Leading space also removed [E1: " Zebralower" -> "Zebralower"]
    # Everything else unchanged [E1: "abc123", "level", "bananaUPPER", "Zebra"]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
