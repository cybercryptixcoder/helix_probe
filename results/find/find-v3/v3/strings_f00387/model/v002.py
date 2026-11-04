def predict(probe):
    # Hypothesis: capitalize the first letter of the whole string only; lowercase everything else.
    # "Hello World function lazy" -> "Hello world function lazy" [E1]
    # "bananaUPPER" -> "Bananaupper" [E1]
    # "abc123" -> "Abc123", "level" -> "Level", "Zebra" -> "Zebra" [E1]
    # Leading space preserved: " Zebralower" -> " zebralower" [E1]
    # "hello world" -> "Hello world", "hello-world" -> "Hello-world" [E2]
    # "HELLO WORLD" -> "Hello world", "hELLo wORLd" -> "Hello world" [E2]
    # "123 hello" -> "123 hello" (no letter at start, nothing capitalized) [E2]
    # " hello" -> " hello" (leading space, first letter not capitalized) [E2]
    # So: uppercase the first alphabetic char of the string, lowercase all other alphabetic chars.
    def transform(s):
        out = []
        seen_letter = False
        for ch in s:
            if ch.isalpha():
                if not seen_letter:
                    out.append(ch.upper())
                    seen_letter = True
                else:
                    out.append(ch.lower())
            else:
                out.append(ch)
        return "".join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
