def predict(probe):
    # First char: next Unicode codepoint, case-preserving, Z->A wrap [E1, E2]
    #   Applies to any letter (Unicode-aware): é->ê, É->Ê, ü->ý, ß->à, α->β, ñ->ò, 日->旦 [E8]
    # Non-letter first char unchanged [E1: " Zebralower"]
    # Append "y" unless the ORIGINAL input already ends in "y" [E3, E4, E6]
    def transform(s):
        if not s:
            return "y"
        c = s[0]
        if c.isalpha():
            n = chr(ord(c) + 1)
            if c == 'z':
                n = 'a'
            elif c == 'Z':
                n = 'A'
        else:
            n = c
        out = n + s[1:]
        if not s.endswith("y"):
            out += "y"
        return out
    return {"outputs": [transform(x) for x in probe["inputs"]]}
