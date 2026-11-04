def predict(probe):
    # Rule: delete every uppercase 'L' [E1-E14]
    # Rule: lowercase 'p' -> 'k' [E15, E16]
    #   Evidence E16: apostrophe->akostrokhe, apostrophes->akostrokhes,
    #     apple->akkle, apricot->akricot, paper->kaker, pepper->kekker,
    #     happy->hakky, open->oken, spoon->skoon, help->helk.
    #   Every lowercase 'p' becomes 'k', regardless of preceding letter
    #   (spoon: s-p -> k; help: l-p -> k; pepper: both p's -> k).
    #   Earlier "p kept" cases (LAMP, SPOON, PEACE, HELP) were uppercase P.
    #   So: lowercase p -> k unconditionally; uppercase P unchanged.
    #   Order: does L-deletion happen before or after p->k? Doesn't matter
    #   since they touch different characters.
    out = []
    for x in probe["inputs"]:
        s = x.replace("L", "")
        s = s.replace("p", "k")
        out.append(s)
    return {"outputs": out}
