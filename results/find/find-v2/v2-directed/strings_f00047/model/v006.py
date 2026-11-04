def predict(probe):
    # Mechanism: strip ALL trailing whitespace (spaces, tabs, newlines, CRs),
    # then apply case rule: first letter uppercased only if at index 0,
    # all other letters lowercased.
    #
    # Evidence:
    # - "hello" -> "Hello", "HELLO" -> "Hello" [E1,E2,E3]: first letter upper, rest lower.
    # - "McDonald" -> "Mcdonald", "iPhone" -> "Iphone" [E3]: only first letter capitalized.
    # - "Hello WORLD" -> "Hello world", "MiXeD CaSe" -> "Mixed case" [E6]: rest lowercased.
    # - "123abc" -> "123abc", "!abc" -> "!abc" [E2]: no leading letter at pos 0, unchanged
    #   (already lowercase).
    # - "123 ABC" -> "123 abc", "!FOO bar" -> "!foo bar", "9Lives" -> "9lives" [E6]:
    #   first letter not at pos 0 -> not capitalized, but rest lowercased.
    # - " hello" -> " hello", "  hello" -> "  hello" [E5,E7]: leading whitespace kept.
    # - "hello " -> "Hello", " hello " -> " hello", "  hello  " -> "  hello" [E4,E7]:
    #   trailing spaces stripped.
    # - "hello\t" -> "Hello", "hello\n" -> "Hello", "hello\r" -> "Hello",
    #   "hello\t " -> "Hello", "hello \t" -> "Hello" [E7]: ALL trailing whitespace
    #   stripped (tabs, newlines, CRs, mixed), not just spaces.
    # - "\thello" -> "\thello", "\nhello" -> "\nhello" [E7]: leading whitespace kept.
    # - "hello\tworld" -> "Hello\tworld" [E4]: internal whitespace preserved.
    #
    # Order: strip trailing whitespace, then apply case rule.

    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            s = s.rstrip()  # strip all trailing whitespace [E7]
            chars = list(s)
            first_letter_idx = None
            for i, c in enumerate(chars):
                if c.isalpha():
                    first_letter_idx = i
                    break
            result = []
            for i, c in enumerate(chars):
                if c.isalpha():
                    if i == first_letter_idx and i == 0:
                        result.append(c.upper())
                    else:
                        result.append(c.lower())
                else:
                    result.append(c)
            outputs.append("".join(result))
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
