def predict(probe):
    # The box reverses each input string [E1: abc123->321cba, level->vel, Zebra->arbeZ]
    # Reversal is character-by-character, including spaces and case [E1: " Zebralower"->"wolarbeZ "]
    # No other transformation observed: case preserved, digits preserved [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1])
        except Exception:
            out.append(s)
    return {"outputs": out}
