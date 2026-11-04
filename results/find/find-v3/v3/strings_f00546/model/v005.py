def predict(probe):
    # Split input on runs of ANY whitespace (spaces, tabs, newlines, \r, \xa0, etc.) [E8]
    #   "a\tb" -> ["a","b"], "a\r\nb" -> ["a","b"], "a\u00a0b" -> ["a","b"] [E8]
    # Leading/trailing whitespace yields one empty first/last word [E4, E7]
    # Reverse each word, keep order, insert "lmKA" before the last word [E1-E7]
    #   join reversed words[:-1] with " ", then " lmKA" + reversed last word [E4]
    #   strip a leading space (when first word empty) [E4 "  y" -> "lmKAy"]
    # Empty input -> "lmKA" [E4]
    import re
    out = []
    for s in probe.get("inputs", []):
        if s == "":
            out.append("lmKA")
            continue
        words = re.split(r'\s+', s)
        rev = [w[::-1] for w in words]
        res = " ".join(rev[:-1]) + " lmKA" + rev[-1]
        if res.startswith(" "):
            res = res[1:]
        out.append(res)
    return {"outputs": out}
