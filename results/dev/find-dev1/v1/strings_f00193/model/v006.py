def predict(probe):
    def transform(s):
        first = s[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') - 2) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') - 2) % 26 + ord('A'))
        return first + s[1:]
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            if x == "":
                outputs.append("HTQL")
            else:
                outputs.append(transform(x) + "JTQL")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
