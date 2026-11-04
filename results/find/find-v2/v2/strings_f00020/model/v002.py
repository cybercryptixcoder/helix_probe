def predict(probe):
    # Insert "5" at index ceil(len/2) [E1, E2]
    # Append a copy of the last character [E1, E2]
    # Empty string raises IndexError (box errors out) [E2]
    def f(s):
        n = len(s)
        idx = (n + 1) // 2
        out = s[:idx] + "5" + s[idx:]
        out = out + s[-1]  # IndexError on empty string, matching box
        return out
    results = []
    for x in probe.get("inputs", []):
        try:
            results.append(f(x))
        except Exception as e:
            results.append("ERROR: " + type(e).__name__)
    return {"outputs": results}
