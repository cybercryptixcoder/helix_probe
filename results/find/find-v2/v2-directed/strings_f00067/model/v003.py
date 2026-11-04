def predict(probe):
    # Observations:
    # - Each whitespace-separated token is transformed independently [E1, E2].
    # - A token w -> w[-1] + w[::-1]  (last char prepended to reversed token) [E1, E2].
    #   e.g. "hello"->"oolleh", "abc"->"ccba", "a"->"aa", "hello,"->",,olleh",
    #   "123"->"3321", "A1!"->"!!1A", "cat."->"..tac" [E1, E2]
    # - Whitespace is NOT preserved verbatim: runs of spaces collapse to a single
    #   space, and leading/trailing whitespace is stripped [E2: "hi  there"->"ih eereht",
    #   " x "->"x"]. So output = " ".join(transform(t) for t in s.split()).
    # - BUT single-char tokens: "a"->"aa" only when alone? No: E3 shows "a  b"->"a bb",
    #   so "a"->"a" (not "aa") when part of a multi-token string [E3].
    #   Wait: E1 "a"->"aa" alone. E3 "a b"->"a bb": first token "a"->"a".
    #   Hypothesis: single-char token maps to itself, EXCEPT when it is the only
    #   token in the whole input? Check E1 "a"->"aa" (only token). E3 "a  b"->"a bb"
    #   ("a" not only token -> "a"). "x  y"->"x yy" ("x"->"x"). Consistent [E1,E3].
    #   So: if the input has exactly one token and it is length 1, output = w+w.
    #   Otherwise single-char token -> itself. Multi-char tokens: w[-1]+w[::-1].
    import re
    def fword(w):
        if len(w) == 1:
            return w  # placeholder; handled by caller for the lone-token case
        return w[-1] + w[::-1]
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            if len(toks) == 1 and len(toks[0]) == 1:
                out.append(toks[0] + toks[0])
            else:
                out.append(" ".join(fword(t) for t in toks))
        except Exception:
            out.append(s)
    return {"outputs": out}
