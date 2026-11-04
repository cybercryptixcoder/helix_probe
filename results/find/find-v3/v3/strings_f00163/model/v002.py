def predict(probe):
    # Rule: reverse the string, then insert "2" at the middle position.
    # Middle index appears to be ceil(len/2) of the reversed string [E2]:
    #   "a" -> "a" -> insert at 1 -> "a2"
    #   "ab" -> "ba" -> insert at 1 -> "b2a"
    #   "abc" -> "cba" -> insert at 2 -> "cb2a"
    #   "abcd" -> "dcba" -> insert at 2 -> "dc2ba"
    #   "abcde" -> "edcba" -> insert at 3 -> "edc2ba"
    #   "Hello" -> "olleH" -> insert at 3 -> "oll2eH"
    #   "hello world" -> "dlrow olleh" -> insert at 6 -> "dlrow 2olleh"
    #   "12345" -> "54321" -> insert at 3 -> "543221"
    #   "A B C" -> "C B A" -> insert at 3 -> "C B2 A"
    #   "Test123!" -> "!321tseT" -> insert at 4 -> "!3212tseT"
    # Also consistent with E1 examples.
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        mid = (len(r) + 1) // 2
        out.append(r[:mid] + "2" + r[mid:])
    return {"outputs": out}
