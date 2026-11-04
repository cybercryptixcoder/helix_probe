def predict(probe):
    # Removes all spaces from the input, then appends "F" [E1]
    #   "Hello World function lazy" -> "HelloWorldfunctionlazyF"
    #   " Zebralower" -> "ZebralowerF"
    # Other characters (digits, case, symbols) are left untouched [E1]
    return {"outputs": [s.replace(" ", "") + "F" for s in probe["inputs"]]}
