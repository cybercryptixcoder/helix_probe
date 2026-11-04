def predict(probe):
    # Rule: output is the input string reversed [E1, E2]
    #   "abc123"->"321cba", "level"->"level", " Zebralower"->"rewolarbeZ",
    #   "Hello World function lazy"->"yzalnoitcnufdlroWolleH", "bananaUPPER"->"REPPUananab",
    #   "Zebra"->"arbeZ", "Example123"->"321elpmaxE", "lazy"->"yzal", "banana"->"ananab"
    # Rule: spaces are removed from the output [E2]
    #   "test case"->"esactset" (not "esac tset"), "banana data banana "->"ananabatadananab"
    #   (not " ananab atad ananab"). Note: E1 " Zebralower"->"rewolarbeZ" is consistent
    #   with either reversal-then-strip or strip-then-reversal (leading space gone either way).
    #   "Hello World function lazy"->"yzalnoitcnufdlroWolleH" also has spaces removed.
    # ? Order: strip spaces first, then reverse (equivalent for these cases).
    return {"outputs": [s.replace(" ", "")[::-1] for s in probe["inputs"]]}
