def predict(probe):
    # f reverses the whole string character by character [E1-E7]
    # Word order preserved, whitespace preserved exactly [E2, E4, E5, E7]
    # Punctuation is not a separator; just characters [E6]
    # Case preserved EXCEPT: capital 'W' becomes 'r' in the output [E8]
    #   "World"->"dlror", "WORLD"->"DLROr", "W"->"r", "Wow"->"wor", "Www"->"wwr"
    #   lowercase 'w' unaffected: "world"->"dlrow", "w"->"w" [E8]
    # So: reverse the string, then replace 'W' with 'r' in the result.
    def rev(s):
        return s[::-1].replace("W", "r")
    return {"outputs": [rev(s) for s in probe["inputs"]]}
