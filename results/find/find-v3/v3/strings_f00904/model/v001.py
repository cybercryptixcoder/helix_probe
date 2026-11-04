def predict(probe):
    # Reverse the string [E1: "abc123"->"321cba", "Zebra"->"arbeZ", " Hello World function lazy"->"yzal noitcnuf dlror olleH"]
    # Case is preserved (not swapped) [E1: "bananaUPPER"->"REPPUananab"]
    # Palindromes unchanged [E1: "level"->"level"]
    # Leading space moves to trailing after reversal [E1: " Zebralower"->"rewolarbeZ "]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
