def predict(probe):
    # Model of the black box f(x).
    #
    # Main idea: every character is shifted by +1 in its Unicode code point
    # (Caesar shift by 1), EXCEPT that a "Y" is inserted at a position that
    # depends on the string's length / structure.
    #
    # Evidence for +1 shift:
    #   "abc123" -> "bcdY234"   (a->b, b->c, c->d, 1->2, 2->3, 3->4)
    #   "level"  -> "mfYwfm"    (l->m, e->f, v->w, e->f, l->m)
    #   "Zebra"  -> "[fYcsb"    (Z->[, e->f, b->c, r->s, a->b)
    #   "zzz"    -> "{Y{{"      (z->{)
    #   "999"    -> ":Y::"      (9->:)
    #   "   "    -> "!Y!!"      (space->!)
    #   "ABCXYZ" -> "BCDYYZ["   (A->B,...,Y->Z, Z->[)
    # All characters shift up by exactly one code point. [E1-E6]
    #
    # Evidence for the inserted "Y":
    #   "abc123" (len 6) -> "bcdY234": Y inserted after 3 chars
    #   "level"  (len 5) -> "mfYwfm":  Y inserted after 2 chars
    #   "Zebra"  (len 5) -> "[fYcsb":  Y inserted after 2 chars
    #   "zzz"    (len 3) -> "{Y{{":    Y inserted after 1 char
    #   "999"    (len 3) -> ":Y::":    Y inserted after 1 char
    #   "   "    (len 3) -> "!Y!!":    Y inserted after 1 char
    #   "ab"     (len 2) -> "bYc":     Y inserted after 1 char
    #   "z"      (len 1) -> "Y{":      Y inserted after 0 chars
    #   "9"      (len 1) -> "Y:":      Y inserted after 0 chars
    #   "  "     (len 2) -> "!Y!":     Y inserted after 1 char
    #   "abcd"   (len 4) -> "bcYde":   Y inserted after 2 chars
    #   "abcde"  (len 5) -> "bcYdef":  Y inserted after 2 chars
    #   "abcdef" (len 6) -> "bcdYefg": Y inserted after 3 chars
    #   "xy"     (len 2) -> "yYz":     Y inserted after 1 char
    #   "xyzw"   (len 4) -> "yzY{x":   Y inserted after 2 chars
    #   "mnop"   (len 4) -> "noYpq":   Y inserted after 2 chars
    #   "QQ"     (len 2) -> "RYR":     Y inserted after 1 char
    #   "12"     (len 2) -> "2Y3":     Y inserted after 1 char
    #   "a1b2"   (len 4) -> "b2Yc3":   Y inserted after 2 chars
    # So insertion index = len(x) // 2 (integer division). [E1-E6]
    #
    # Check longer strings:
    #   "Hello World function lazy" (len 26) -> "Ifmmp!Xpsme!Ygvodujpo!mb{z"
    #     shifted: "Ifmmp!Xpsme!gvodujpo!mb{z", Y inserted at index 13.
    #     len//2 = 13. Matches.
    #   "Hello World" (len 11) -> "IfmmpY!Xpsme"
    #     shifted: "Ifmmp!Xpsme", Y at index 5. len//2 = 5. Matches.
    #   "banana data banana " (len 19) -> "cbobob!ebYub!cbobob!"
    #     shifted: "cbobob!ebub!cbobob!", Y at index 9. len//2 = 9. Matches.
    #   "racecar Example racecar" (len 23) -> "sbdfdbs!FybYnqmf!sbdfdbs"
    #     shifted: "sbdfdbs!Fybnqmf!sbdfdbs", Y at index 11. len//2 = 11. Matches.
    #   "Example123" (len 10) -> "FybnqYmf234"
    #     shifted: "Fybnqmf234", Y at index 5. len//2 = 5. Matches.
    #   "function Hello World" (len 20) -> "gvodujpo!IYfmmp!Xpsme"
    #     shifted: "gvodujpo!Ifmmp!Xpsme", Y at index 10. len//2 = 10. Matches.
    #
    # So: shift every char by +1, then insert "Y" at index len(x)//2.

    out = []
    for x in probe.get("inputs", []):
        shifted = "".join(chr(ord(c) + 1) for c in x)
        idx = len(x) // 2
        out.append(shifted[:idx] + "Y" + shifted[idx:])
    return {"outputs": out}
