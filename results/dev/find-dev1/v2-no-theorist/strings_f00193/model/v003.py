def predict(probe):
    # Append "JTQL" to input, then shift the first character of the result back by 2 [E1-E8]
    # Wrap-around for a,b,A,B [E5]
    # Non-letter first chars unchanged [E1,E2,E3,E4,E7]
    # Unicode letters shift by -2 code points (é->ç, α->ί) [E5,E6]
    # Empty input -> "JTQL" -> "HTQL" [E8]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        if c.isalpha():
            return chr(ord(c) - 2)
        return c
    outs = []
    for s in probe["inputs"]:
        t = s + "JTQL"
        outs.append(shift(t[0]) + t[1:])
    return {"outputs": outs}
