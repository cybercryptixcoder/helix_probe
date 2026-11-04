def predict(probe):
    # Split input on whitespace (spaces/tabs/etc), collapsing runs [E6]
    # Each word: reverse chars, then insert 'I' after first char of reversed word [E1,E2,E4]
    # Join words with a single space; leading/trailing whitespace dropped [E6]
    # Empty/whitespace-only input -> "I" [E6 "  "->"I"]
    def transform(word):
        rev = word[::-1]
        return rev[0] + "I" + rev[1:]
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
