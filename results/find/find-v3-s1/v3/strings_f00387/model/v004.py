def predict(probe):
    # First char uppercased, rest lowercased [E1,E2,E3]
    # Leading whitespace: no capitalization [E2,E4]
    # Lowercase 'm' is deleted when it is the FIRST letter of a word [E4,E5,E6]
    #   "quote me"->"quote e", "matter"->"atter", "am matter"->"A atter"
    #   "banana man"->"Banana an", "item"->"Ite", "camera"->"Caera"
    #   "summer"->"Suer": 'm' at index 2, not word start... wait
    # Re-examine E6: amber->Aber (m at idx1 deleted), emerald->Eerald (idx1),
    #   imagine->Iagine (idx1), omit->Oit (idx1), umbrella->Ubrella (idx1),
    #   camera->Caera (m at idx2 deleted), summer->Suer (m at idx2 deleted),
    #   item->Ite (m at idx3 deleted), am matter->A atter (both m's deleted)
    # So 'm' is deleted EVERYWHERE it appears as lowercase! [E6]
    #   Check E5: "Mississippi"->"Mississippi" capital M kept (not lowercase).
    #   E1: "test caseMiXeD"->"Test casemixed": after lowercasing, "casemixed"
    #     has 'm' at idx4 -> should be deleted -> "caseixed"? But E1 shows "casemixed"!
    #   Hmm. Let me check E1 output again: "Test casemixed" - m kept there.
    #   Contradiction. Difference: in E1 the m came from uppercase 'M' originally.
    #   So: delete 'm' only if it was lowercase in the ORIGINAL input? 
    #   "Example"->"Exaple": original 'm' lowercase -> deleted. Good.
    #   "caseMiXeD": original 'M' uppercase -> kept. Good.
    #   "Mississippi": original 'M' uppercase -> kept. Good.
    #   E6 all lowercase m -> all deleted. Good.
    #   "am matter": both lowercase m -> both deleted -> "A atter". Good.
    # Rule: lowercase 'm' in original input is deleted; uppercase 'M' kept.
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        first = s[0]
        if first.isspace():
            t = first + s[1:].lower()
        else:
            t = first.upper() + s[1:].lower()
        res = []
        for i, ch in enumerate(t):
            if ch == 'm' and s[i] == 'm':
                continue
            res.append(ch)
        out.append(''.join(res))
    return {"outputs": out}
