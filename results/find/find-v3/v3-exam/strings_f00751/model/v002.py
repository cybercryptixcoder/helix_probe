def predict(probe):
    # Strip leading AND trailing whitespace first [E1, E2: "  abc  "->"aibc", "xy  "->"xyi", "ab "->"aib"]
    # Then insert "i" at index floor(len(stripped)/2) [E1, E2]
    #   "  abc  "->"abc", mid=1 -> "aibc" [E2]
    #   "xy  "->"xy", mid=1 -> "xyi" [E2]
    #   "  hello"->"hello", mid=2 -> "heillo"? observed "hiello" -> mid=1
    #   "a b "->"a b", mid=1 -> "a ib" [E2]
    #   "  "->"", mid=0 -> "i" [E2]
    #   "ab "->"ab", mid=1 -> "aib" [E2]
    # "hello" (len 5): observed "hiello" -> insert at index 1, not 2.
    # "level" (len 5): "leivel" -> index 2. "Zebra" (len 5): "Zeibra" -> index 2.
    # "abc123" (len 6): "abci123" -> index 3. "bananaUPPER" (len 11): "bananiaUPPER" -> index 6.
    # "Hello World function lazy" (len 25): "Hello World ifunction lazy" -> index 12.
    # So mid = len//2 generally, but "hello" gave index 1. Hmm.
    # Wait: "  hello" stripped = "hello" len 5, mid=2 -> "heillo", but observed "hiello".
    # Unless insertion index is computed on the ORIGINAL string then applied to stripped?
    # "  hello" len 7, mid=3. Stripped "hello", insert at min(3, len)=3 -> "helilo". No.
    # Maybe index = (len(stripped)-1)//2? "hello"->2, no.
    # Recheck: "hiello" = "h"+"i"+"ello", index 1. "leivel" index 2. Both len 5.
    # Difference: "  hello" had leading spaces. Perhaps index computed on original: len 7 //2 =3? no.
    # Perhaps leading whitespace count subtracted differently: original mid=3, minus leading spaces 2 =1. Yes!
    # "  abc  " len 7 mid=3, leading 2 -> 1 -> "aibc" ✓
    # "xy  " len 4 mid=2, leading 0 -> 2 -> "xyi" ✓
    # "a b " len 4 mid=2, leading 0 -> 2 -> "a ib"? "a b" insert at 2 = "a ib" ✓
    # "ab " len 3 mid=1 -> "aib" ✓
    # "  " len 2 mid=1, leading 2 -> -1? clamp 0 -> "i" ✓
    # " Zebralower" len 12 mid=6, leading 1 -> 5 -> "Zebri"+"alower"? observed "Zebrialower" = index 5 ✓
    # "Hello World function lazy" len 25 mid=12, leading 0 -> 12 ✓
    # So: mid = len(original)//2 - leading_whitespace_count, clamped to [0, len(stripped)]
    outputs = []
    for s in probe["inputs"]:
        lead = len(s) - len(s.lstrip())
        t = s.strip()
        mid = len(s) // 2 - lead
        mid = max(0, min(mid, len(t)))
        outputs.append(t[:mid] + "i" + t[mid:])
    return {"outputs": outputs}
