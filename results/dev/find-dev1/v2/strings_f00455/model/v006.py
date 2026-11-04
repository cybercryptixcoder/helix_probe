def predict(probe):
    # Mechanism:
    # 1. Each character shifted +1 codepoint in a case region [E1,E2,E3,E9].
    # 2. First char uses UPPERCASE region; later chars use LOWERCASE region [E1,E6,E7].
    #    - "a"->"B", "A"->"B"; "hello"->"Ifmmp"; "1A"->"2b" [E1,E5]
    #    - non-ASCII letters same: "é"->"Ê", "aé"->"Bê" [E6,E7]
    # 3. Non-letters: +1 codepoint regardless of position [E5,E9].
    # 4. First char z/Z -> '[' (upper Z+1); later z/Z -> '{' (lower z+1) [E8,E9].
    # 5. Multi-char upper (ß->"SS", ﬁ->"FI", ﬂ->"FL"): first char of expansion
    #    upper+1, rest lower+1. "ß"->"Tt", "ﬁ"->"Gj", "ﬂ"->"Gm" [E10,E11].
    # 6. Titlecase chars (ǅ,ǈ,ǲ): first char -> raw codepoint +1 (NOT upper+1);
    #    later -> lower+1. "ǅ"->"ǆ", "aǅ"->"BǇ", "ǅa"->"ǆb" [E11].
    # 7. No wraparound; pure +1 [E9].

    def shift_first(c):
        if c.istitle() and not c.isupper():
            return chr(ord(c) + 1)
        if c.lower() != c.upper():
            u = c.upper()
            if len(u) == 1:
                return chr(ord(u) + 1)
            return chr(ord(u[0]) + 1) + "".join(chr(ord(x) + 1) for x in u[1:].lower())
        return chr(ord(c) + 1)

    def shift_later(c):
        if c.lower() != c.upper():
            l = c.lower()
            if len(l) == 1:
                return chr(ord(l) + 1)
            return "".join(chr(ord(x) + 1) for x in l)
        return chr(ord(c) + 1)

    s = probe.get("inputs", [])
    if not isinstance(s, list):
        s = [s]
    out = []
    for inp in s:
        if not isinstance(inp, str):
            inp = str(inp)
        res = []
        for i, ch in enumerate(inp):
            res.append(shift_first(ch) if i == 0 else shift_later(ch))
        out.append("".join(res))
    return {"outputs": out}
