def predict(probe):
    # Reverse each whitespace-separated word, join with single spaces. [E1-E7]
    # Strip leading/trailing whitespace first. [E2, E3, E5, E7]
    # Duplicate the last character of the last word, prepended to its reversal. [E2,E4,E5,E6,E7]
    #   "abc def GHI"->"cba fed IIHG"; "aMiXeD"->"DDeXiMa"; "abc"->"cba" [E6,E5,E7]
    # Dup applies to last word only, regardless of repeats. [E4]
    # Dup does NOT apply when the stripped string is a single character? [E2: "a b c"->"a b cc" applies]
    #   Actually "abc" (single word) -> "cba" (no dup) [E7]. But "aMiXeD" single word -> "DDeXiMa" (dup).
    #   And "level"->"llevel", "banana"->"aananab", "lazy"->"yyzal" (single word, dup applies) [E3].
    #   So why "abc"->"cba" without dup? Hypothesis: dup only if last char is not... hmm.
    #   "abc" ends in 'c' (lowercase letter). "aMiXeD" ends 'D' (uppercase). "level" ends 'l'.
    #   Wait "level"->"llevel" dup applied, ends 'l'. "banana"->"aananab" dup, ends 'a'.
    #   So lowercase letter ending still dups for level/banana but not abc?
    #   Difference: "abc" is length 3. Hmm. Or maybe dup skipped when... let's check E7 "abc " -> "cba".
    #   E2 "a b c" -> "a b cc" (dup on 'c'). So single 'c' word dups, but "abc" doesn't.
    #   Maybe: dup applies only if the last word has length >= 4? level(5) yes, banana(6) yes, lazy(4) yes,
    #     aMiXeD(6) yes, abc(3) no, "c"(1) yes?? contradicts.
    #   Alternative: dup applies unless last word is all lowercase and length 3? Too ad hoc.
    #   Recheck E2 "a b c"->"a b cc": last word "c", dup -> "cc". length 1.
    #   So length isn't it. What distinguishes "abc" from "c","level","banana","lazy"?
    #   Hmm, maybe it's about the original string having trailing space? "abc " had trailing space.
    #   E5 "Example " -> "elpmaxE" (no dup!). "banana a data " -> "ananab a atad" (no dup on "data").
    #   E3 "banana data banana " -> "ananab atad ananab" (no dup).
    #   So: trailing whitespace in original => no dup! [E5,E7,E3]
    #   Check E2 "  leading and trailing  " -> "gnidael dna gniliart" no dup (trailing spaces). Yes!
    #   And "abc " -> "cba" no dup. Consistent!
    # So rule: if original string had trailing whitespace, no dup. Otherwise dup last char of last word.
    outs = []
    for s in probe.get("inputs", []):
        had_trailing = s != s.rstrip()
        t = s.strip()
        if t == "":
            outs.append("")
            continue
        words = t.split()
        rev = [w[::-1] for w in words]
        last = words[-1]
        if last and not had_trailing:
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
