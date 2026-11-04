def predict(probe):
    # Split on any whitespace, reverse each token's characters, join with single space [E1-E7]
    # Append 'I' as a suffix to the whole result [E1-E7]
    # BUT: 'I' is not always appended — when the result already ends with 'I', no extra 'I'? 
    #   E8: "I"->"I" (not "II"), "hi I"->"ih I" (not "ih II"), "I I"->"I I" (not "I II"),
    #   "II"->"II" (not "III"), "Ihello"->"ollehI" (not "ollehII")
    #   So: append 'I' only if result does not already end with 'I' [E8]
    #   Check: "i"->"iI" (ends 'i', append) ok; "am I"->"ma I" (ends 'I', no append) ok
    #   "hello I world"->"olleh I dlrow" ends 'w', append -> "olleh I dlrowI" ok
    #   "helloi"->"iolleh" ends 'h', append -> "iollehI" ok
    #   "I am"->"I ma" ends 'a', append -> "I maI" ok
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            r = " ".join(w[::-1] for w in words)
            if not r.endswith("I"):
                r += "I"
            out.append(r)
        except Exception:
            out.append("I")
    return {"outputs": out}
