def predict(probe):
    # Rule: output is the input string reversed [E1, E2, E5-E9]
    # Rule: whitespace (spaces AND tabs) is removed from the output [E2, E9]
    #   E9: "worldtab\tsep" -> "pesbatdlrow" (tab removed, not kept)
    #   E2: "test case" -> "esactset" (space removed)
    #   Order: strip whitespace first, then reverse (equivalent for these cases).
    import re
    return {"outputs": [re.sub(r"\s", "", s)[::-1] for s in probe["inputs"]]}
