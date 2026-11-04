def predict(probe):
    # First character: if it's a letter, shift to next letter, case preserved, wrapping z->a, Z->A [E1,E2,E3,E4]
    # First character: if it's NOT a letter (digit, symbol, space), leave it unchanged [E3,E4,E5]
    # Append 'y' to the end of every output, UNLESS the input already ends in 'y' [E1,E2,E3,E4,E8]
    #   "caty"->"daty" (not "datyy") [E8]
    #   The "ends in y" check is on the ORIGINAL input, not the shifted output [E9: "y"->"z" not "zy"]
    # Empty input: ""->"z" [E5]
    def f(s):
        if s == "":
            return "z"
        first = s[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') + 1) % 26 + ord('A'))
        out = first + s[1:]
        if not s.endswith("y"):
            out += "y"
        return out
    return {"outputs": [f(x) for x in probe["inputs"]]}
