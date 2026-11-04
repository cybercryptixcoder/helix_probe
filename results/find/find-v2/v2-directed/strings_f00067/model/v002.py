def predict(probe):
    # Observations:
    # - Each whitespace-separated token is transformed independently [E1, E2].
    # - A token w -> w[-1] + w[::-1]  (last char prepended to reversed token) [E1, E2].
    #   e.g. "hello"->"oolleh", "abc"->"ccba", "a"->"aa", "hello,"->",,olleh",
    #   "123"->"3321", "A1!"->"!!1A", "cat."->"..tac" [E1, E2]
    # - Whitespace is NOT preserved verbatim: runs of spaces collapse to a single
    #   space, and leading/trailing whitespace is stripped [E2: "hi  there"->"ih eereht",
    #   " x "->"x"]. So output = " ".join(transform(t) for t in s.split()).
    def fword(w):
        return w[-1] + w[::-1]
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            out.append(" ".join(fword(t) for t in toks))
        except Exception:
            out.append(s)
    return {"outputs": out}
