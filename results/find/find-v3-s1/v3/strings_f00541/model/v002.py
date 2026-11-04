def predict(probe):
    # f removes all uppercase 'H' characters [E1, E2]
    #   "Hello" -> "ello", "HHH" -> "", "AHBHC" -> "ABC", "hHHh" -> "hh"
    # f removes trailing whitespace [E1]
    #   "test case " -> "test case", "data a Python " -> "data a Python"
    # Lowercase 'h' is untouched [E2]: "hHello" -> "hello", "h h H h" -> "h h  h"
    def f(s):
        s = s.rstrip()
        s = s.replace("H", "")
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
