def predict(probe):
    # Identity for almost all inputs [E1-E4]
    # Trailing 'D' -> 'J' [E5, E6: "D"->"J", "aD"->"aJ", "helloD"->"helloJ",
    #   "Hello D"->"Hello J", "world D"->"world J", "MiXeD"->"MiXeJ"]
    # BUT "ABCD" -> "ACJ": the D became J AND the preceding C was dropped [E6]
    #   So when a D is preceded by 'C' (i.e. "...CD" ending), the C is removed too.
    #   "D abc" -> "J abc": leading D also becomes J! So it's not just trailing.
    #   Wait: "D abc" -> "J abc" means a D at start of string -> J.
    #   Re-examine: maybe ALL 'D' characters become 'J'? Check "ABCD"->"ACJ":
    #   if all D->J we'd get "ABCJ", but observed "ACJ" (C dropped). Hmm.
    #   Alternative: 'D' -> 'J' everywhere, and additionally "CD" -> "J" (C dropped)?
    #   "ABCD": A B C D -> A B [C dropped] J = "ABJ"? No, observed "ACJ".
    #   Let's think: "ABCD" -> "ACJ". That's A, C, J. B dropped, D->J.
    #   Hmm, or maybe it's a Caesar-like shift on the last char? D->J is +6.
    #   "D"->"J" (+6), "aD"->"aJ", "helloD"->"helloJ". Last char D->J.
    #   "ABCD"->"ACJ": last char D->J, and... "ABC" -> "AC"? B dropped.
    #   "D abc"->"J abc": first char D->J. So D->J wherever it appears?
    #   Then "ABCD" all-D-rule gives "ABCJ" but we see "ACJ". Contradiction unless
    #   something else drops B. 
    #   Maybe rule: replace 'D' with 'J', and also drop 'B' when followed by 'C'?
    #   "ABCD": A B C D -> drop B (before C) -> A C D -> D->J -> A C J. Matches!
    #   Check "D abc": no B before C, D->J -> "J abc". Matches.
    #   Check "aMiXeD": D->J -> "aMiXeJ". Matches.
    #   Check E1 "abc123" no D, no BC. "bananaUPPER" no. "Zebra" no.
    #   Check E2/E3/E4: no D, no "BC". Consistent.
    #   Hypothesis: every 'D' -> 'J'; every 'B' immediately followed by 'C' is dropped.
    #   Uncertain: is it "BC"->"C" or "B" before "C"? Only one data point (ABCD).
    #   Also uncertain whether D->J is truly global (only "D abc" shows leading D).
    def f(s):
        out = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == 'B' and i + 1 < len(s) and s[i+1] == 'C':
                i += 1  # drop B
                continue
            if c == 'D':
                out.append('J')
            else:
                out.append(c)
            i += 1
        return ''.join(out)
    return {"outputs": [f(x) for x in probe["inputs"]]}
