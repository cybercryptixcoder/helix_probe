def predict(probe):
    # A: split on any whitespace, drop empty parts [E2, E6]
    # A: if 0 or 1 parts, return "" or the single part (whitespace stripped) [E6]
    # A: if >1 parts, reverse order and join with single spaces [E1, E2, E3, E4, E5]
    # A: punctuation stays attached to its word [E3, E4, E5]
    def f(s):
        parts = s.split()
        if len(parts) > 1:
            return " ".join(reversed(parts))
        return parts[0] if parts else ""
    return {"outputs": [f(x) for x in probe["inputs"]]}
