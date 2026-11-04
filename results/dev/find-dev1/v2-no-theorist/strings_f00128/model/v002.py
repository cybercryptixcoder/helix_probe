def predict(probe):
    # Rule: lowercase whole string, insert "10" at len//2, then capitalize first char [E1,E2,E3]
    # E3 "\u0130a" -> "\u013010a": Python's str.lower() maps İ to "i\u0307" (2 chars),
    #   but observed output keeps İ as single char. So lowercase must NOT expand İ.
    #   Use casefold? No. Use a per-char lower that keeps İ as İ? Observed "\u013010a":
    #   position len//2 = 1, so insert after first char: "\u0130"+"10"+"a". So İ unchanged.
    #   => lowercase only ASCII letters (and other chars that don't expand).
    # E3 "ßa" -> "Ss10a": ß.lower()="ß", but capitalize() of "ß10a" gives "Ss10a" in Python
    #   (capitalize uppercases first char: ß->Ss). So keep ß, let capitalize handle it.
    # E3 "ÀÉÎÕÜ" -> "Àé10îõü": lowercased rest, first char À kept uppercase by capitalize.
    # So: lowercase via str.lower() but İ must stay single char. Python lower of İ = "i\u0307".
    # Fix: replace İ with itself before/after lowering.
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s2 = s.lower()
            # undo İ expansion: "i\u0307" -> "İ"? but we want İ preserved as-is
            s2 = s2.replace("i\u0307", "\u0130")
            pos = len(s) // 2
            s3 = s2[:pos] + "10" + s2[pos:]
            outputs.append(s3.capitalize())
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
