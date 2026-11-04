def predict(probe):
    # Split ORIGINAL string at len//2 into left and right halves [E6]
    # Left half: .capitalize() (first char upper, rest lower; ß->Ss) [E2,E5,E6]
    # Right half: .lower() (all lower; İ->i̇, ß stays ß) [E5,E6]
    # Join with "10" [E1,E3]
    #   len 0 -> "10"; len 1 -> "10"+lower(s) [E3]
    out = []
    for s in probe.get("inputs", []):
        p = len(s) // 2
        left = s[:p].capitalize()
        right = s[p:].lower()
        out.append(left + "10" + right)
    return {"outputs": out}
