def predict(probe):
    # Each word (space-separated token) is reversed in place; word order kept [E1,E2,E3]
    # Trailing/leading spaces are dropped (split/join normalizes) [E2,E3]
    # Then "I" is appended at the end [E1,E2,E3]
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            rev = " ".join(w[::-1] for w in words)
            out.append(rev + "I")
        except Exception:
            out.append("")
    return {"outputs": out}
