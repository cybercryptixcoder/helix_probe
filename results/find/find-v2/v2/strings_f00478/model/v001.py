def predict(probe):
    # Removes all spaces from the input string [E1]
    # " Zebralower" -> "Zebralower" (leading space removed)
    # "Hello World function lazy" -> "HelloWorldfunctionlazy" (all spaces removed)
    # Other inputs unchanged (no spaces present)
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
