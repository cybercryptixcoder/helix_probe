def predict(probe):
    """Model: f(x) reverses the characters of x by code point, then removes all Unicode whitespace."""
    try:
        out = []
        for s in probe.get("inputs", []):
            rev = s[::-1]
            out.append("".join(ch for ch in rev if not ch.isspace()))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
