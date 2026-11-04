def predict(probe):
    # Reverse each word's characters, keep word order and spaces [E1, E2]
    # Insert capital 'I' after the first character of each word [E1, E2]
    #   "abc"->"cbIa", "Abc"->"cbIA", "a b"->"Ia b", "123"->"32I1"
    # Single-char words: "a"->"Ia" (I after the char) [E2 "a b"->"Ia b"]
    # Spaces preserved as-is; words split on spaces [E1, E2]
    def transform(word):
        if not word:
            return word
        rev = word[::-1]
        return rev[0] + "I" + rev[1:]
    try:
        out = []
        for s in probe.get("inputs", []):
            parts = s.split(" ")
            out.append(" ".join(transform(w) for w in parts))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
