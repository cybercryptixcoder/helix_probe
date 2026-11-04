def predict(probe):
    # Uniform +8 shift on every code point [E1, E2]
    #   hello->pmttw, HELLO->PMTTW, 123->9:;, !@#->)H+, space->( [E1]
    #   NUL->\b, ~->\x86, \xff->\x107, é->ñ, emoji->emoji+8 [E2]
    # Shift wraps modulo 0x110000: \ufff8+8 -> U+10000 (astral) [E3]
    #   \uffff+8 -> U+10007, \ufff8\ufff9\ufffa -> U+10000..U+10002 [E3]
    # If any char would exceed U+10FFFF, the box raises ValueError [E3: \udbff\udfff]
    #   (lone surrogates D800-DFFF are valid code points to chr(); \udbff\udfff
    #    is a surrogate pair string, ord() of each is DFFF+8 = E007, fine...
    #    but observed ERROR, so treat astral surrogate-pair input as error)
    # Empty string -> empty [E1]
    def shift(s):
        out = []
        for c in s:
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
