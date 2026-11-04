def predict(probe):
    # Removes all spaces from the input string [E1]
    # "Hello World function lazy" -> "HelloWorldfunctionlazy" [E1]
    # " Zebralower" -> "Zebralower" (leading space removed) [E1]
    # Other inputs unchanged (no spaces present) [E1]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}
