def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            for c in s:
                o = ord(c)
                if 'a' <= c <= 'z':
                    r.append(chr((o - ord('a') + 2) % 26 + ord('a')))
                elif 'A' <= c <= 'Z':
                    r.append(chr((o - ord('A') + 2) % 26 + ord('A')))
                elif '0' <= c <= '9':
                    r.append(chr((o - ord('0') + 2) % 10 + ord('0')))
                else:
                    r.append(chr(o + 2))
            out.append("".join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
