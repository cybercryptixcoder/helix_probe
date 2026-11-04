def predict(probe):
    # Rule: output = 'k' + reverse(input)  [E1]
    # Evidence: every output in E1 is 'k' followed by the input reversed.
    #   "abc123" -> "k321cba", "level" -> "klevel", " Zebralower" -> "krewolarbeZ ",
    #   "Hello World function lazy" -> "kyzal noitcnuf dlroW olleH",
    #   "bananaUPPER" -> "kREPPUananab", "Zebra" -> "karbeZ"
    return {"outputs": ["k" + s[::-1] for s in probe["inputs"]]}
