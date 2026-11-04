def predict(probe):
    # Each letter is shifted forward by 1 in the alphabet, case preserved [E1]
    # Non-letters (digits, spaces, symbols) are unchanged [E1]
    # A trailing 'y' is appended to every output [E1]
    # 'z'/'Z' wraps to 'a'/'A' [E1: Zebra->Aebray, lazy->lazy? no: lazy->lazy+y? check]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    outs = []
    for s in probe.get("inputs", []):
        outs.append("".join(shift(c) for c in s) + "y")
    return {"outputs": outs}
