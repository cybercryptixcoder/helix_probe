def predict(probe):
    # Observations from E1:
    # "abc123" -> "Abc123": first letter capitalized, rest unchanged
    # "level" -> "Level": first letter capitalized
    # " Zebralower" -> "zebralower": leading space removed, then... first letter lowercased?
    #   Actually " Zebralower" has space then 'Z'. Output "zebralower" = space removed, 'Z' lowercased.
    # "Hello World function lazy" -> "Helloworldfunctionlazy": spaces removed, and... 
    #   "Hello World function lazy" -> "Helloworldfunctionlazy"
    #   H-e-l-l-o W-o-r-l-d -> "Helloworld": 'W' lowercased, rest kept
    #   " function lazy" -> "functionlazy": 'f','l' kept lowercase
    #   So: remove spaces, and lowercase any char that follows a space? Or lowercase chars that were after spaces.
    # "bananaUPPER" -> "Bananaupper": first char uppercased, rest lowercased
    # "Zebra" -> "Zebra": unchanged (already capitalized)
    #
    # Hypothesis: 
    # 1. Remove all spaces.
    # 2. Capitalize first letter of result (uppercase first char, lowercase rest)?
    #    Check "bananaUPPER" -> "Bananaupper": yes, first upper, rest lower.
    #    Check "abc123" -> "Abc123": first upper, rest lower -> "Abc123" yes.
    #    Check "level" -> "Level": yes.
    #    Check " Zebralower" -> remove space -> "Zebralower" -> capitalize -> "Zebralower". 
    #      But observed "zebralower" (lowercase z)! Contradiction.
    #    Check "Hello World function lazy" -> remove spaces -> "HelloWorldfunctionlazy" -> capitalize -> "Helloworldfunctionlazy". Yes matches!
    #    Check "Zebra" -> "Zebra". Yes.
    #
    # So only " Zebralower" -> "zebralower" breaks the "capitalize" rule.
    # Maybe leading space causes lowercase? Or maybe the rule is: 
    #   capitalize first letter only if no leading space? 
    # Or: the first character of the *original* input determines case: if original first char is letter, capitalize it; if space, lowercase everything?
    # " Zebralower": original starts with space -> output all lowercase "zebralower". 
    #   But then "Hello World function lazy" starts with 'H' -> capitalize -> "Helloworldfunctionlazy" yes.
    #   "bananaUPPER" starts with 'b' -> capitalize -> "Bananaupper" yes.
    #   "abc123" -> "Abc123" yes.
    #   "level" -> "Level" yes.
    #   "Zebra" -> "Zebra" yes.
    #
    # Alternative: maybe it's title-case-ish? No, "Helloworldfunctionlazy" is not title case.
    #
    # Hypothesis: 
    #   s = input with all spaces removed
    #   if input starts with a space: return s.lower()
    #   else: return s[0].upper() + s[1:].lower()
    #
    # But wait, what about "bananaUPPER" -> "Bananaupper": s[1:].lower() = "ananaupper", yes.
    # "Hello World function lazy" -> s = "HelloWorldfunctionlazy", s[1:].lower() = "elloworldfunctionlazy", 
    #   result "Helloworldfunctionlazy" yes.
    #
    # What if input is empty or all spaces? Unknown. Guess: return "".
    # What if input starts with space but has uppercase later? " Zebralower" -> "zebralower" all lower. Consistent.
    #
    # What about digits/symbols first? Unknown. Guess: apply same rule (upper on first char is no-op for non-letters).
    #
    # Let me reconsider: maybe rule is simpler: 
    #   remove spaces, then if original had leading space -> lowercase all, else capitalize first.
    # That's what I have.
    #
    # Another thought: maybe it's "capitalize" but leading space makes it think it's a new word? 
    #   Like title()? "hello world" -> "Hello World" no, spaces removed.
    #
    # I'll go with the hypothesis. Mark uncertainty with ?.

    results = []
    for x in probe["inputs"]:
        s = x.replace(" ", "")
        if x.startswith(" "):
            out = s.lower()
        else:
            if s:
                out = s[0].upper() + s[1:].lower()
            else:
                out = ""
        results.append(out)
    return {"outputs": results}
