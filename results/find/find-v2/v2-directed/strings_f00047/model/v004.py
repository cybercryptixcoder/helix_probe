def predict(probe):
    # Only the very first character of the whole string is uppercased [E1,E2,E3,E4]
    # The rest of the string is lowercased entirely [E3]
    # Leading whitespace: first char is space, so nothing uppercased [E2,E4]
    # Trailing whitespace preserved, no effect on case [E4]
    # Tabs/newlines/CR are not word separators; only the string start matters [E4]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[:1].upper() + s[1:].lower())
        except Exception:
            out.append(s)
    return {"outputs": out}
