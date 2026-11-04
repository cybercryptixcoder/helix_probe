def predict(probe):
    # Insertion index = ceil(n/2) = (n+1)//2 [E2: lengths 1..5 give 1,1,2,2,3]
    # Insert "5" at that index [E1, E2, E3, E4, E5]
    # Append the last character of the original string [E2: "a"->"a5a", "ab"->"a5bb"]
    # Empty string raises IndexError (on s[-1]) -> output "ERROR: IndexError" [E6]
    outputs = []
    for s in probe.get("inputs", []):
        if s == "":
            outputs.append("ERROR: IndexError")
            continue
        n = len(s)
        idx = (n + 1) // 2
        res = s[:idx] + "5" + s[idx:] + s[-1]
        outputs.append(res)
    return {"outputs": outputs}
