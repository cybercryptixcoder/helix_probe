def predict(probe):
    # Reverse the string, then prepend 'k' [E1]
    # Evidence: "abc123" -> "k321cba", "level" -> "klevel", "Zebra" -> "karbeZ"
    # " Zebralower" -> "krewolarbeZ " (reverse keeps leading space at end)
    # "Hello World function lazy" -> "kyzal noitcnuf dlroW olleH"
    # "bananaUPPER" -> "kREPPUananab"
    # So: f(x) = 'k' + x[::-1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("k" + s[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
