def predict(probe):
    # Reverses the entire string, character by character [E1]
    #   "apple" -> "clppa", "test case " -> " esac tset",
    #   "test caseMiXeD" -> "BeXiMesac tset", etc.
    # No case change, no word reordering: pure full-string reversal.
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
