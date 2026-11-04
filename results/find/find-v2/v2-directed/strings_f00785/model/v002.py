def predict(probe):
    # First character: if it's a letter, shift to next letter, case preserved, wrapping z->a, Z->A [E1,E2,E3,E4]
    #   "hello"->"iello", "zebra"->"aebray", "Z"->"Ay" [E1,E4]
    # First character: if it's NOT a letter (digit, symbol, space), leave it unchanged [E3,E4,E5]
    #   "123abc"->"123abcy", "!hello"->"!helloy", "  hello"->"  helloy" [E3,E4]
    # Last character: append 'y' to the end of every output [E1,E2,E3,E4,E5]
    # Empty input: treated as if first char is 'z' -> 'a'? No: observed ""->"z" [E5]
    #   So empty string: first-char rule applied to... produces "z" then append "y"? No, output is "z" only.
    #   ""->"z": looks like append 'y' would give "y", but got "z". Special: empty -> "z" [E5]
    # Everything else unchanged [E1,E2,E3,E4,E5]
    def f(s):
        if s == "":
            return "z"  # E5: empty input yields "z" (not "y")
        first = s[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') + 1) % 26 + ord('A'))
        return first + s[1:] + "y"
    return {"outputs": [f(x) for x in probe["inputs"]]}
