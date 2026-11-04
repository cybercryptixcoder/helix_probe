def predict(probe):
    # Each character's Unicode code point is increased by 1 [E1]
    #   'h'->'i', 'e'->'f', ' '->'!', '1'->'2', '!'->'"', '?'->'@'
    # Applies to every character, including spaces, digits, punctuation [E1]
    # Case is preserved because shifting code point keeps letter case [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("".join(chr(ord(c) + 1) for c in s))
        except Exception:
            out.append(s)
    return {"outputs": out}
