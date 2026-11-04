def predict(probe):
    def shift(s):
        out = list(s)
        i = 0
        n = len(s)
        while i < n:
            if s[i].isalpha() and s[i].isascii():
                j = i
                while j < n and s[j].isalpha() and s[j].isascii():
                    j += 1
                # shift only the last char of the run
                last = s[j-1]
                if 'a' <= last <= 'z':
                    out[j-1] = chr((ord(last) - ord('a') + 1) % 26 + ord('a'))
                elif 'A' <= last <= 'Z':
                    out[j-1] = chr((ord(last) - ord('A') + 1) % 26 + ord('A'))
                i = j
            else:
                i += 1
        return ''.join(out)
    try:
        return {"outputs": [shift(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
