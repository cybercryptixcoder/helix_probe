def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            mid = len(s) // 2
            result = s[:mid] + "2" + s[mid:]
            last = result[-1]
            if last.isalpha():
                if 'a' <= last <= 'z':
                    shifted = chr((ord(last) - ord('a') + 2) % 26 + ord('a'))
                elif 'A' <= last <= 'Z':
                    shifted = chr((ord(last) - ord('A') + 2) % 26 + ord('A'))
                else:
                    shifted = chr(ord(last) + 2)
                result = result[:-1] + shifted
            outputs.append(result)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
