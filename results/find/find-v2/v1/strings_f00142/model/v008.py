def predict(probe):
    def is_high(cp):
        return 0xD800 <= cp <= 0xDBFF

    def is_low(cp):
        return 0xDC00 <= cp <= 0xDFFF

    def check(s):
        orig = [ord(c) for c in s]
        shifted = [cp + 5 for cp in orig]
        i = 0
        n = len(orig)
        while i < n:
            # Detect an original valid pair whose shifted high lands in low range
            if i + 1 < n and is_high(orig[i]) and is_low(orig[i + 1]):
                if is_low(shifted[i]):
                    return None
                i += 2
                continue
            i += 1
        return ''.join(chr(c) for c in shifted)

    outputs = []
    for s in probe.get("inputs", []):
        try:
            res = check(s)
            if res is None:
                outputs.append("ERROR: ValueError")
            else:
                outputs.append(res + 'W')
        except Exception:
            outputs.append("ERROR: ValueError")
    return {"outputs": outputs}
