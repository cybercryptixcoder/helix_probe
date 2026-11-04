def predict(probe):
    def transform(s):
        if s == "":
            return "H"
        first = s[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') - 2) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') - 2) % 26 + ord('A'))
        return first + s[1:]
    try:
        inputs = probe.get("inputs", [])
        outputs = [transform(x) + "JTQL" for x in inputs]
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
