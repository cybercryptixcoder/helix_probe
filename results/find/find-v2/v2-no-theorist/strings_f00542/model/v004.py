def predict(probe):
    # Split on whitespace, reverse each token, join with single spaces [E2,E3,E4]
    # Runs of spaces collapse to one; leading/trailing whitespace dropped [E4]
    # Tabs/newlines act as separators too [E4]
    # Empty/whitespace-only input -> "" [E4]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(" ".join(w[::-1] for w in s.split()))
        except Exception:
            out.append("")
    return {"outputs": out}
