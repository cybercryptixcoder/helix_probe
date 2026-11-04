def predict(probe):
    # Reverse the string, then prepend 'k' [E1: hello->kolleh, 123->k321]
    # Reversal applies to whole string including spaces/punct [E1: hello world->kdlrow olleh]
    # Case preserved as-is [E1: Hello->kolleH, HELLO->kOLLEH]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("k" + s[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
