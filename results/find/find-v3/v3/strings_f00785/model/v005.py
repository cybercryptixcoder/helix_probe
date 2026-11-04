def predict(probe):
    # Rules inferred from evidence:
    # - Empty input returns "z" [E6]
    # - First character shifted +1 if letter, case-preserving, Z->A, z->a [E1,E2,E3,E5,E6]
    # - Non-letter first char unchanged [E6: "1","!"," "]
    # - If original string ends in 'y': no 'y' appended, last char unchanged [E4,E6]
    # - Otherwise append 'y' [E1,E2,E3,E5]
    def f(s):
        if s == "":
            return "z"
        chars = list(s)
        c = chars[0]
        if 'a' <= c <= 'z':
            chars[0] = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            chars[0] = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        res = ''.join(chars)
        if s.endswith('y'):
            return res
        return res + 'y'
    return {"outputs": [f(x) for x in probe["inputs"]]}
