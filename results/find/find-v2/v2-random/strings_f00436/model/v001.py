def predict(probe):
    # Reverse the string, then insert 'I' before the last character [E1]
    # Evidence: "abc123" -> "321Icba" (reverse "321cba", insert I before 'a')
    #           "level" -> "levIel" (reverse "level", insert I before 'l')
    #           " Zebralower" -> "rewolaIrbeZ" (reverse, insert I before 'Z')
    #           "Hello World function lazy" -> "olleH dlroW noitcnufI yzal"
    #           "bananaUPPER" -> "REPPUaInanab"
    #           "Zebra" -> "arbIeZ"
    # Rule: reverse the string; then insert 'I' immediately before the final character.
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        if len(r) >= 1:
            r = r[:-1] + "I" + r[-1:]
        out.append(r)
    return {"outputs": out}
