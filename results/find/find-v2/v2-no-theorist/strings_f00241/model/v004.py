def predict(probe):
    # Identity for almost all inputs [E1-E4, E7]
    # 'D' -> 'J' everywhere [E5, E6: "D"->"J", "aD"->"aJ", "helloD"->"helloJ",
    #   "Hello D"->"Hello J", "world D"->"world J", "D abc"->"J abc", "MiXeD"->"MiXeJ"]
    # 'B' immediately followed by 'C' is dropped (case-sensitive, uppercase only) [E8:
    #   "BC"->"C", "ABC"->"AC", "xBCx"->"xCx", "BBC"->"C", "BCC"->"CC", "BCBC"->"CC",
    #   "a B C"->"a  C", "ABCDE"->"ACJE"; "abC"->"abC", "aBc"->"ac" (B dropped, c kept)]
    #   Note "aBc"->"ac": B dropped even before lowercase c? Wait: "aBc"->"ac" means
    #   B dropped and c kept. But "abC"->"abC" (b kept, C kept). So rule: drop 'B' when
    #   next char is 'C' OR 'c'? "aBc"->"ac" confirms B dropped before 'c' too.
    #   But "abC" keeps b (b is lowercase, rule is uppercase B). So: uppercase 'B'
    #   followed by 'C' or 'c' is dropped. Check "BBC"->"C": first B followed by B (kept?),
    #   second B followed by C (dropped) -> "BC"? but observed "C". Hmm.
    #   "BBC"->"C": both B's gone. If rule is "B followed by C dropped": first B->next is B
    #   (kept), second B->next C (dropped) gives "BC". Not "C". So maybe: 'B' followed by
    #   'B' or 'C' dropped? "BBC": B1 next B -> drop, B2 next C -> drop -> "C". Matches.
    #   "BCBC"->"CC": B1 next C drop, B2 next C drop -> "CC". Matches.
    #   "BCC"->"CC": B next C drop -> "CC". Matches.
    #   So rule: uppercase 'B' is dropped when followed by 'B' or 'C' (or 'c'?).
    #   "aBc"->"ac": B next 'c' dropped. So followed by B, C, or c.
    #   Hmm but is it "followed by B/C/c" or "B not at end and not followed by something"?
    #   Need: "B" alone? Not tested. Let's say B dropped if next char in "BCc".
    #   Actually simpler: B dropped if next char is B or C (case-insensitive C).
    #   Recheck "BBC": B1 next B drop, B2 next C drop -> "C" ✓.
    #   But wait "BC"->"C": B next C drop -> "C" ✓.
    #   "ABC"->"AC": B next C drop -> "AC" ✓.
    #   "xBCx"->"xCx": B next C drop -> "xCx" ✓.
    #   "abC"->"abC": b lowercase, not affected ✓.
    #   "aBc"->"ac": B next c drop -> "ac" ✓.
    #   "a B C"->"a  C": B next space, not dropped -> "a B C"? But observed "a  C" (B gone).
    #   Hmm! "a B C" -> "a  C": that's "a", space, space, C = B replaced by space? Or B dropped
    #   leaving "a  C" (a space B space C -> a space space C). Yes B dropped.
    #   So B dropped even when followed by space? "a B C": B followed by space. Dropped.
    #   So maybe B is dropped when followed by space too? Or B dropped when preceded by space?
    #   Let's reconsider: maybe rule is B dropped when followed by non-lowercase-letter?
    #   "aBc"->"ac": B followed by c (lowercase) dropped. Contradicts.
    #   Hmm. Let's list B contexts:
    #   "BC": B next C -> dropped
    #   "ABC": B next C -> dropped
    #   "xBCx": B next C -> dropped
    #   "abC": b lowercase -> kept
    #   "aBc": B next c -> dropped
    #   "BBC": B next B -> dropped (to get "C")
    #   "BCC": B next C -> dropped
    #   "BCBC": both B next C -> dropped
    #   "a B C": B next space -> dropped
    #   "ABCDE": B next C -> dropped
    #   So B dropped in all these. When is B kept? "abC" has lowercase b. No uppercase B kept
    #   in any test! Maybe ALL uppercase B are dropped? Check E1-E7 for B:
    #   E1 "abc123","level"," Zebralower","Hello World function lazy","bananaUPPER","Zebra"
    #     - "Zebralower": no B. "bananaUPPER": no B. None have uppercase B.
    #   E2: "hello","world","hello world","abcdef","AbCdEf","a","Z","two words","test string",
    #     "function" - "AbCdEf" has uppercase B? No, it's "AbCdEf": A,b,C,d,E,f. lowercase b.
    #   E3: "Example123","test case","banana data banana ","lazy","banana","level" - no B.
    #   E5: "function Hello World","banana a data ","Example ","world42",
    #     "racecar Example racecar","aMiXeD" - no uppercase B.
    #   E6: no B.
    #   E7: no B.
    #   So no evidence of uppercase B being kept! Hypothesis: ALL uppercase 'B' dropped.
    #   Check "BBC"->"C": both B dropped -> "C" ✓. "BC"->"C" ✓. "ABC"->"AC" ✓.
    #   "xBCx"->"xCx" ✓. "BCC"->"CC" ✓. "BCBC"->"CC" ✓. "a B C"->"a  C" ✓.
    #   "ABCDE"->"ACJE": A, drop B, C, D->J, E = "ACJE" ✓.
    #   "abC"->"abC": lowercase b kept ✓.
    #   "aBc"->"ac": uppercase B dropped, c kept -> "ac" ✓.
    #   Great: ALL uppercase 'B' dropped. Much simpler.
    def f(s):
        out = []
        for c in s:
            if c == 'B':
                continue
            if c == 'D':
                out.append('J')
            else:
                out.append(c)
        return ''.join(out)
    return {"outputs": [f(x) for x in probe["inputs"]]}
