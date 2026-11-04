def predict(probe):
    # Rule: remove all spaces, then capitalize the first letter of the result [E1]
    #   "apple" -> "Apple"
    #   "test case " -> "Testcase"
    #   "test caseMiXeD" -> "Testcasemixed"
    #   "data a Python " -> "Dataapython"
    #   "test case Zebra" -> "Testcasezebra"
    #   "Mississippi Hello World data" -> "Mississippihelloworlddata"
    # Note: only the first character is uppercased; the rest is lowercased.
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        if t:
            t = t[0].upper() + t[1:].lower()
        out.append(t)
    return {"outputs": out}
