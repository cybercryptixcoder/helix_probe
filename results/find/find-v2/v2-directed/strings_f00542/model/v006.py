def predict(probe):
    # f(s): split on whitespace into tokens t1..tn. [E1,E2]
    # Output = rev(dedup(t1)) + " " + rev(dedup_after(t2+...+tn))  [E1-E9]
    # Dedup keeps FIRST occurrence. [E7: "bookkeeper"->"rpekob"]
    # First word's letters feed into rest-block's seen-set. [E10,E11]
    # BUT: if the rest-block dedup produces an EMPTY string, no trailing
    #   space is emitted (just the first word's reverse). [E11: "eat ate"->"tae",
    #   "cat act"->"tac", "top pot"->"pot"]
    # Dedup is case-sensitive and applies to non-letters too. [E11: "Red red"->"deR r",
    #   "red Red"->"der R", "red dog!"->"der !go"]
    # Single word: just rev(dedup(word)). [E1,E7]
    # Leading/trailing/multiple spaces collapsed by split(). [E1,E2]
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            if not toks:
                out.append("")
                continue
            seen = set()
            def dedup(x):
                r = []
                for c in x:
                    if c not in seen:
                        seen.add(c)
                        r.append(c)
                return "".join(r)
            first = dedup(toks[0])[::-1]
            if len(toks) == 1:
                out.append(first)
            else:
                rest = dedup("".join(toks[1:]))[::-1]
                if rest:
                    out.append(first + " " + rest)
                else:
                    out.append(first)
        except Exception:
            out.append("")
    return {"outputs": out}
