def predict(probe):
    # Observations [E1]:
    # - "hello" -> "Olleh": reverse the string, then uppercase the first letter
    #   (which was the last letter) and lowercase the rest? Let's check.
    #   "hello" reversed = "olleh". Output "Olleh": first char upper, rest lower.
    # - "world" -> "Dlrow": reversed "dlrow" -> "Dlrow". Yes.
    # - "Hello" -> "Olleh": reversed "olleH" -> "Olleh". First upper, rest lower.
    # - "HELLO" -> "Olleh": reversed "OLLEH" -> "Olleh". First upper, rest lower.
    # - "abc" -> "Cba": reversed "cba" -> "Cba".
    # - "ABC" -> "Cba": reversed "CBA" -> "Cba".
    # - "123" -> "321": reversed "321", no letters so unchanged case.
    # - "a1b2" -> "2b1a": reversed "2b1a", first char '2' not a letter.
    # - "two words" -> "Sdrow owt": reversed "sdrow owt" -> "Sdrow owt".
    # - "cat" -> "Tac": reversed "tac" -> "Tac".
    # Rule: reverse the string; then capitalize (first char upper, rest lower).
    #   Capitalize only affects letters; digits/symbols pass through.
    #   Python's str.capitalize() does exactly: first char upper, rest lower.
    def f(s):
        return s[::-1].capitalize()
    return {"outputs": [f(x) for x in probe["inputs"]]}
