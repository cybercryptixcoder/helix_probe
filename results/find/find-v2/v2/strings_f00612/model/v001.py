def predict(probe):
    # Rule: for each input string s:
    #   1. Shift every character up by 1 in ASCII (Caesar +1) [E1]
    #   2. Insert 'Y' at index len(s)//2 [E1]
    # Evidence: abc123->bcdY234, level->mfYwfm, Zebra->[fYcsb,
    #   " Zebralower"->"![fcsYbmpxfs", "Hello World function lazy"->"Ifmmp!Xpsme!Ygvodujpo!mb{z",
    #   bananaUPPER->cboboYbVQQFS [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            shifted = "".join(chr(ord(c) + 1) for c in s)
            i = len(s) // 2
            out.append(shifted[:i] + "Y" + shifted[i:])
        except Exception:
            out.append("")
    return {"outputs": out}
