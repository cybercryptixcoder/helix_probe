def predict(probe):
    # Rule: each char shifted +1 (ord+1) [E1,E2,E3]
    # Then: first char of string -> uppercase if it's a letter [E1 "Hello"->"Ifmmp", E3 "aMiXeD"->"Bnjyfe"]
    #       all other chars -> lowercase if it's a letter [E3 "Hello"->"ifmmp", "World"->"xpsme"; E1 "bananaUPPER"->"vqqfs"]
    # Non-letters just get +1 (space->!, Z->[ or {, digits +1) [E1 "Zebra"->"[fcsb", " Zebralower"->"!{fcsbmpxfs"]
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("")
            continue
        r = []
        for i, c in enumerate(s):
            n = chr(ord(c) + 1)
            if 'a' <= n <= 'z' or 'A' <= n <= 'Z':
                if i == 0:
                    n = n.upper()
                else:
                    n = n.lower()
            r.append(n)
        out.append("".join(r))
    return {"outputs": out}
