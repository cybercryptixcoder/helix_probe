def predict(probe):
    # f(x) = "k" + reverse(x)  [E1: all six inputs reversed and prefixed with 'k']
    #   "abc123" -> "k321cba", "level" -> "klevel" (palindrome), " Zebralower" -> "krewolarbeZ "
    #   "Hello World function lazy" -> "kyzal noitcnuf dlroW olleH", "bananaUPPER" -> "kREPPUananab", "Zebra" -> "karbeZ"
    return {"outputs": ["k" + s[::-1] for s in probe["inputs"]]}
