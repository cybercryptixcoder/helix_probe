def predict(probe):
    # Reverses the string, then appends "I" [E1: all outputs are reversed input + "I"]
    # "abc123" -> "321cba" + "I"; "level" -> "level" + "I"; " Zebralower" -> "rewolarbeZ" + "I"
    # "Hello World function lazy" -> reversed + "I"; "bananaUPPER" -> "REPPUananab" + "I"; "Zebra" -> "arbeZ" + "I"
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1] + "I")
        except Exception:
            out.append("")
    return {"outputs": out}
