def predict(probe):
    # Tokens split on whitespace; whitespace collapses to single spaces, stripped [E2,E3].
    # Every token w -> w[-1] + w[::-1] [E1,E2].
    # Single-char token -> itself, EXCEPT the last token which is always w[-1]+w[::-1]
    #   (so a lone single-char last token -> w+w) [E1,E3,E4].
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            if not toks:
                out.append("")
                continue
            res = []
            for i, w in enumerate(toks):
                if len(w) == 1 and i != len(toks) - 1:
                    res.append(w)
                else:
                    res.append(w[-1] + w[::-1])
            out.append(" ".join(res))
        except Exception:
            out.append(s)
    return {"outputs": out}
