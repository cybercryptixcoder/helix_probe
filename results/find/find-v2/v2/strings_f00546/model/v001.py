def predict(probe):
    # Observations [E1]:
    # - "abc123" -> "lmKA321cba": reversed, then prefixed with "lmKA"
    # - "level" -> "lmKAlevel": palindrome, so reversed == same; prefixed
    # - " Zebralower" -> "lmKArewolarbeZ": reversed (space moved to end), prefixed
    # - "Hello World function lazy" -> "olleH dlroW noitcnuf lmKAyzal":
    #     only the LAST word "lazy" got reversed to "yzal" and prefixed with "lmKA";
    #     the rest "Hello World function " was reversed as a whole to
    #     "olleH dlroW noitcnuf " ... wait, check: reverse of "Hello World function "
    #     is " noitcnuf dlroW olleH". Observed is "olleH dlroW noitcnuf lmKAyzal".
    #     That's each word reversed individually, order preserved, and "lmKA"
    #     inserted before the last word.
    # - "bananaUPPER" -> "lmKAREPPUananab": single word reversed, prefixed
    # - "Zebra" -> "lmKAarbeZ": single word reversed, prefixed
    #
    # Refined rule: split on spaces. Reverse each word. Join with spaces.
    # Then insert "lmKA" immediately before the final word.
    # Check "Hello World function lazy":
    #   words reversed: "olleH dlroW noitcnuf yzal"
    #   insert lmKA before last word: "olleH dlroW noitcnuf lmKAyzal" ✓
    # Check "abc123": single word -> "321cba", insert before last -> "lmKA321cba" ✓
    # Check " Zebralower": words ["", "Zebralower"] -> reversed ["", "rewolarbeZ"]
    #   joined " rewolarbeZ", insert before last word -> " lmKArewolarbeZ"
    #   But observed is "lmKArewolarbeZ" (no leading space). Hmm.
    #   So leading space is dropped? Or split/join strips? Let's treat: strip
    #   leading/trailing spaces, then process. " Zebralower" -> "Zebralower"
    #   -> "lmKArewolarbeZ" ✓
    # Check "level": palindrome -> "level", prefix -> "lmKAlevel" ✓
    # Check "bananaUPPER": -> "REPPUananab", prefix -> "lmKAREPPUananab" ✓
    # Check "Zebra": -> "arbeZ", prefix -> "lmKAarbeZ" ✓
    #
    # Rule: strip outer spaces; split on single spaces; reverse each word;
    # join with single spaces; insert "lmKA" before the last word.
    # "?" unknown: multiple consecutive spaces, empty input, tabs/newlines.
    try:
        s = probe["inputs"]
        out = []
        for x in s:
            t = x.strip()
            if t == "":
                out.append("lmKA")
                continue
            words = t.split(" ")
            rev = [w[::-1] for w in words]
            rev[-1] = "lmKA" + rev[-1]
            out.append(" ".join(rev))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
