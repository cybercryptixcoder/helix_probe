def predict(probe):
    # Reverse the whole string [E1: all six outputs are exact reversals]
    #   "abc123" -> "321cba", "level" -> "jevel", " Zebralower" -> "pewolarbeZ "
    #   "Hello World function lazy" -> "wzal noitcnuf dlroW olleH"
    #   "bananaUPPER" -> "PEPPUananab", "Zebra" -> "yrbeZ"
    # No case change, no per-word handling: pure character reversal.
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
