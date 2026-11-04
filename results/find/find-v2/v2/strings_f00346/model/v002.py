import re

def predict(probe):
    # Mechanism (from the evidence):
    # 1. All spaces are removed from the output [E2 "hello world"->"jelloworld", E3 "test case"->"vestcase", E4 "ab cd ef"->"cbcdef", E5 "banana a data "->"dananaadata"]
    # 2. A leading run of spaces is removed, and then the first non-space character is shifted [E4 " ab"->"cb", "  ab"->"cb", E6 "   abc"->"cbc", "  z"->"b"]
    # 3. The first character of the (space-stripped) string is shifted +1 in the alphabet, case preserved [E1 "abc123"->"cbc123", "Zebra"->"Bebra", E2 "abc"->"cbc", "Abc"->"Cbc", E3 "lazy"->"nazy", E4 "a b"->"cb"]
    #    Wait: "abc"->"cbc" means 'a'->'c' (+2), not +1. Check "Zebra"->"Bebra": Z->B is +2 (wrapping). "lazy"->"nazy": l->n is +2. "Example"->"Gxample": E->G +2. "test"->"vest": t->v +2. "world"->"yorld": w->y +2. "hello"->"jello": h->j +2. So shift is +2, case preserved, wrapping [E1,E2,E3,E4,E5].
    # 4. If the first char is not a letter (digit/symbol), no shift occurs [E2 "1abc"->"1abc", "!hello"->"!hello", E6 "123abc"->"123abc", "!!!abc"->"!!!abc", "9z"->"9z", "!!z"->"!!z"]
    # 5. Only the first character is shifted; the rest is unchanged (after space removal) [all evidence]
    # 6. Spaces inside are simply deleted, not shifted [E2 "hello  world"->"jelloworld", E4 "a-b"->"c-b" (only first char)]
    # 7. Leading spaces: stripped before finding the first character to shift [E4 " ab"->"cb", E6 "   abc"->"cbc"]
    # 8. Trailing spaces removed too [E3 "banana data banana "->"dananadatabanana"]
    # 9. Empty string -> empty string (no evidence, but safe) [?]

    def transform(s):
        # Remove all spaces
        t = s.replace(" ", "")
        if not t:
            return ""
        c = t[0]
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shifted = chr((ord(c) - base + 2) % 26 + base)
            return shifted + t[1:]
        else:
            return t

    return {"outputs": [transform(x) for x in probe["inputs"]]}
