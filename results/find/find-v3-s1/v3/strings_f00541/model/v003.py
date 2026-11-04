def predict(probe):
    # f strips all leading and trailing whitespace (spaces, tabs, newlines) [E4]
    #   "  hello" -> "hello", "\thello" -> "hello", "hello\t" -> "hello", "hello\n" -> "hello"
    # f removes all uppercase 'H' characters [E2]
    #   "Hello" -> "ello", "HHH" -> "", "AHBHC" -> "ABC", "hHHh" -> "hh"
    # Lowercase 'h' is untouched [E2]: "hHello" -> "hello"
    # Order: strip first, then remove H. "  Hello  " -> "ello" (strip -> "Hello" -> "ello") [E4]
    #   " H " -> "" (strip -> "H" -> ""), " H" -> "" [E4]
    def f(s):
        s = s.strip()
        s = s.replace("H", "")
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
