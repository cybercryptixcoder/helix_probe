def predict(probe):
    # Model: split on whitespace, reverse each word, keep order, join with single space. [E1-E3]
    # Then prepend the last char of the last word to the reversed last word,
    # UNLESS that char is an uppercase letter. [E1, E2]
    # "hello world"->"olleh ddlrow" (d dup); "hello WORLD"->"olleh DDLROW" (D upper, no dup) [E2]
    # "hello world 123"->"olleh dlrow 3321" (3 dup); "abc def GHI"->"cba fed IIHG" (I upper) [E2]
    # "one two three!"->"eno owt !!eerht" (! dup); "Hello, World!"->",olleH !!dlroW" (! dup) [E2]
    # "banana data banana "->"ananab atad ananab": trailing space stripped, last word "banana"
    #   ends 'a' but NO dup -> so dup only when last char is NOT a letter? [E3]
    # Recheck: "world"->d dup (letter, lowercase) contradicts. So rule differs.
    # E3 "banana"->"aananab" (a dup) but "banana data banana"->"...ananab" (no dup).
    # Difference: multi-word vs single-word? "a b c"->"a b cc" dup, multi-word. Contradicts.
    # Difference: last word equals an earlier word? "banana data banana" has repeat.
    # "a b c" no repeat -> dup. "hello world" no repeat -> dup. "two  spaces" no repeat -> dup.
    # "banana data banana" repeat -> no dup. [E3]
    outs = []
    for s in probe.get("inputs", []):
        t = s.strip()
        if t == "":
            outs.append("")
            continue
        words = t.split()
        rev = [w[::-1] for w in words]
        last = words[-1]
        dup = last and not last[-1].isupper()
        if dup and words.count(last) > 1:
            dup = False
        if dup:
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
