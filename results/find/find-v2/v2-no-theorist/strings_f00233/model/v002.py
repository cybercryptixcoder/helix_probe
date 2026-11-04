def predict(probe):
    # Reverse the string [E1, E2]
    # Then uppercase the first character of the result, lowercase the rest [E2]
    # "hello" -> "olleh" -> "Olleh" [E2]
    # "HELLO" -> "OLLEH" -> "Olleh" [E2]
    # "MiXeD" -> "DeXiM" -> "Dexim" [E2]
    # " a" -> "a " -> "A " [E2]
    # "a " -> " a" -> " a" [E2]
    out = []
    for s in probe.get("inputs", []):
        try:
            r = s[::-1]
            if r:
                r = r[0].upper() + r[1:].lower()
            out.append(r)
        except Exception:
            out.append("")
    return {"outputs": out}
