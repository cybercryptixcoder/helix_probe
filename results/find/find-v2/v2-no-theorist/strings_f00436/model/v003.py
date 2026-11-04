def predict(probe):
    # Split on whitespace, collapse runs, drop leading/trailing [E6]
    # Each word: reverse chars, then insert 'I' after the 3rd char of the reversed word
    #   (i.e. at index 3), or at end if word shorter than 3 [E1,E2,E3,E5,E7,E8]
    # Empty/whitespace-only input -> "I" [E6]
    # Join words with single space [E6]
    def transform(word):
        rev = word[::-1]
        if len(rev) <= 3:
            return rev + "I"
        return rev[:3] + "I" + rev[3:]
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
