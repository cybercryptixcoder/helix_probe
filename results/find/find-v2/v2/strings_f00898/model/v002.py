def predict(probe):
    # Insert 'f' at index len//2 [E1, E2, E3, E4]
    # Then append the last character [E1, E2, E3, E4]
    # Empty string: insert 'f' at 0, then append last char of original... but original empty.
    #   Observed "" -> "ff": so append 'f' when empty (the inserted char acts as last?) [?]
    #   Simplest: if empty, output "ff" [E4]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        mid = n // 2
        r = s[:mid] + "f" + s[mid:]
        if n > 0:
            r += s[-1]
        else:
            r += "f"
        out.append(r)
    return {"outputs": out}
