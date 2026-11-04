def predict(probe):
    # Rule: each char shifted +1 (ord+1) [E1,E2,E3,E4,E5]
    # Then: first char of string -> uppercase if it's a letter [E1 "Hello"->"Ifmmp", E3 "aMiXeD"->"Bnjyfe"]
    #       all other chars -> lowercase if it's a letter [E3 "Hello"->"ifmmp", "World"->"xpsme"; E1 "bananaUPPER"->"vqqfs"]
    # Non-letters just get +1 (space->!, Z->[ or {, digits +1) [E1 "Zebra"->"[fcsb", " Zebralower"->"!{fcsbmpxfs"]
    # E5 "a!@#"->"B\"A$": after shift 'a'->'b' (upper 'B'), '!'->'"', '@'->'A', '#'->'$'.
    #   The '@'->'A' is a LETTER after shift, and it is at index 2, yet stays UPPERCASE.
    #   So the lowercase rule does NOT apply to non-alphabetic originals that become letters.
    #   Only original letters (a-z, A-Z) get case-normalized; other chars keep their shifted case.
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("")
            continue
        r = []
        for i, c in enumerate(s):
            n = chr(ord(c) + 1)
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
                if i == 0:
                    n = n.upper()
                else:
                    n = n.lower()
            r.append(n)
        out.append("".join(r))
    return {"outputs": out}
