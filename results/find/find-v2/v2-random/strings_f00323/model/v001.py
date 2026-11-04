def predict(probe):
    # Rule: output is the input string reversed [E1: all 6 outputs are exact reversals]
    #   "abc123"->"321cba", "level"->"level" (palindrome), " Zebralower"->"rewolarbeZ",
    #   "Hello World function lazy"->"yzalnoitcnufdlroWolleH", "bananaUPPER"->"REPPUananab", "Zebra"->"arbeZ"
    # No case change, no trimming, spaces preserved — pure reversal.
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
