def predict(probe):
    def shift_and_check(s):
        # Shift each UTF-16 code unit by +5
        shifted = [ord(c) + 5 for c in s]
        # Check for invalid surrogate sequences
        i = 0
        n = len(shifted)
        while i < n:
            cp = shifted[i]
            if 0xD800 <= cp <= 0xDBFF:
                # high surrogate: must be followed by low surrogate
                if i + 1 < n and 0xDC00 <= shifted[i+1] <= 0xDFFF:
                    i += 2
                    continue
                else:
                    return None  # invalid
            elif 0xDC00 <= cp <= 0xDFFF:
                # lone low surrogate
                return None
            else:
                i += 1
        return ''.join(chr(c) for c in shifted)

    outputs = []
    for s in probe.get("inputs", []):
        try:
            res = shift_and_check(s)
            if res is None:
                outputs.append("ERROR: ValueError")
            else:
                outputs.append(res + 'W')
        except Exception:
            outputs.append("ERROR: ValueError")
    return {"outputs": outputs}
