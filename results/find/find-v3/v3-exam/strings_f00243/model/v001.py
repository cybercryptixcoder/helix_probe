def predict(probe):
    # Insert 'Z' at a position determined by the input [E1]
    # Observations:
    #  abc123 -> abcZ123 (after 3 chars)
    #  level -> leZvel (after 2)
    #  " Zebralower" -> ZebraZlower (leading space removed, Z after 5)
    #  "Hello World function lazy" -> HelloWorldfZunctionlazy (spaces removed, Z after 11)
    #  bananaUPPER -> bananZaUPPER (after 5)
    #  Zebra -> ZeZbra (after 2)
    # Hypothesis: remove spaces, then insert 'Z' at index len//2 (floor).
    # Check: abc123 len6 ->3 ok; level len5->2 ok; Zebralower len10->5 ok;
    # HelloWorldfunctionlazy len22->11 ok; bananaUPPER len11->5 ok; Zebra len5->2 ok.
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        i = len(t) // 2
        out.append(t[:i] + "Z" + t[i:])
    return {"outputs": out}
