def predict(probe):
    # Beliefs about the mechanism:
    # 1. Every character is lowercased [E1-E6: "ABC DEF"->"Abc def", "HELLO world"->"Hello world"]
    # 2. The first character is uppercased if it is a letter (Python str.capitalize semantics)
    #    [E1 "abc123"->"Abc123"; E2 " hello"->" hello" (space blocks); "1ABC"->"1abc" (digit blocks);
    #     "!Hello"->"!hello" (symbol blocks)]
    # 3. Trailing whitespace is removed first [E3 "banana "->"banana"; E4 "  mixed CASE  "->"  mixed case";
    #    E5 "Example "->"Example"]
    # 4. Leading whitespace is preserved [E2 " hello"->" hello", "  hello"->"  hello"; E4 " one two"->" one two"]
    # 5. Unicode letters capitalize per Python rules [E6 "ßeta test"->"Sseta test", "élan"->"Élan"]
    # 6. The whole thing is exactly s.rstrip().capitalize() [consistent with all evidence]
    # ? Whether rstrip removes only spaces or all whitespace is untested; assuming all whitespace.

    def f(s):
        return s.rstrip().capitalize()

    return {"outputs": [f(x) for x in probe["inputs"]]}
