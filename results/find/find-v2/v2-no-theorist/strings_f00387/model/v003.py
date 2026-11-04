def predict(probe):
    # Capitalize first letter, lowercase the rest [E1, E2]
    # Drop 'm' from every word starting with "exam" (case-insensitive) [E3, E4]
    #   - "Example"->"Exaple", "Exam"->"Exa", "An example"->"An exaple", "Exam room"->"Exa roo" [E4]
    #   - "EXAMPLE"->"Example" (no drop): only lowercase 'm' after "exa" is dropped? [E4]
    #     Actually "EXAMPLE" lowercases to "example" then... it did NOT drop. So drop applies
    #     only to lowercase 'm' in the original? "Example" has lowercase m -> dropped.
    #     "EXAMPLE" has uppercase M -> not dropped. So: drop lowercase 'm' in words starting "exam" [E4]
    # Leading space preserved, no capitalization of first char if it's a space [E1, E2]
    import re
    def f(s):
        r = s[:1].upper() + s[1:].lower()
        # drop lowercase 'm' in words beginning with "exam" (after lowercasing, but only if original m was lowercase)
        # Work on original to detect case of m, but match word start case-insensitively
        def fix_word(m):
            w = m.group(0)
            # find position of 'm' in "exam" prefix
            if len(w) >= 4 and w[:4].lower() == "exam":
                if w[3] == 'm':  # lowercase m in original
                    return w[:3] + w[4:]
            return w
        # Apply to each word in original, but capitalization/lowercasing complicates.
        # Simpler: operate on original words, drop lowercase m, then apply case transform.
        words = re.split(r'(\s+)', s)
        out = []
        for w in words:
            if len(w) >= 4 and w[:4].lower() == "exam" and w[3] == 'm':
                w = w[:3] + w[4:]
            out.append(w)
        s2 = ''.join(out)
        r = s2[:1].upper() + s2[1:].lower()
        return r
    return {"outputs": [f(s) for s in probe["inputs"]]}
