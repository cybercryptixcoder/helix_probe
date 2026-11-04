def predict(probe):
    # Uniform +8 shift on every code point [E1, E2]
    #   hello->pmttw, HELLO->PMTTW, 123->9:;, !@#->)H+, space->( [E1]
    #   NUL->\b, ~->\x86, \xff->\x107, é->ñ, emoji->emoji+8 [E2]
    # Shift wraps modulo 0x110000: \ufff8+8 -> U+10000 (astral) [E3]
    #   \uffff+8 -> U+10007, \ufff8\ufff9\ufffa -> U+10000..U+10002 [E3]
    # If any char would exceed U+10FFFF, the box raises ValueError [E3: \udbff\udfff]
    # Lowercase 't' is deleted from input before shifting; equivalently '|' is
    #   removed from the shifted output (only 't'+8 == '|') [E6: "tab\there"->
    #   "ij\u0011pmzm", "Hi, there!"->"Pq4(pmzm)"; all other E6 outputs pure +8]
    # Empty string -> empty [E1]
    def shift(s):
        out = []
        for c in s:
            if c == 't':
                continue
            o = ord(c) + 8
            if o > 0x10FFFF:
                raise ValueError
            out.append(chr(o))
        return ''.join(out)
    results = []
    for x in probe["inputs"]:
        try:
            results.append(shift(x))
        except Exception:
            results.append("ERROR: ValueError")
    return {"outputs": results}
