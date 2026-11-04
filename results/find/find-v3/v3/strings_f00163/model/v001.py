def predict(probe):
    # Rule: reverse the string, then insert "2" at the middle position [E1]
    #   - "abc123" -> "321cba" -> insert 2 at index 3 -> "3212cba" [E1]
    #   - "level"  -> "level"  -> insert 2 at index 2 -> "lev2el"  [E1]
    #   - " Zebralower" -> "rewolarbeZ " -> insert 2 at index 6 -> "rewola2rbeZ " [E1]
    #   - "Hello World function lazy" -> reversed -> insert 2 at index 12 -> matches [E1]
    #   - "bananaUPPER" -> "REPPUananab" -> insert 2 at index 5 -> "REPPUa2nanab" [E1]
    #   - "Zebra" -> "arbeZ" -> insert 2 at index 2 -> "arb2eZ" [E1]
    # Middle index = len(s)//2 (integer division) [E1]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        mid = len(r) // 2
        out.append(r[:mid] + "2" + r[mid:])
    return {"outputs": out}
