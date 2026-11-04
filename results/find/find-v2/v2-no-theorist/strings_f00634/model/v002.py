def predict(probe):
    # Rule: remove all whitespace (spaces, tabs, newlines) [E1, E6]
    # Rule: uppercase the first character of the original string, lowercase the rest [E1, E2, E4, E6]
    #   - first char may be digit/punct/space; only letters change case [E2, E4, E6]
    #   - "  Leading" -> "leading": first char is space (upper=space), rest lowercased, spaces removed [E4]
    #   - "\ttab here" -> "tabhere": tab removed like space [E6]
    #   - "line\nbreak" -> "Linebreak": newline removed like space [E6]
    import re
    def f(s):
        if not s:
            return ""
        t = s[0].upper() + s[1:].lower()
        return re.sub(r"\s", "", t)
    return {"outputs": [f(x) for x in probe["inputs"]]}
