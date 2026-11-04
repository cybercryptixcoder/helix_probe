def predict(probe):
    # Rule: output = "lmKA" + reverse(input) [E1]
    # Evidence: "hello"->"lmKAolleh", "123"->"lmKA321", ""->"lmKA", " "->"lmKA"
    # Note: " " (single space) -> "lmKA" suggests spaces are stripped before processing
    # "a b c" -> "a b lmKAc": hmm, this looks like reverse of "c b a" = "a b c"? 
    #   Actually reverse("a b c") = "c b a", so "lmKA"+"c b a" would be "lmKAc b a"
    #   But observed is "a b lmKAc". That's odd.
    # "hello world" -> "olleh lmKAdlrow": reverse("hello world")="dlrow olleh"
    #   observed "olleh lmKAdlrow" = reverse("world")+" "+"lmKA"+reverse("hello")
    #   So it seems: reverse each word, and insert "lmKA" before... the last word? 
    #   "hello world": words ["hello","world"] -> "olleh" + " " + "lmKA" + "dlrow"
    #   "a b c": words ["a","b","c"] -> "a" + " " + "b" + " " + "lmKA" + "c"
    #   "hello": ["hello"] -> "lmKA"+"olleh"
    #   " " -> ["",""]? or stripped -> "" -> "lmKA"
    #   "" -> "lmKA"
    # So: reverse each word, join with spaces, but put "lmKA" before the LAST word.
    #   Equivalently: reverse words, then prefix last word with "lmKA".
    # Check "Hello World" -> "olleH lmKAdlroW" ✓ (reverse each: "olleH","dlroW")
    # "abc123" -> "lmKA321cba" ✓ single word
    # "hello!" -> "lmKA!olleh" ✓ single word
    # " " -> split gives ["",""], reversed ["",""], last prefixed -> " lmKA" ? 
    #   But observed "lmKA". So maybe strip first: " ".strip()="" -> "lmKA". 
    #   Or split() (no arg) on " " gives [] -> "lmKA". Let's use split() with no arg.
    #   But then "a b c".split() = ["a","b","c"] ✓
    #   "hello world".split() = ["hello","world"] ✓
    #   "" .split() = [] -> "lmKA" ✓
    #   " ".split() = [] -> "lmKA" ✓
    # Great: split() on whitespace, reverse each word, prefix last with "lmKA", join with " ".
    s = probe.get("inputs", [])
    out = []
    for x in s:
        words = x.split()
        if not words:
            out.append("lmKA")
        else:
            rev = [w[::-1] for w in words]
            rev[-1] = "lmKA" + rev[-1]
            out.append(" ".join(rev))
    return {"outputs": out}
