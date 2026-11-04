def predict(probe):
    # Insert '4' at index floor(len/2) [E1, E2]
    # Increment last char by 1 only if it is a lowercase letter a-y [E1, E2]
    #   'Z' -> 'A' (wrap within uppercase) [E2: "Z"->"4A"]
    #   digits, spaces, punctuation unchanged [E1: "abc123", E2: "9"," ","a1"]
    #   'z' -> 'a'? unknown; assume wrap within lowercase [E2 'Z'->'A' suggests wrap]
    def f(s):
        n = len(s)
        pos = n // 2
        t = s[:pos] + "4" + s[pos:]
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                t = t[:-1] + ('a' if c == 'z' else chr(ord(c) + 1))
            elif 'A' <= c <= 'Z':
                t = t[:-1] + ('A' if c == 'Z' else chr(ord(c) + 1))
        return t
    return {"outputs": [f(x) for x in probe["inputs"]]}
