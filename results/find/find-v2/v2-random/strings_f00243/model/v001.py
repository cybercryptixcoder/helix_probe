def predict(probe):
    # Observations from E1:
    # - "abc123" -> "abcZ123": 'Z' inserted before first digit
    # - "level" -> "leZvel": 'Z' inserted at middle (len 5 -> pos 2)
    # - " Zebralower" -> "ZebraZlower": space removed, 'Z' inserted at middle of remaining
    # - "Hello World function lazy" -> "HelloWorldfZunctionlazy": spaces removed, 'Z' inserted at middle
    # - "bananaUPPER" -> "bananZaUPPER": 'Z' inserted at middle (len 11 -> pos 5)
    # - "Zebra" -> "ZeZbra": 'Z' inserted at middle (len 5 -> pos 2)
    # Rules:
    # 1. Remove all spaces [E1]
    # 2. Insert 'Z' at the middle index (len//2) of the space-stripped string [E1]
    #    - "abc123" len 6 -> pos 3 -> "abcZ123" ✓
    #    - "level" len 5 -> pos 2 -> "leZvel" ✓
    #    - "Zebralower" len 10 -> pos 5 -> "ZebraZlower" ✓
    #    - "HelloWorldfunctionlazy" len 23 -> pos 11 -> "HelloWorldfZunctionlazy" ✓
    #    - "bananaUPPER" len 11 -> pos 5 -> "bananZaUPPER" ✓
    #    - "Zebra" len 5 -> pos 2 -> "ZeZbra" ✓
    out = []
    for s in probe.get("inputs", []):
        t = s.replace(" ", "")
        m = len(t) // 2
        out.append(t[:m] + "Z" + t[m:])
    return {"outputs": out}
