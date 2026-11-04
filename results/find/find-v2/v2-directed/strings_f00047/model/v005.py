def predict(probe):
    # Mechanism: capitalise the first *letter* of the string (uppercase it),
    # and lowercase every other letter in the string.
    #
    # Evidence:
    # - "hello" -> "Hello", "world" -> "World" [E1]: first letter upper, rest lower.
    # - "HELLO" -> "Hello", "hELLO" -> "Hello", "HeLLo" -> "Hello" [E2,E3]:
    #   everything after the first letter is lowercased.
    # - "McDonald" -> "Mcdonald", "iPhone" -> "Iphone" [E3]: only the FIRST
    #   letter is capitalized; later capitals are lowered.
    # - "Hello WORLD" -> "Hello world", "MiXeD CaSe" -> "Mixed case" [E6]:
    #   first letter upper, all remaining letters lower.
    # - "123abc" -> "123abc", "!abc" -> "!abc", "123 hello" -> "123 hello",
    #   "!hello world" -> "!hello world", "-abc" -> "-abc", "'hello" -> "'hello",
    #   "(hello)" -> "(hello)" [E2,E5]: if the string does not START with a
    #   letter, nothing is changed at all (no capitalization, no lowercasing).
    #   e.g. "123 ABC" -> "123 abc" [E6] shows lowercasing DOES happen when
    #   there's a leading letter... wait: "123 ABC" -> "123 abc" [E6].
    #
    # Re-examining: "123 ABC" -> "123 abc" [E6] but "123abc" -> "123abc" [E2]
    # and "123 hello" -> "123 hello" [E5]. So with digits first, later letters
    # ARE lowercased in E6 but NOT in E2/E5. The distinguishing factor:
    # "123 ABC" has an uppercase letter present; "123abc"/"123 hello" are
    # already lowercase. So the rule is: lowercase all letters except the
    # first letter; capitalize the first letter ONLY if it is the first
    # character of the string. If the first letter isn't at position 0,
    # it stays as-is but the rest are lowercased.
    #
    # Check: "!FOO bar" -> "!foo bar" [E6]: first char '!' not a letter, so
    # no capitalization, but "FOO" -> "foo" lowercased. Yes!
    # "!abc" -> "!abc" [E2]: already lowercase, unchanged. Consistent.
    # "9Lives" -> "9lives" [E6]: 'L' not at position 0, lowercased. Consistent.
    # "QQ" -> "Qq" [E6]: first letter at pos 0, capitalized, rest lower.
    #
    # So: lowercase every letter except keep the first letter uppercase IF
    # it occurs at index 0. Otherwise leave the first letter unchanged.
    #
    # - " hello" -> " hello" [E2,E4,E5]: leading space, first letter not at
    #   index 0, already lowercase, unchanged. Consistent.
    # - "hello " -> "Hello" [E4]: trailing space removed! " hello world " ->
    #   " hello world" [E4]: trailing space stripped, leading kept.
    # - "hello\tworld" -> "Hello\tworld" [E4]: tab preserved, not stripped.
    #   Only trailing spaces stripped? "hello " -> "Hello" (space gone).
    #   " hello world " -> " hello world" (one trailing space gone).
    #   So: strip trailing spaces (rstrip of spaces only), not tabs/newlines.
    # - "Hello\tWorld" -> "Hello\tworld" [E4]: lowercase after first letter
    #   across tabs too. Consistent with global lowercasing of non-first letters.
    #
    # Order of operations: strip trailing spaces, then apply case rule.
    # "hello " -> strip -> "hello" -> "Hello". Good.
    #
    # First letter definition: the first alphabetic character in the string.
    # It is uppercased only if it is at index 0; all other letters lowercased.
    # Non-letters unchanged.

    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            # Strip trailing spaces only [E4]
            s = s.rstrip(" ")
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
