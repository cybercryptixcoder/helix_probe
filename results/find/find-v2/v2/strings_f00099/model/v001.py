def predict(probe):
    # The box reverses each input string [E1]
    # "abc123" -> "321cba", "level" -> "level", " Zebralower" -> "rewolarbeZ "
    # "Hello World function lazy" -> "yzal noitcnuf dlroW olleH"
    # "bananaUPPER" -> "REPPUananab", "Zebra" -> "arbeZ"
    # All six outputs are exact reversals of their inputs.
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
