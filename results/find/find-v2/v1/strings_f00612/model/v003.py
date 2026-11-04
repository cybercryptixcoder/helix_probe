def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            try:
                shifted_chars = []
                for ch in s:
                    cp = ord(ch) + 1
                    if cp > 0x10FFFF:
                        raise ValueError("out of range")
                    shifted_chars.append(chr(cp))
                shifted = "".join(shifted_chars)
                idx = len(s) // 2
                out.append(shifted[:idx] + "Y" + shifted[idx:])
            except Exception:
                out.append("ERROR: ValueError")
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
