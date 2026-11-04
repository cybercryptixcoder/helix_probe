def predict(probe):
    # Split on whitespace, collapse runs, drop leading/trailing [E6]
    # Each word: reverse chars, then insert 'I' at a length-dependent position [E10,E11,E12,E13,E14]
    #   - len 1: after the 1 char (end) -> "aI" [E4]
    #   - len 2: after 1st char of reversed -> "bIa" [E4]
    #   - len 3: after 1st char of reversed -> "cbIa" [E8]
    #   - len 4: after 2nd char of reversed -> "dcIba" [E8]
    #   - len 5: after 2nd char of reversed -> "edcIba" [E8]
    #   - len 6: after 3rd char of reversed -> "fedIcba" [E8]
    #   - len 7: after 3rd char of reversed -> "gnitIset" [E14]
    #   - len 8: after 4th char of reversed -> "noitIcnuf" [E14]
    #   - len 9: after 4th char of reversed -> "elpmIaxe" [E14]
    #   - len 10: after 5th char of reversed -> "ecneIics" [E14]
    #   - len 11: after 5th char of reversed -> "gninIrael" [E14]
    #   - len 12: after 6th char of reversed -> "ippississiM"->"ippississiM"? [E11: "ippississiM" has I after 6]
    # Rule: insert position = ceil(len/2) in the reversed word (i.e. at index ceil(len/2)) [E8,E14]
    #   len1->1, len2->1, len3->2? check: "abc"->"cbIa" I at index 2. ceil(3/2)=2. yes
    #   len4->2, len5->3? "abcde"->"edcIba" I at index 3. ceil(5/2)=3. yes
    #   len6->3, len7->4? "testing"->"gnitIset" I at index 4. ceil(7/2)=4. yes
    #   len8->4, len9->5? "example"->"elpmIaxe" I at index 5. ceil(9/2)=5. yes
    #   len10->5, len11->6? "learning"->"gninIrael" I at index 6. ceil(11/2)=6. yes
    #   len12->6? "Mississippi"->"ippississiM" I at index 6. ceil(12/2)=6. yes
    # So: insert 'I' at index ceil(len/2) of the reversed word. [E8,E10-E14]
    # Empty/whitespace-only input -> "I" [E6]
    # Join words with single space [E6]
    import math
    def transform(word):
        rev = word[::-1]
        n = len(rev)
        pos = (n + 1) // 2  # ceil(n/2)
        return rev[:pos] + "I" + rev[pos:]
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("I")
            else:
                out.append(" ".join(transform(w) for w in words))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
