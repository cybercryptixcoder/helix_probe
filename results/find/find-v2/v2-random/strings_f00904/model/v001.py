def predict(probe):
    # Reverses the entire string character by character [E1]
    # Evidence: "abc123"->"321cba", " Zebralower"->"rewolarbeZ ",
    # "Hello World function lazy"->"yzal noitcnuf dlror olleH",
    # "bananaUPPER"->"REPPUananab", "Zebra"->"arbeZ"
    # "level" is a palindrome so reversal is invisible [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
