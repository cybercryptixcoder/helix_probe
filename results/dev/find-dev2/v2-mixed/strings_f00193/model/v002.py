def predict(probe):
    # Every output appends constant suffix "JTQL" [E1-E6]
    # First character shifted back 2 in alphabet, same case, wrapping [E1-E6]
    # Non-letter first chars unchanged [E2 "123abc", E6 "1 2","! ?"," a"]
    out = []
    for s in probe.get("inputs", []):
        if s and s[0].isalpha():
            c = s[0]
            if c.islower():
                n = (ord(c) - ord('a') - 2) % 26 + ord('a')
            else:
                n = (ord(c) - ord('A') - 2) % 26 + ord('A')
            s = chr(n) + s[1:]
        out.append(s + "JTQL")
    return {"outputs": out}
