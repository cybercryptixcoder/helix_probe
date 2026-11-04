def predict(probe):
    # Capitalize first letter, lowercase the rest [E1]
    # "abc123" -> "Abc123", "level" -> "Level", "bananaUPPER" -> "Bananaupper"
    # "Hello World function lazy" -> "Hello world function lazy"
    # " Zebralower" -> " zebralower" (leading space kept, first char is space so no change)
    # "Zebra" -> "Zebra"
    return {"outputs": [s[:1].upper() + s[1:].lower() for s in probe["inputs"]]}
