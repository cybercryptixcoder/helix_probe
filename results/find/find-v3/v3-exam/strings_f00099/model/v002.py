def predict(probe):
    # Reverses the string [E1: "abc123"->"321cba", "Zebra"->"arbeZ", "bananaUPPER"->"REPPUananab"]
    # "level" is a palindrome so reversal is invisible [E1]
    # Whitespace is stripped before reversing, not after [E2: "  spaces  "->"secaps  "]
    #   i.e. leading spaces removed, trailing spaces kept, then reverse.
    #   "  spaces  " -> strip leading -> "spaces  " -> reverse -> "  secaps" ... no.
    #   Observed "secaps  ": reverse of "  spaces" = "secaps  ". So trailing stripped, leading kept.
    # So: strip trailing whitespace, then reverse [E1 " Zebralower"->"rewolarbeZ " consistent]
    return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
