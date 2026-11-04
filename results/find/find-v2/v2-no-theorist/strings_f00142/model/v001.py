def predict(probe):
    # Each character shifted +5 in ASCII, then "W" appended [E1]
    # e.g. "abc123" -> "fgh678W", " Zebralower" -> "%_jgwfqt|jwW" [E1]
    out = []
    for s in probe.get("inputs", []):
        out.append("".join(chr(ord(c) + 5) for c in s) + "W")
    return {"outputs": out}
