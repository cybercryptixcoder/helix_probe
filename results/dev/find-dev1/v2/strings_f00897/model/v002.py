def predict(probe):
    # Model of f(x):
    # - Empty string -> empty string [E1]
    # - Each character is shifted by +2 or +4 depending on position/class.
    # - First char: +2 if letter (a-z, A-Z), else +4 [E1, E2]
    #     "a"->"c", "A"->"C", "z"->"~", "Z"->"^" (letters +2)
    #     "1"->"5", "!"->"%", " "->"$", "9"->"=", "~"->"\x82" (non-letters +4)
    # - All later chars: +4 [E1, E2]
    #     "ab"->"cf", "Hello"->"Jipps", "123"->"567", "a b"->"c$f"
    #     "ab1"->"cf5", "1ab"->"5ef", "a1b"->"c5f", "AB"->"CF", "aA"->"cE", "z z"->"~$~"
    # - Shift is plain ord+shift with no wraparound (e.g. "~"->"\x82") [E2]
    results = []
    for s in probe.get("inputs", []):
        r = ""
        for i, ch in enumerate(s):
            if i == 0 and ch.isalpha():
                r += chr(ord(ch) + 2)
            else:
                r += chr(ord(ch) + 4)
        results.append(r)
    return {"outputs": results}
