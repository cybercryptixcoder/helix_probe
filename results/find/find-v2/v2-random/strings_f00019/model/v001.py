def predict(probe):
    # Last char is replaced by the char before it in the alphabet [E1: level->levem, Zebra->Zebrb]
    #   Wait: level ends 'l'->'m' (next), Zebra ends 'a'->'b' (next). So last char -> next char.
    # "abc123" unchanged: last char '3' -> '4'? No, unchanged. So only letters shift.
    # " Zebralower" -> " Zebralowes": 'r'->'s' next letter. Yes.
    # "Hello World function lazy" -> "...lazz": 'y'->'z' next letter.
    # "bananaUPPER" -> "bananaUPPES": 'R'->'S' next letter (uppercase).
    # So: last character, if a letter, replaced by next letter (wrapping z->a, Z->A presumably).
    # Non-letter last char: unchanged (abc123).
    def shift(s):
        if not s:
            return s
        c = s[-1]
        if 'a' <= c <= 'z':
            c2 = 'a' if c == 'z' else chr(ord(c) + 1)
            return s[:-1] + c2
        if 'A' <= c <= 'Z':
            c2 = 'A' if c == 'Z' else chr(ord(c) + 1)
            return s[:-1] + c2
        return s
    return {"outputs": [shift(x) for x in probe["inputs"]]}
