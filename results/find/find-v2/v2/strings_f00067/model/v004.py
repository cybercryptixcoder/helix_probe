def predict(probe):
    # Each word is reversed [E1: "abc123"->"3321cba", E2: "hello"->"olleh"]
    # Words split on whitespace, rejoined with single spaces; leading/trailing
    #   whitespace dropped [E2: "hello  world"->"olleh ddlrow", "  hello"->"oolleh"]
    # First char of the reversed LAST word is doubled iff the input does NOT
    #   end with whitespace [E2: "world"->"ddlrow" vs "red "->"der"; E6: "x"->"xx"]
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            if not words:
                out.append("")
                continue
            rev = [w[::-1] for w in words]
            if not s[-1].isspace():
                rev[-1] = rev[-1][0] + rev[-1]
            out.append(" ".join(rev))
        except Exception:
            out.append("")
    return {"outputs": out}
