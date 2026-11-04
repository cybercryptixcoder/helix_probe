def predict(probe):
    # Insert "10" at position len(s)//2 in every string [E1]
    # - "hello"(5) -> "He10llo" (pos 2) [E1]
    # - "HELLO"(5) -> "He10llo" (pos 2) [E1]
    # - "Hello World"(11) -> "Hello10 world" (pos 5) [E1]
    # - "12345"(5) -> "1210345" (pos 2) [E1]
    # - "a1b2c3"(6) -> "A1b102c3" (pos 3) [E1]
    # - "!@#$%"(5) -> "!@10#$%" (pos 2) [E1]
    # - "  spaces  "(10) -> "  spa10ces  " (pos 5) [E1]
    # - ""(0) -> "10" (pos 0) [E1]
    # - "x"(1) -> "10x" (pos 0) [E1]
    # - long sentence -> insert at midpoint [E1]
    # Also: uppercase letters appear lowercased in output [E1: HELLO->He10llo, a1b2c3->A1b102c3]
    #   Actually "HELLO"->"He10llo": H stays upper, ELLO lowercased? "Hello" is title-case.
    #   "a1b2c3"->"A1b102c3": 'a'->'A' (first char uppercased), rest unchanged.
    #   Hypothesis: capitalize first letter (title-case first char), lowercase rest? 
    #   "Hello World"->"Hello10 world": W->w lowercased. Consistent with: first char upper, rest lower.
    #   "!@#$%" unchanged case-wise (no letters). "  spaces  " -> "  spa10ces  " (already lower).
    #   "The quick..." -> "The quick..." first char T upper, rest lower already.
    # So: s2 = s[0].upper() + s[1:].lower() if s else s; then insert "10" at len(s)//2.
    # ? Insertion position uses original length (same as transformed length).
    out = []
    for s in probe.get("inputs", []):
        if s:
            t = s[0].upper() + s[1:].lower()
        else:
            t = s
        p = len(s) // 2
        out.append(t[:p] + "10" + t[p:])
    return {"outputs": out}
