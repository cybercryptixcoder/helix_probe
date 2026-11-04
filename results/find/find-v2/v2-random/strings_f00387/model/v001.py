def predict(probe):
    # Capitalize first letter, lowercase the rest [E1: abc123->Abc123, level->Level,
    #   " Zebralower"->" zebralower", "Hello World function lazy"->"Hello world function lazy",
    #   bananaUPPER->Bananaupper, Zebra->Zebra]
    # Leading space preserved; only first char of whole string is capitalized.
    return {"outputs": [s[:1].upper() + s[1:].lower() for s in probe["inputs"]]}
