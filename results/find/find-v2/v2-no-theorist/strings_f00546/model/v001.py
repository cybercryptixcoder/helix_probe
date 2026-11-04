def predict(probe):
    # Observations from E1:
    # - "abc123" -> "lmKA321cba": prefix "lmKA" + reversed input
    # - "level" -> "lmKAlevel": prefix "lmKA" + input (palindrome, reversal same)
    # - " Zebralower" -> "lmKArewolarbeZ": prefix + reversed input
    # - "Hello World function lazy" -> "olleH dlroW noitcnuf lmKAyzal"
    #     reversed whole string would be "yzal noitcnuf dlroW olleH"
    #     observed: "olleH dlroW noitcnuf lmKAyzal"
    #     -> words reversed in order, each word reversed? Let's check:
    #        words: Hello, World, function, lazy
    #        reversed word order: lazy function World Hello
    #        each reversed: yzal noitcnuf dlroW olleH
    #        observed: olleH dlroW noitcnuf lmKAyzal
    #     Hmm. Observed = "olleH dlroW noitcnuf lmKAyzal"
    #     Split observed by spaces: ["olleH","dlroW","noitcnuf","lmKAyzal"]
    #     That's each word reversed, in original order, except last word has "lmKA" prefix and reversed "lazy"->"yzal" giving "lmKAyzal".
    #     Wait: "olleH" = reverse("Hello"), "dlroW"=reverse("World"), "noitcnuf"=reverse("function"), "lmKAyzal" = "lmKA"+reverse("lazy").
    #     So: reverse each word, keep order, and prefix "lmKA" to the LAST word.
    # - "bananaUPPER" -> "lmKAREPPUananab": reverse = "REPPUananab", prefix lmKA. Single word -> prefix.
    # - "Zebra" -> "lmKAarbeZ": reverse + prefix.
    # So rule: split on spaces, reverse each word, join with spaces, prefix "lmKA" to the last word.
    # For single word: reversed word gets prefix.
    # Check "abc123": single word -> reverse "321cba", prefix -> "lmKA321cba". ✓
    # Check "level": reverse "level", prefix -> "lmKAlevel". ✓
    # Check " Zebralower": leading space. Split " Zebralower" by " " -> ["", "Zebralower"]. Reverse each: ["", "rewolarbeZ"]. Join: " rewolarbeZ". Prefix last word: " lmKArewolarbeZ"? But observed "lmKArewolarbeZ" (no leading space).
    # Hmm. Observed "lmKArewolarbeZ" - no leading space. So maybe strip? Or split differently.
    # If we strip leading/trailing spaces first: "Zebralower" -> reverse "rewolarbeZ" -> "lmKArewolarbeZ". ✓
    # But then "Hello World function lazy" has no leading space, fine.
    # Let's assume: strip input, split on spaces, reverse each word, join with single spaces, prefix "lmKA" to last word.
    # Edge: empty string? Unknown. Guess: return "lmKA".
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
