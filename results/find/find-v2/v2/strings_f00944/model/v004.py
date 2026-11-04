def predict(probe):
    # Uppercase R is deleted everywhere [E6: "R"->"", "ER"->"F", "ZebraR"->"Zebrb", "HERO"->"HEP"]
    # Lowercase r is kept [E6: "Er"->"Es", "er"->"es", "Error"->"Erros"]
    # After R-removal, the LAST character is shifted up by 1 if it's a letter [E1-E5]
    #   a->b, z->a, A->B, Z->A (wraparound) [E2: "z"->"a", "Z"->"A"; E4: "xyz"->"xya", "XYZ"->"XYA"]
    # Non-letters (digits, spaces, symbols) at the end are left unchanged [E2, E4, E5]
    # Empty result stays empty [E6: "R"->""]
    out = []
    for s in probe.get("inputs", []):
        t = s.replace("R", "")
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                nc = 'a' if c == 'z' else chr(ord(c) + 1)
                t = t[:-1] + nc
            elif 'A' <= c <= 'Z':
                nc = 'A' if c == 'Z' else chr(ord(c) + 1)
                t = t[:-1] + nc
        out.append(t)
    return {"outputs": out}
