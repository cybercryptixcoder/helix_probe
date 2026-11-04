def predict(probe):
    # Split on whitespace, strip leading/trailing [E1,E2,E3]
    # Reverse each token in place, keep order [E1,E2,E3]
    # Join with single space [E2]
    # Prefix "lmKA" to the FIRST token, not last [E3: "banana data banana"->"ananab atad ananab lmKA"]
    # Wait: E3 shows "ananab atad ananab lmKA" = lmKA on LAST token
    # But E1 "Hello World function lazy"->"olleH dlroW noitcnuf lmKAyzal" = last token
    # E2 all show lmKA on last token
    # E3 "banana data banana "->"ananab atad ananab lmKA" = last token (trailing space stripped)
    # So lmKA on last token is correct. My v2 got E3 wrong on "banana data banana "
    # because split() gives ["banana","data","banana"], last is "banana"->"ananab", prefix->"lmKAananab"
    # but observed "ananab atad ananab lmKA" = "lmKA" appended AFTER last token reversed? No:
    # "ananab atad ananab lmKA" tokens: ananab, atad, ananab, lmKA -> lmKA is separate 4th token!
    # So when trailing space present, lmKA becomes its own token at end?
    # Check E2 "trail  "->"liart lmKA" : tokens liart, lmKA -> lmKA separate!
    # E2 "  lead"->"lmKAdael" : lmKA prefixed to lead (no trailing space)
    # E2 "one  two"->"eno lmKAowt" : lmKA prefixed to owt (no trailing space)
    # So: if input ends with whitespace, lmKA is appended as separate token; else prefixed to last token
    try:
        out = []
        for x in probe["inputs"]:
            words = x.split()
            if not words:
                out.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            if x != x.rstrip():
                rev.append("lmKA")
            else:
                rev[-1] = "lmKA" + rev[-1]
            out.append(" ".join(rev))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
