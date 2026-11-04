def predict(probe):
    # Reverses the string [E1: "abc123"->"321cba", "Zebra"->"arbeZ", "bananaUPPER"->"REPPUananab"]
    # "level" is a palindrome so reversal is invisible [E1]
    # Leading space preserved at end after reversal [E1: " Zebralower"->"rewolarbeZ "]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
