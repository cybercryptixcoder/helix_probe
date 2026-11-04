def predict(probe):
    def is_letter(ch):
        return ch.isalpha()
    def shift(s):
        if not s:
            return s
        out = list(s)
        last = s[-1]
        if is_letter(last):
            if last == 'z':
                out[-1] = 'a'
            elif last == 'Z':
                out[-1] = 'A'
            else:
                out[-1] = chr(ord(last) + 1)
        return ''.join(out)
    try:
        return {"outputs": [shift(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
