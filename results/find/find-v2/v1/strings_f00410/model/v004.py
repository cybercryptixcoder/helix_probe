def predict(probe):
    def transform(s):
        try:
            if not s:
                return s
            rev = s[::-1]
            first = rev[0]
            if first.isalpha():
                base = ord('A') if first.isupper() else ord('a')
                shifted = chr((ord(first) - base - 2) % 26 + base)
                return shifted + rev[1:]
            return rev
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
