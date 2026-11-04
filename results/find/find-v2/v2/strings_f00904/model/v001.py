def predict(probe):
    # The box reverses the entire string [E1: "abc123"->"321cba", "Zebra"->"arbeZ",
    #   "Hello World function lazy"->"yzal noitcnuf dlror olleH",
    #   "bananaUPPER"->"REPPUananab", " Zebralower"->"rewolarbeZ "]
    # "level" is a palindrome, so reversal is consistent with it too [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
