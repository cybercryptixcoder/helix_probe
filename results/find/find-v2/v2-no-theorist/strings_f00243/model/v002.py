def predict(probe):
    # Rule: remove ALL whitespace (spaces, tabs, newlines), then insert 'Z' at index len//2 [E1, E2]
    # Evidence: "a\tb" -> "aZb" (tab removed, not kept) [E2]
    # Evidence: "  lead" -> "leZad", "trail  " -> "trZail" (leading/trailing whitespace removed) [E2]
    # Evidence: "  " -> "Z" (all whitespace removed -> empty, Z at 0) [E2]
    # Evidence: "abc123" -> "abcZ123" (len6, pos3) [E1]
    # Evidence: "level" -> "leZvel" (len5, pos2) [E1]
    import re
    def f(s):
        s = re.sub(r"\s+", "", s)
        i = len(s) // 2
        return s[:i] + "Z" + s[i:]
    return {"outputs": [f(x) for x in probe["inputs"]]}
