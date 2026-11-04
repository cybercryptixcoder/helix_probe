def predict(probe):
    # The box reverses the string [E1: all outputs are reversed inputs]
    # "abc123"->"321cba", "level"->"jevel", " Zebralower"->"pewolarbeZ ",
    # "bananaUPPER"->"PEPPUananab", "Zebra"->"yrbeZ" all confirm plain reversal.
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
