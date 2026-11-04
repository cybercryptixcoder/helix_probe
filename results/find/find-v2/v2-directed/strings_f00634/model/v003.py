def predict(probe):
    # Lowercase entire string [E1, E2]
    # Remove all whitespace (spaces, tabs, newlines) [E1, E3]
    # Uppercase only the very first character of the whole string, whatever it is [E1, E7]
    #   - "  spaced  " -> "spaced" (leading space removed, so 's' is first -> but observed "spaced" lowercase!)
    #   - "  hello there" -> "hellothere" (NOT "Hellothere") [E7]
    #   - "  a  b  " -> "ab" (NOT "Ab") [E3]
    # So: uppercase the first character only if the ORIGINAL string's first char is non-whitespace.
    #   Equivalently: strip leading whitespace first, then uppercase first char of the stripped string.
    #   "  spaced  " -> strip -> "spaced" -> "Spaced"? But observed "spaced". Contradiction!
    # Re-examine: E1 "  spaced  " -> "spaced" (lowercase s). E7 "  hello there" -> "hellothere" (lowercase h).
    #   So leading whitespace means NO capitalization at all.
    #   But "hello" -> "Hello" capitalizes. "123abc" -> "123abc" (first char digit, no change).
    # Rule: uppercase the first character of the raw string, then lowercase rest, then remove whitespace?
    #   "  spaced  ": first char is space -> upper(space)=space, then remove whitespace -> "spaced". ✓
    #   "  hello there": first char space -> stays, remove ws -> "hellothere". ✓
    #   "hello": 'h'->'H', -> "Hello". ✓
    #   "123abc": '1'->'1'. ✓
    #   "hello, World!": 'h'->'H', lower rest -> "Hello, world!", remove ws -> "Hello,world!". ✓
    # So: t = s[0].upper() + s[1:].lower(), then remove all whitespace.
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("")
            continue
        t = s[0].upper() + s[1:].lower()
        t = "".join(t.split())
        out.append(t)
    return {"outputs": out}
