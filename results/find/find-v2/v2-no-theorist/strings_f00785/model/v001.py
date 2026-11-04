def predict(probe):
    # First char -> next letter in alphabet, case-preserving, Z->A wrap [E1]
    # Non-letter first char unchanged [E1: " Zebralower"]
    # Append "y" to the end [E1]
    def transform(s):
        if not s:
            return "y"
        c = s[0]
        if 'a' <= c <= 'z':
            n = 'a' if c == 'z' else chr(ord(c) + 1)
        elif 'A' <= c <= 'Z':
            n = 'A' if c == 'Z' else chr(ord(c) + 1)
        else:
            n = c
        return n + s[1:] + "y"
    return {"outputs": [transform(x) for x in probe["inputs"]]}
