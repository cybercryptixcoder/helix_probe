def predict(probe):
    # Reverses each input string [E1]
    #   "abc123" -> "321cba", "level" -> "level" (palindrome),
    #   " Zebralower" -> "rewolarbeZ " (space moves to end),
    #   "Hello World function lazy" -> reversed,
    #   "bananaUPPER" -> "REPPUananab", "Zebra" -> "arbeZ"
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
