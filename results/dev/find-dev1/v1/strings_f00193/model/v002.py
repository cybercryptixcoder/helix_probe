def predict(probe):
    def transform(s):
        if s == "":
            return "H"
        out = []
        for c in s:
            if 'a' <= c <= 'z':
                out.append(chr((ord(c) - ord('a') - 2) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                out.append(chr((ord(c) - ord('A') - 2) % 26 + ord('A')))
            else:
                out.append(c)
        return ''.join(out)
    try:
        inputs = probe.get("inputs", [])
        outputs = [transform(x) + "JTQL" for x in inputs]
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
