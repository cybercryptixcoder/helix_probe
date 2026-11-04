def predict(probe):
    # Reverse the entire string, character by character [E1]
    # "abc123"->"321cba", "level"->"vel", " Zebralower"->"wolarbeZ",
    # "Hello World function lazy"->"oleH yzaitcnufdrW", "bananaUPPER"->"REPUnab", "Zebra"->"arbeZ"
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
