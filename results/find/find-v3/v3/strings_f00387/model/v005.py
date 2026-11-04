def predict(probe):
    # Rules inferred from evidence:
    # R1: Remove all lowercase 'm' characters (uppercase 'M' is kept) [E4, E6].
    # R2: If the first character (after m-removal) is alphabetic: capitalize it and
    #     lowercase all other alphabetic characters [E1, E2, E3, E5].
    # R3: If the first character is NOT alphabetic (space, digit, symbol, or empty):
    #     lowercase ALL alphabetic characters, no capitalization [E1, E2, E7].
    #     Evidence: " Zebralower"->" zebralower", "123 hello"->"123 hello",
    #     " hello"->" hello", "  apple..."->"  apple...", " Example"->" exaple",
    #     " functionend."->" functionend.".
    # R4: Non-letters pass through unchanged [E1, E2].
    def transform(s):
        s = s.replace("m", "")
        out = []
        cap_next = bool(s) and s[0].isalpha()
        for ch in s:
            if ch.isalpha():
                if cap_next:
                    out.append(ch.upper())
                    cap_next = False
                else:
                    out.append(ch.lower())
            else:
                out.append(ch)
        return "".join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
