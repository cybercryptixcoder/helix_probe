def predict(probe):
    # Hypothesis: capitalize first letter of each word, lowercase the rest.
    # "Hello World function lazy" -> "Hello world function lazy" [E1]
    # "bananaUPPER" -> "Bananaupper" [E1]
    # "abc123" -> "Abc123", "level" -> "Level", "Zebra" -> "Zebra" [E1]
    # Leading space preserved: " Zebralower" -> " zebralower" [E1]
    # So: title-case but only uppercase the first alpha of each word, lowercase rest.
    def transform(s):
        out = []
        prev_is_letter = False
        for ch in s:
            if ch.isalpha():
                if not prev_is_letter:
                    out.append(ch.upper())
                else:
                    out.append(ch.lower())
                prev_is_letter = True
            else:
                out.append(ch)
                prev_is_letter = False
        return "".join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
