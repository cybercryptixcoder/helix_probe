def predict(probe):
    # Reverse the string [E1, E2, E3]
    # Then swap case of each character [E1, E2, E3]
    # Wait: E1 "abc123" -> "321cba" (reverse, no case change since lowercase->lowercase?)
    #   Actually "abc123" reversed = "321cba", swapcase would give "321CBA". Observed "321cba".
    # E1 "level" -> "Level": reverse "level"="level", swapcase="LEVEL". Observed "Level".
    #   So only first char uppercased? "level" -> "Level" = capitalize.
    # E1 " Zebralower" -> "Rewolarbez ": reverse="rewolarbeZ ", swapcase="REWOLARBEz ". Observed "Rewolarbez ".
    #   That's capitalize of reversed: "rewolarbez " -> "Rewolarbez ".
    # E1 "Hello World function lazy" -> "Yzal noitcnuf dlrow olleh": reverse then capitalize.
    # E1 "bananaUPPER" -> "Reppuananab": reverse="REPPUananab", capitalize="Reppuananab". Yes!
    # E1 "Zebra" -> "Arbez": reverse="arbez", capitalize="Arbez". Yes.
    # E2 "a"->"A", "Z"->"Z", "1"->"1", "!"->"!", "ab"->"Ba", "aB"->"Ba", "Ab"->"Ba",
    #   "12"->"21", "a1"->"1a", "a b"->"B a". All consistent with reverse then capitalize.
    # E3 confirms: "Example123"->"321elpmaxe" (reverse "321elpmaxE", capitalize "321elpmaxe").
    # So: reverse, then capitalize (first char upper, rest lower).
    return {"outputs": [s[::-1].capitalize() for s in probe["inputs"]]}
