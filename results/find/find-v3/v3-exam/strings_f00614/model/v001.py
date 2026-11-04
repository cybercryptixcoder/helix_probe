def predict(probe):
    # Removes spaces and appends "F" [E1]
    # Evidence: "Hello World function lazy" -> "HelloWorldfunctionlazyF"
    #   (spaces removed, F appended); " Zebralower" -> "ZebralowerF"
    #   (leading space removed, F appended); all other inputs just get F.
    # Case is preserved [E1: "bananaUPPER" -> "bananaUPPERF", "Zebra" -> "ZebraF"]
    # Digits/symbols preserved [E1: "abc123" -> "abc123F"]
    return {"outputs": [s.replace(" ", "") + "F" for s in probe["inputs"]]}
