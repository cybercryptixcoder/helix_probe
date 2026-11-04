def predict(probe):
    # Evidence:
    # E1: "test caseMiXeD" -> "test caseMiXeJ" (final D -> J)
    # E2: "D"->"J", "aD"->"aJ", "ABD"->"AJ", "12D"->"12J",
    #     "hello d"->"hello d" (lowercase d unchanged),
    #     "hello D"->"hello J", "Dd"->"Jd", "Dx"->"Jx",
    #     "x D"->"x J", "endD"->"endJ"
    # Rule: every 'D' anywhere in the string becomes 'J'; 'd' unaffected.
    # (E1's "data a Python " has no D; "Mississippi Hello World data" has no D.)
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J"))
    return {"outputs": out}
