def predict(probe):
    # f(s): split on whitespace into tokens t1..tn. [E1,E2]
    # Output = rev(dedup(t1)) + " " + rev(dedup_after(t2+...+tn))  [E1-E9]
    # where dedup keeps first occurrence, and the rest-block dedup treats
    # letters already emitted by the first word as already-seen. [E8,E9]
    #   "one two three": first "one"->"eno"; rest "twothree" dedup against {o,n,e}
    #     = "twhr" -> "rhwt" -> "eno rhwt" [E9]
    #   "sun moon star": first "sun"->"nus"; rest "moonstar" dedup against {s,u,n}
    #     = "motar" -> "ratom" -> "nus ratom" [E9]
    #   "big red dog": first "big"->"gib"; rest "reddog" dedup against {b,i,g}
    #     = "redo" -> "oder" -> "gib oder" [E9]
    #   "hello big world": first "hello"->"helo"->"oleh"; rest "bigworld" dedup
    #     against {h,e,l,o} = "bigwrd" -> "drwgib" -> "oleh drwgib" [E9]
    #   "cat sat mat": first "cat"->"tac"; rest "satmat" dedup against {c,a,t}
    #     = "sm" -> "ms" -> "tac ms" [E9]
    #   "red dog": first "red"->"der"; rest "dog" dedup against {r,e,d} = "og" -> "go" [E9]
    #   "moon star": first "moon"->"mon"->"nom"; rest "star" dedup against {m,o,n}
    #     = "star" -> "rats" -> "nom rats" [E9]
    #   "do re mi": first "do"->"od"; rest "remi" dedup against {d,o} = "remi"
    #     -> "imer" -> "od imer" [E9]
    #   "foo bar baz": first "foo"->"fo"->"of"; rest "barbaz" dedup against {f,o}
    #     = "barz" -> "zrab" -> "of zrab" [E9]
    # Single word: just rev(dedup(word)). [E1,E7]
    # Leading/trailing/multiple spaces collapsed by split(). [E1,E2]
    # Dedup keeps FIRST occurrence (not last). [E7: "bookkeeper"->"rpekob"]
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
                out.append(first + " " + rest)
        except Exception:
            out.append("")
    return {"outputs": out}
