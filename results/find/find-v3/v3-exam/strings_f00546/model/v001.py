def predict(probe):
    # Split input on spaces; reverse characters of each word; keep word order;
    # prefix "lmKA" to the last word; join with single spaces [E1]
    # Leading/trailing/empty words: empty words reverse to empty, join preserves spacing
    # but E1 " Zebralower" -> "lmKArewolarbeZ" (leading space dropped)
    # So empty words are dropped before joining.
    out = []
    for s in probe.get("inputs", []):
        words = [w for w in s.split(" ") if w != ""]
        rev = [w[::-1] for w in words]
        if rev:
            rev[-1] = "lmKA" + rev[-1]
        out.append(" ".join(rev))
    return {"outputs": out}
