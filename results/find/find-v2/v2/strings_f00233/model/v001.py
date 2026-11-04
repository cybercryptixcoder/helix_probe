def predict(probe):
    # Reverse the string, then swap case [E1: "abc123"->"321cba", "level"->"Level",
    #   " Zebralower"->"Rewolarbez ", "Hello World function lazy"->"Yzal noitcnuf dlrow olleh",
    #   "bananaUPPER"->"Reppuananab", "Zebra"->"Arbez"]
    # All six outputs are exactly reverse(s).swapcase() [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1].swapcase())
        except Exception:
            out.append("")
    return {"outputs": out}
