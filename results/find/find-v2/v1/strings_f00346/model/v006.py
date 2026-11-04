def predict(probe):
    def transform(s):
        t = ''.join(ch for ch in s if not ch.isspace())
        if not t:
            return ''
        first = t[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') + 2) % 26 + ord('A'))
        elif first.isalpha():
            first = chr(ord(first) + 2)
        return first + t[1:]
    return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
