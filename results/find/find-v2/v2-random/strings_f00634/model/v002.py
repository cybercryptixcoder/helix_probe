def predict(probe):
    # Rule: capitalize() the whole string first (first char upper, rest lower),
    # then remove ALL whitespace characters (spaces, tabs, etc.).
    # Evidence:
    #  "abc123" -> "Abc123" [E1]
    #  "level" -> "Level" [E1]
    #  " Zebralower" -> "zebralower" (capitalize keeps leading space, then removed) [E1]
    #  "Hello World function lazy" -> "Helloworldfunctionlazy" [E1]
    #  "bananaUPPER" -> "Bananaupper" [E1]
    #  "worldtab\tsep" -> "Worldtabsep" (tab also removed) [E9]
    #  "  the quick brown fox" -> "thequickbrownfox" [E8]
    #  "  aMiXeD" -> "amixed" [E7]
    #  "  xyz " -> "xyz" [E8]
    #  "world  " -> "World" [E5,E6]
    #  "test case a  " -> "Testcasea" [E9]
    import re
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(re.sub(r"\s+", "", s.capitalize()))
        except Exception:
            out.append("")
    return {"outputs": out}
