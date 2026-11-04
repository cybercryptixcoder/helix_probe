def predict(probe):
    # Insert 'i' at index floor(len(s)/2) of the ORIGINAL string, then strip leading/trailing whitespace [E1,E2,E3,E4]
    #   " hello" len6 floor3 -> " heillo" -> "heillo" [E3]
    #   "hello " len6 floor3 -> "helilo " -> "helilo" [E3]
    #   "ab  " len4 floor2 -> "abi  " -> "abi" [E4]
    #   "  ab" len4 floor2 -> "  iab" -> "iab" [E4]
    #   "  ab  " len6 floor3 -> "  aib  " -> "aib" [E4]
    #   "  " len2 floor1 -> " i " -> "i" [E3]
    # Interior whitespace (spaces, tabs, newlines) kept and counted [E3,E4]
    # Empty string len0 floor0 -> "i" [?]
    def transform(s):
        pos = len(s) // 2
        return (s[:pos] + 'i' + s[pos:]).strip()
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [transform(s) for s in inputs]}
    except Exception:
        return {"outputs": []}
