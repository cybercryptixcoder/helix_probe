def predict(probe):
    # The box reverses each input string. [E1]
    # "abc123"->"321cba", "level"->"level" (palindrome), " Zebralower"->"rewolarbeZ ",
    # "Hello World function lazy"->"yzal noitcnuf dlroW olleH",
    # "bananaUPPER"->"REPPUananab", "Zebra"->"arbeZ". All are exact reversals. [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
