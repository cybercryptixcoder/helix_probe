def predict(probe):
    # Insert "5" at index ceil(len/2) = (len+1)//2, then append the last char [E2, E3, E4, E5]
    # Empty string raises IndexError (box errors out) [E6]
    # Single char "a" -> "a5a": insert at index 1, append last char [E4, E6]
    # Appended char is always the original last char, even space/punct [E6]
    outs = []
    for s in probe.get("inputs", []):
        if len(s) == 0:
            outs.append("ERROR: IndexError")
        else:
            k = (len(s) + 1) // 2
            outs.append(s[:k] + "5" + s[k:] + s[-1])
    return {"outputs": outs}
