def predict(probe):
    # lowercase p -> k [E1-E14]
    # if a lowercase p is followed by uppercase L, drop that L [E10,E12,E14]
    #   pL->k, PpL->Pk, apL->ak, pLL->k (only first L dropped, second L... wait pLL->k means both dropped)
    #   Actually pLL->k: p->k, then L dropped, then next L also dropped? "pLL" -> "k". 
    #   Hmm, "pLL" observed "k". So both L's gone. But "pLp"->"kk": p->k, L dropped, p->k.
    #   So after p, ALL consecutive uppercase L's are dropped? pLL->k yes.
    #   But wait, is it "drop L's following p" or "drop L's following k that came from p"?
    #   Let's just: when see lowercase p, emit k, then skip all following uppercase L's.
    def f(s):
        out = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == 'p':
                out.append('k')
                i += 1
                while i < len(s) and s[i] == 'L':
                    i += 1
            else:
                out.append(c)
                i += 1
        return ''.join(out)
    return {"outputs": [f(s) for s in probe["inputs"]]}
