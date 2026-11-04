def predict(probe):
    # Reverses the entire string character by character [E1, E2, E3]
    # Evidence: "abc123"->"321cba", " Zebralower"->"rewolarbeZ ",
    # "Hello World function lazy"->"yzal noitcnuf dlror olleH",
    # "bananaUPPER"->"REPPUananab", "Zebra"->"arbeZ"
    # "level" is a palindrome so reversal is invisible [E1]
    # E3 surprise: "function Hello World" -> "dlror olleH noitcnuf"
    #   Plain reversal would give "dlroW olleH noitcnuf".
    #   The observed output has "dlror" (r) instead of "dlroW" (W).
    #   This looks like the 'W' got mangled/replaced by 'r' in this case.
    #   Hypothesis (?): uppercase 'W' is transformed to 'r' before/after reversal.
    #   Check other evidence: "Hello World function lazy" -> "yzal noitcnuf dlror olleH"
    #   also shows "dlror" not "dlroW"! So 'W' -> 'r' consistently.
    #   "bananaUPPER" has no W. "world42" -> "24dlrow" (lowercase w unaffected).
    #   So rule: uppercase 'W' becomes 'r' (lowercase w stays w).
    def transform(s):
        s = s.replace("W", "r")
        return s[::-1]
    return {"outputs": [transform(s) for s in probe["inputs"]]}
