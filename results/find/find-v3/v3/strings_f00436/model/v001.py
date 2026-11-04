def predict(probe):
    # Reverse the whole string, then insert 'I' before the last character of the reversed string [E1, E2]
    # Equivalently: reverse s -> r; if len(r)>=1, insert 'I' at position len(r)-1 (before last char) [E2]
    # Empty string -> "I" (insert into empty gives just "I") [E2]
    # Single char -> char + "I" (reversed is same char, insert before last = after it) [E2]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        if len(r) == 0:
            out.append("I")
        else:
            out.append(r[:-1] + "I" + r[-1])
    return {"outputs": out}
