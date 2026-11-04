def predict(probe):
    # Reverse the whole string [E1-E22]
    # Insert 'I' at index len//2 of the ORIGINAL string, measured from the start,
    #   then reverse. Equivalently: in the reversed string, insert 'I' at
    #   position len - len//2 = ceil(len/2) from the start of the reversed string.
    #   Check: "cat" len3 -> orig mid 1 -> "c|at" -> reverse "ta|c" -> "taIc" [E20]
    #   "hello" len5 -> mid2 -> "he|llo" -> "oll|eh" -> "ollIeh" [E20]
    #   "the cat sat on the mat" len22 -> mid11 -> insert after 11 chars of orig,
    #     reversed gives "eht tac Itas..." [E22]
    # Leading/trailing whitespace is stripped before processing [E18 "  cat dog  "->"Itac god",
    #   E19 " lazy "->"yzIal", E21 "  hello"->"olleIh"]
    out = []
    for s in probe.get("inputs", []):
        s = s.strip()
        n = len(s)
        m = n // 2
        # insert 'I' at index m in original, then reverse
        t = s[:m] + "I" + s[m:]
        out.append(t[::-1])
    return {"outputs": out}
