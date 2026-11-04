def predict(probe):
    # Lowercase entire string, then uppercase first char of raw string [E1,E2]
    # Remove all whitespace [E1,E3]
    # Capitalization applies to raw first char only (even if whitespace) [E7,E8]
    # Case mapping is full Unicode: ß -> SS (Python str.upper) [E9]
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("")
            continue
        t = s[0].upper() + s[1:].lower()
        out.append("".join(t.split()))
    return {"outputs": out}
