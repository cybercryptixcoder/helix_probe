def predict(probe):
    # Observations from E1:
    #   "abc123" -> "321Wcba"        : reverse, but 'W' inserted in middle
    #   "level"  -> "leWvel"         : reverse -> "level", 'W' inserted in middle
    #   " Zebralower" -> "rewolWarbeZ " : reverse -> "rewolWarbeZ ", 'W' inserted in middle
    #   "Hello World function lazy" -> "yzal noitcnuWf dlroW olleH"
    #        reverse -> "yzal noitcnuf dlroW olleH", 'W' inserted in middle
    #   "bananaUPPER" -> "REPPUWananab" : reverse -> "REPPUananab", 'W' inserted in middle
    #   "Zebra" -> "arWbeZ"          : reverse -> "arbeZ", 'W' inserted in middle
    # Rule: reverse the string, then insert 'W' at the middle index.
    # Middle index = len(s)//2 (insert before that position).
    # Check: "abc123" len 6 -> reverse "321cba", insert at 3 -> "321Wcba" ✓
    #        "level" len 5 -> reverse "level", insert at 2 -> "leWvel" ✓
    #        " Zebralower" len 11 -> reverse "rewolWarbeZ "? reverse is "rewolWarbeZ ",
    #            insert at 5 -> "rewolWarbeZ " -> "rewol"+"W"+"arbeZ " = "rewolWarbeZ " ✓
    #        "bananaUPPER" len 11 -> reverse "REPPUananab", insert at 5 -> "REPPU"+"W"+"ananab" ✓
    #        "Zebra" len 5 -> reverse "arbeZ", insert at 2 -> "arWbeZ" ✓
    #        "Hello World function lazy" len 26 -> reverse "yzal noitcnuf dlroW olleH",
    #            insert at 13 -> "yzal noitcnu"+"W"+"f dlroW olleH" = "yzal noitcnuWf dlroW olleH" ✓
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        m = len(r) // 2
        out.append(r[:m] + "W" + r[m:])
    return {"outputs": out}
