def predict(probe):
    # The last character of the whole string is shifted +1 in Unicode code point [E1, E2, E4]
    # "hello"->"hellp", "world"->"worle", "abc"->"abd" [E1]
    # "Hello"->"Hellp", "HELLO"->"HELLP", "hELLo"->"hELLp" [E1]
    # "cat"->"cau", "Buzz"->"Buza" [E2]
    # "two words"->"two wordt", "a b c"->"a b d": only very last char [E1]
    # "test end."->"test end.", "dog."->"dog.", "hi!"->"hi!", "yes?"->"yes?" : last char punctuation, unchanged [E2]
    # "a1"->"a1", "abc123"->"abc123", "123"->"123" : last char digit, unchanged [E1, E2]
    # "1a"->"1b" : last char letter, shifted [E2]
    # "Z"->"A", "z"->"a" : wrap around within A-Z / a-z [E2]
    # "hello "->"hello ", "world."->"world.", "abc!"->"abc!", "cat1"->"cat1" : trailing non-letter unchanged [E3]
    # Accented letters shift by code point: "café"->"cafê", "über"->"übes", "Å"->"Æ", "ä"->"å", "ö"->"÷" [E4]
    # So: shift applies to any alphabetic char (Unicode), +1 code point; non-alphabetic last char unchanged [E4]
    # Wrap: only for ASCII z->a and Z->A [E2]; non-ASCII just +1 code point [E4]
    def shift(s):
        if not s:
            return s
        c = s[-1]
        if c == 'z':
            return s[:-1] + 'a'
        if c == 'Z':
            return s[:-1] + 'A'
        if c.isalpha():
            return s[:-1] + chr(ord(c) + 1)
        return s
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(shift(s))
        except Exception:
            out.append(s)
    return {"outputs": out}
