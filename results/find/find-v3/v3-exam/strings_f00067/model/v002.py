def predict(probe):
    # Rule: split on spaces, reverse each word, double the first char of each
    # reversed word, rejoin with single spaces [E1, E2].
    #   "ab cd" -> "ba"+" "+"ddc"? wait: "cd"->"dc", double first -> "ddc" ✓
    #   "a b c" -> "a"+" "+"b"+" "+"cc" ✓
    #   "hello world" -> "olleh"+" "+"ddlrow" ✓
    #   "xy z" -> "yx"+" "+"zz" ✓
    #   "one two three" -> "eno"+" "+"owt"+" "+"eeerht" ✓
    #   "a"->"aa", "ab"->"bba", "abc"->"ccba", "a b"->"a bb" ✓
    #   "abc123"->"3321cba" ✓ (single word)
    #   "level"->"llevel" ✓, "Zebra"->"aarbeZ" ✓
    #   "bananaUPPER"->"RREPPUananab" ✓
    #   "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal" ✓
    #   " Zebralower" -> split(" ") gives ["","Zebralower"]; empty word -> ""?
    #     observed "rrewolarbeZ" (no leading space). So empty words dropped /
    #     leading space collapsed. Use split() (whitespace, drops empties) [E1].
    def g(w):
        r = w[::-1]
        return r[0] + r
    return {"outputs": [" ".join(g(w) for w in s.split()) for s in probe["inputs"]]}
