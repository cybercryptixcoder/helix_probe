def predict(probe):
    # Reverse the whole string, then insert 'I' at the middle position of the reversed string [E1-E4]
    # Middle = len(r)//2 (integer division), inserted before that index [E4]
    # Empty string -> "I" [E2]
    # Single char -> char + "I" (middle of len 1 is 0, insert before index 0? no...) [E2]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        n = len(r)
        if n == 0:
            out.append("I")
        else:
            m = n // 2
            out.append(r[:m] + "I" + r[m:])
    return {"outputs": out}
