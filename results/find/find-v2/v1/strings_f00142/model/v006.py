def predict(probe):
    def shift(s):
        return ''.join(chr(ord(c) + 5) for c in s)

    def is_high(cp):
        return 0xD800 <= cp <= 0xDBFF

    def is_low(cp):
        return 0xDC00 <= cp <= 0xDFFF

    def check(s):
        # Detect invalid surrogate sequences in the *shifted* string,
        # but only when the original input had a valid pair that got broken.
        orig = [ord(c) for c in s]
        shifted = [cp + 5 for cp in orig]
        i = 0
        n = len(shifted)
        while i < n:
            cp = shifted[i]
            if is_high(cp):
                if i + 1 < n and is_low(shifted[i + 1]):
                    i += 2
                    continue
                else:
                    # lone high surrogate in output
                    # was the original also a lone high surrogate?
                    if is_high(orig[i]):
                        # original lone high -> allowed
                        i += 1
                        continue
                    else:
                        return None
            elif is_low(cp):
                # lone low surrogate in output
                if is_low(orig[i]):
                    i += 1
                    continue
                else:
                    return None
            else:
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
