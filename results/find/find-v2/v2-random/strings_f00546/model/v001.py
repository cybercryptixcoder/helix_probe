def predict(probe):
    # Reverse the string, then prepend "lmKA" [E1]
    # Evidence: "abc123" -> "lmKA321cba", "level" -> "lmKAlevel",
    # " Zebralower" -> "lmKArewolarbeZ", "bananaUPPER" -> "lmKAREPPUananab",
    # "Zebra" -> "lmKAarbeZ" [E1]
    # "Hello World function lazy" -> "olleH dlroW noitcnuf lmKAyzal" [E1]
    #   -> note: only the LAST word "lazy" was reversed to "yzal" and moved
    #      to the end, while the rest "Hello World function" reversed as a
    #      whole to "olleH dlroW noitcnuf". Actually the whole string reversed
    #      is "yzal noitcnuf dlroW olleH"; observed is
    #      "olleH dlroW noitcnuf lmKAyzal". This equals: reverse whole string
    #      then... let's check: reverse("Hello World function lazy") =
    #      "yzal noitcnuf dlroW olleH". Observed = "olleH dlroW noitcnuf lmKAyzal".
    #      That is reverse of each word individually? reverse each word:
    #      "olleH" "dlroW" "noitcnuf" "yzal" -> "olleH dlroW noitcnuf yzal",
    #      then prepend lmKA before last word: "olleH dlroW noitcnuf lmKAyzal".
    #      Yes! So: reverse each word, keep word order, insert "lmKA" before
    #      the last word. But single-word cases: "abc123" -> reverse word
    #      "321cba", insert lmKA before last (only) word -> "lmKA321cba". ✓
    #      "level" -> "level", "lmKAlevel" ✓
    #      " Zebralower" -> words ["", "Zebralower"]? reverse each: "" and
    #      "rewolarbeZ". Insert lmKA before last word: " lmKArewolarbeZ"?
    #      Observed "lmKArewolarbeZ" (no leading space). Hmm.
    #      Maybe split on spaces, reverse each word, join, then insert lmKA
    #      before last word. " Zebralower".split(" ") = ["", "Zebralower"],
    #      reversed each = ["", "rewolarbeZ"], join = " rewolarbeZ",
    #      insert before last word -> " lmKArewolarbeZ". Observed lacks space.
    #      Alternative: reverse whole string, then... reverse(" Zebralower")
    #      = "rewolarbeZ " -> observed "lmKArewolarbeZ". 
    #      Let's reconsider: maybe it reverses the whole string and prepends
    #      lmKA, EXCEPT multi-word where it reverses each word?
    #      Check "Hello World function lazy": whole reverse = "yzal noitcnuf
    #      dlroW olleH". Observed "olleH dlroW noitcnuf lmKAyzal". Not that.
    #      Per-word reverse + lmKA before last word fits all multi-word.
    #      For " Zebralower": per-word reverse gives " rewolarbeZ", then lmKA
    #      before last word "lmKArewolarbeZ" but with leading space -> " lmKArewolarbeZ".
    #      Observed "lmKArewolarbeZ". So leading empty word dropped.
    #      Rule: split on whitespace (dropping empties), reverse each word,
    #      join with single space, insert "lmKA" before the last word.
    #      Check "Hello World function lazy": words reversed joined =
    #      "olleH dlroW noitcnuf yzal", insert lmKA before last -> 
    #      "olleH dlroW noitcnuf lmKAyzal" ✓
    #      "abc123" -> "321cba", insert before last (only) -> "lmKA321cba" ✓
    #      "bananaUPPER" -> "REPPUananab" -> "lmKAREPPUananab" ✓
    #      "Zebra" -> "arbeZ" -> "lmKAarbeZ" ✓
    #      "level" -> "level" -> "lmKAlevel" ✓
    #      " Zebralower" -> words ["Zebralower"] -> "rewolarbeZ" -> "lmKArewolarbeZ" ✓
    # So: split on whitespace, reverse each word, join by space, prepend "lmKA"
    # to the last word (or to the whole if single word).
    try:
        s = probe["inputs"]
    except Exception:
        return {"outputs": []}
    outs = []
    for x in s:
        try:
            words = x.split()
            if not words:
                outs.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            rev[-1] = "lmKA" + rev[-1]
            outs.append(" ".join(rev))
        except Exception:
            outs.append("")
    return {"outputs": outs}
