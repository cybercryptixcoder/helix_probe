def predict(probe):
    # The box reverses each input string [E1: "abc123"->"321cba", "Zebra"->"arbeZ",
    #   "Hello World function lazy"->"yzal noitcnuf dlror olleH", "bananaUPPER"->"REPPUananab",
    #   " Zebralower"->"rewolarbeZ " (leading space becomes trailing space)]
    # "level" is a palindrome so reversal is invisible [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
