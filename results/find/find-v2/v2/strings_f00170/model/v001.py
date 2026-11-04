def predict(probe):
    # Rule: output = 'k' + reverse(input) [E1]
    # Evidence: every output in E1 is 'k' followed by the input reversed.
    #   "abc123" -> "k321cba", "level" -> "klevel" (palindrome),
    #   " Zebralower" -> "krewolarbeZ " (space moves to end),
    #   "Hello World function lazy" -> "kyzal noitcnuf dlroW olleH",
    #   "bananaUPPER" -> "kREPPUananab", "Zebra" -> "karbeZ".
    # So: prepend 'k', then reverse the whole string.
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("k" + s[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
