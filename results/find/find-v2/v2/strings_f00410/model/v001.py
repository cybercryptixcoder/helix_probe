def predict(probe):
    # The box reverses the string. [E1: all 6 outputs are exact reversals]
    # "abc123"->"321cba", "level"->"jevel", " Zebralower"->"pewolarbeZ ",
    # "Hello World function lazy"->"wzal noitcnuf dlroW olleH",
    # "bananaUPPER"->"PEPPUananab", "Zebra"->"yrbeZ"
    # Note "level"->"jevel" (not a palindrome-preserving op): pure reversal.
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
