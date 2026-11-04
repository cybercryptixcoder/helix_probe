def predict(probe):
    # Rule: insert 'i' at index floor(len/2) of the ORIGINAL string,
    #       then strip whitespace from both ends [E1-E12]
    # - index computed on pre-strip length: "   ab" -> "i ab" vs "ab   " -> "abi" [E6, E7]
    # - strip applied after insertion: "  " -> "i", " hello" -> "heillo" [E3, E9]
    # - internal whitespace preserved: "two words" -> "two iwords" [E1]
    outputs = []
    for s in probe["inputs"]:
        idx = len(s) // 2
        result = s[:idx] + "i" + s[idx:]
        outputs.append(result.strip())
    return {"outputs": outputs}
