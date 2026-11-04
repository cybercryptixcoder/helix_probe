def predict(probe):
    # Shift every char's code point by +1 [E1, E2]
    # For LETTERS, case is normalized by position before shifting:
    #   first char -> uppercase, all later chars -> lowercase [E2]
    #   'a'->'B', 'A'->'b', 'z'->'[', 'Z'->'{' [E2]
    # Non-letters are just shifted, no case change: '1'->'2',' '->'!','@'->'A' [E1, E2]
    out = []
    for s in probe.get("inputs", []):
        try:
            r = []
            for i, c in enumerate(s):
                if c.isalpha():
                    t = c.upper() if i == 0 else c.lower()
                    r.append(chr(ord(t) + 1))
                else:
                    r.append(chr(ord(c) + 1))
            out.append("".join(r))
        except Exception:
            out.append(s)
    return {"outputs": out}
