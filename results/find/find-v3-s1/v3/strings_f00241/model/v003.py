def predict(probe):
    # Evidence:
    # E1: "test caseMiXeD" -> "test caseMiXeJ" (final D -> J)
    # E2: "D"->"J", "aD"->"aJ", "ABD"->"AJ" (!!), "12D"->"12J",
    #     "hello d"->"hello d", "hello D"->"hello J", "Dd"->"Jd", "Dx"->"Jx",
    #     "x D"->"x J", "endD"->"endJ"
    # E4: all D->J, multiple D's fine, "Good Day"->"Good Jay"
    # E6: all D->J in mixed contexts, "DeDupED"->"JeJupEJ"
    # E8: "B"->"" (!!), "ABC FPT Z"->"AC FPT Z" (B deleted!)
    #     F,P,T,Z,J,j unchanged; Dj->Jj, jD->jJ
    #
    # Rules:
    # 1. Every 'D' becomes 'J' [E1,E2,E4,E6,E8]
    # 2. Every 'B' is deleted [E8: "B"->"", "ABC FPT Z"->"AC FPT Z"]
    #    Note E2 "ABD"->"AJ": A,B,D -> A,(del),J = "AJ" consistent with B deletion!
    #    (v2 wrongly predicted "ABJ" by only doing D->J.)
    out = []
    for s in probe["inputs"]:
        t = s.replace("D", "J").replace("B", "")
        out.append(t)
    return {"outputs": out}
