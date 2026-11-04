def predict(probe):
    # Rule: insert 'i' at index floor(len(s)/2) of the whole string [E1,E2,E3]
    # Leading/trailing spaces are stripped BEFORE computing length and insertion [E3]
    #   " hello" -> strip -> "hello" len5 -> heillo ✓
    #   "hello " -> strip -> "hello" -> heillo ✓
    #   "  " -> strip -> "" -> "i" ✓
    #   " " -> "" -> "i" ✓
    # Interior spaces are kept as-is and count toward length [E3]
    #   "hello world" len11 floor5 -> helloi world ✓
    #   "hello  world" len12 floor6 -> hello i world ✓
    #   "a b" len3 floor1 -> ai b ✓
    #   "ab cd" len5 floor2 -> abi cd ✓
    #   "hi there" len8 floor4 -> hi tihere ✓
    #   "one two three" len13 floor6 -> one twio three ✓
    #   "x y z" len5 floor2 -> x iy z ✓
    # Empty string -> "i" (guess, consistent with whitespace->i) [?]
    def transform(s):
        t = s.strip()
        if t == '':
            return 'i'
        pos = len(t) // 2
        return t[:pos] + 'i' + t[pos:]
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [transform(s) for s in inputs]}
    except Exception:
        return {"outputs": []}
