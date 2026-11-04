def predict(probe):
    def shift_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 5) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 5) % 26 + ord('A'))
        if '0' <= c <= '9':
            return chr((ord(c) - ord('0') + 5) % 10 + ord('0'))
        return chr(ord(c) + 5)

    outputs = []
    for s in probe.get("inputs", []):
        try:
            out = ''.join(shift_char(c) for c in s) + 'W'
        except Exception:
            out = ''
        outputs.append(out)
    return {"outputs": outputs}
