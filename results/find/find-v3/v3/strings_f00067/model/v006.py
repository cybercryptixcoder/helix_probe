def predict(probe):
    # Reverse each whitespace-separated word, join with single spaces. [E1-E6]
    # Strip leading/trailing whitespace first. [E2, E3, E5]
    # Always duplicate the last character of the last word (prepend to its reversal). [E2,E4,E5,E6]
    #   "hello WORLD"->"DDLROW"; "abc def GHI"->"IIHG"; "test 123"->"3321"; "aMiXeD"->"DDeXiMa" [E2,E5,E6]
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
        if last:
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
