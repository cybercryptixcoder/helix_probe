def predict(probe):
    # Mechanism: shift each char by +4, EXCEPT the first char of the string
    # which gets +2 if it is a letter (a-z or A-Z), else +4.
    # Evidence:
    # - First char letter -> +2: a,b,c,l,H,b,Z? no...
    #   "abc"->"cfg" a+2 [E4]; "level"->"nizip" l+2 [E1]; "Hello"->"Jipps" H+2 [E1]
    #   "bananaUPPER"->"derere..." b+2 [E1]; "nop"->"pst" n+2 [E2]; "zop"->"~st" z+2 [E2]
    #   "NOP"->"PST" N+2 [E2]; "MNO"->"ORS" M+2 [E2]; "AOP"->"CST" A+2 [E2]
    #   "Xbc"->"\\fg" X+2 [E4]; "Abc"->"Cfg" A+2 [E4]; "Ybc"->"]fg" Y+2 [E4]
    #   "Zbc"->"^fg" Z+4 [E4]  <-- Z is the exception among letters!
    #   "Zebra"->"^ifve" Z+4 [E1]; "Zop"->"^st" Z+4 [E2]
    # - First char non-letter -> +4: "0op"->"4st" [E2]; " op"->"$st" [E2]
    #   " Zebralower"->"$^ifve..." space+4 [E1]
    # - All non-first chars -> +4: "abc123"->"cfg567" [E1]; "aXc"->"c\\g" X+4 [E4]
    #   "XYc"->"\\]g" X+4,Y+4 [E4]; "abcX"->"cfg\\" [E4]; "aZcd"->"c^gh" Z+4 [E4]
    #   "world42"->"{svph86" w+4 [E5]; "aMiXeD"->"cQm\\iH" M+4,i+4,X+4,e+4,D+4 [E5]
    # - Z is the only letter that gets +4 as first char (both cases? only Z tested).
    #   Hypothesis: first char gets +2 iff it is a letter other than 'Z'.
    #   (Lowercase z gets +2 per E2 "zop"->"~st"; only uppercase Z is +4.)
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'z') or ('A' <= c <= 'Y')):
                sh = 2
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
