def predict(probe):
    # Insert "10" at len//2 of the ORIGINAL string [E1-E11]
    # Then apply str.capitalize() (first char titlecase, rest lowercased) [E9,E11]
    #   E11: "İx"->"İ10x" (İ not lowercased before insert; capitalize keeps İ)
    #   E11: "ẞa"->"ẞ10a" (ẞ not lowercased before insert)
    #   E11: "ßa"->"Ss10a" (capitalize: ß->Ss)
    #   E9: "İİ"->"İ10i̇" (first İ kept, second lowercased by capitalize)
    #   E9: "ẞ"->"10ß" (insert at 0, capitalize lowercases ẞ->ß in tail)
    def transform(s):
        p = len(s) // 2
        return (s[:p] + '10' + s[p:]).capitalize()
    return {"outputs": [transform(x) for x in probe["inputs"]]}
