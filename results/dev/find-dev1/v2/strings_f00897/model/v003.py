def predict(probe):
    # Model of f(x):
    # - Empty string -> empty string [E1]
    # - First character: +2 regardless of class [E1, E3, E4]
    #     "a"->"c", "A"->"C", "1"->"5"? no: "1"->"5" is +4... check E1
    #     E1: "1"->"5" (+4), "!"->"%" (+4), " "->"$" (+4)
    #     E4: "@"->"B" (+2), "0"->"4" (+4), " "->"$" (+4), "!"->"%" (+4)
    #     So first char: letters +2, but digits/punct/space +4 EXCEPT "@"->"B" (+2)
    #     Hmm: E3 "@"->"B" (+2). E4 "@"->"B" (+2). So "@" is +2.
    #     Letters +2 [E1,E3,E4]. "@" +2 [E3,E4]. Digits/space/! +4 [E1,E4].
    # - Later chars: +4 uniformly [E1,E2,E3,E4]
    results = []
    for s in probe.get("inputs", []):
        r = ""
        for i, ch in enumerate(s):
            if i == 0 and (ch.isalpha() or ch == "@"):
                r += chr(ord(ch) + 2)
            else:
                r += chr(ord(ch) + 4)
        results.append(r)
    return {"outputs": results}
