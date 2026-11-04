def predict(probe):
    # Insert "5" at index ceil(n/2) = (n+1)//2 [E1-E18 all consistent]
    # Append a copy of the ORIGINAL last character (not modified last) [E11 "a"->"a5a", E14 "a  "->"a 5  "]
    # Empty string: insert at 0, no last char to duplicate -> "5" [?]
    results = []
    for s in probe.get("inputs", []):
        n = len(s)
        i = (n + 1) // 2
        out = s[:i] + "5" + s[i:]
        if n > 0:
            out += s[-1]
        results.append(out)
    return {"outputs": results}
