def predict(probe):
    # First character shifted back by 2 in the alphabet, case preserved [E1,E2,E3,E4]
    # Wrap-around works for a,b,A,B [E5]
    # Non-letter first chars unchanged [E1,E2,E3,E4]
    # Accented/Unicode letters also shift by -2 (é->ç, É->Ç) [E5]
    # "JTQL" appended to every output [E1]
    def shift(c):
        if c.isalpha() and ord(c) < 128:
            if 'a' <= c <= 'z':
                return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
            if 'A' <= c <= 'Z':
                return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        # Unicode letters: shift code point by -2 (é->ç, É->Ç) [E5]
        if c.isalpha():
            return chr(ord(c) - 2)
        return c
    outs = []
    for s in probe["inputs"]:
        if s:
            s = shift(s[0]) + s[1:]
        outs.append(s + "JTQL")
    return {"outputs": outs}
