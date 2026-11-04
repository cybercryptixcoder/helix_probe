def predict(probe):
    # Rule: s.capitalize() then remove ALL whitespace [E1, E2]
    # - "hello\tworld" -> "Helloworld", "hello\nworld" -> "Helloworld" [E2]
    # - "  leading" -> "leading", "trailing  " -> "Trailing" [E2]
    # - "hello WORLD" -> "Helloworld" (rest lowercased) [E2]
    # - "123ABC" -> "123abc", "HELLO" -> "Hello", "x" -> "X" [E2]
    # - " Zebralower" -> capitalize gives " zebralower", strip ws -> "zebralower" [E1]
    import re
    out = []
    for s in probe.get("inputs", []):
        try:
            t = s.capitalize()
            t = re.sub(r"\s+", "", t)
            out.append(t)
        except Exception:
            out.append("")
    return {"outputs": out}
