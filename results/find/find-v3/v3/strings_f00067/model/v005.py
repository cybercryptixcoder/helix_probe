def predict(probe):
    # Reverse each whitespace-separated word, join with single spaces. [E1-E5]
    # Strip leading/trailing whitespace first. [E2, E3, E5]
    # Duplicate the last character of the last word (prepend to its reversal),
    #   UNLESS the last word is entirely uppercase (last.isupper()). [E1-E5]
    #   - "bananaUPPER"->no dup; "hello WORLD"->no dup; "abc def GHI"->no dup [E1,E2]
    #   - "Zebra"->dup; "aMiXeD"->dup (mixed case, not all-upper); "data"->dup [E1,E5]
    # Dup applies to last word only, regardless of repeats. [E4]
    outs = []
    for s in probe.get("inputs", []):
        t = s.strip()
        if t == "":
            outs.append("")
            continue
        words = t.split()
        rev = [w[::-1] for w in words]
        last = words[-1]
        if last and not last.isupper():
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
