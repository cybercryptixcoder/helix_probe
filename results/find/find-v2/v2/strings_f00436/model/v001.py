def predict(probe):
    # Reverse the string, then insert "I" in the middle [E1]
    #   "abc123" -> "321cba" -> "321Icba"  (len 6, insert at index 3)
    #   "level"  -> "level"  -> "levIel"   (len 5, insert at index 3)
    #   " Zebralower" -> "rewolarbeZ" -> "rewolaIrbeZ" (len 11, insert at index 6)
    #   "Hello World function lazy" -> "yzal noitcnuf dlroW olleH" -> "...functionI lazy"
    #   "bananaUPPER" -> "REPPUananab" -> "REPPUaInanab" (len 11, insert at index 6)
    #   "Zebra" -> "arbeZ" -> "arbIeZ" (len 5, insert at index 3)
    # Insert position = ceil(len/2) for odd, len/2 for even? 
    #   len 6 -> 3, len 5 -> 3, len 11 -> 6, len 5 -> 3
    #   So position = (len+1)//2 for odd gives 3, even 6//2=3. Both = (len+1)//2.
    out = []
    for s in probe.get("inputs", []):
        try:
            r = s[::-1]
            pos = (len(r) + 1) // 2
            out.append(r[:pos] + "I" + r[pos:])
        except Exception:
            out.append("")
    return {"outputs": out}
