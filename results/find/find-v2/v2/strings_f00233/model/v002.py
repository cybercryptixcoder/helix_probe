def predict(probe):
    # Reverse the string, then capitalize (first char upper, rest lower) [E1, E2]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1].capitalize())
        except Exception:
            out.append("")
    return {"outputs": out}
