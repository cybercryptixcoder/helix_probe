def predict(probe):
    def transform(s):
        # remove spaces first
        t = s.replace(' ', '')
        if not t:
            return ''
        first = t[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') + 2) % 26 + ord('A'))
        return first + t[1:]
    return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
