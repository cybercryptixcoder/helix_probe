def predict(probe):
    # Reverse the string, then prepend 'k' [E1]
    # "abc123" -> "321cba" -> "k321cba" [E1]
    # "level" -> "level" -> "klevel" [E1]
    # " Zebralower" -> "rewolarbeZ " -> "krewolarbeZ " [E1]
    # "Hello World function lazy" -> "yzal noitcnuf dlroW olleH" -> "kyzal..." [E1]
    # "bananaUPPER" -> "REPPUananab" -> "kREPPUananab" [E1]
    # "Zebra" -> "arbeZ" -> "karbeZ" [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("k" + s[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
