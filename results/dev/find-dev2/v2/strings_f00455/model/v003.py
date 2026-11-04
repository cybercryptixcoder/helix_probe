def predict(probe):
    # Core: for each char, first char -> uppercase (ß->"Ss"), rest -> lowercase,
    # then shift each resulting code point by +1 [E1-E12]
    # No wrapping at boundaries [E2: z->[ , 9->: , ~->DEL]
    # ß at first position -> "Tt" (i.e. "Ss"+1) [E12]
    # Non-ASCII letters shift by code point [E6,E9,E10,E12]
    out = []
    for s in probe["inputs"]:
        res = []
        for i, ch in enumerate(s):
            if i == 0:
                u = ch.upper()
                if u == "SS":  # ß case
                    u = "Ss"
                cased = u
            else:
                cased = ch.lower()
            for c in cased:
                res.append(chr(ord(c) + 1))
        out.append("".join(res))
    return {"outputs": out}
