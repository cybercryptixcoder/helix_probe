def predict(probe):
    # Mechanism: shift each char by +4, EXCEPT the first char of the string
    # which gets +2 if it is a letter other than 'z' or 'Z', else +4.
    # Evidence:
    # - First char letter (not z/Z) -> +2: "abc"->"cfg" a+2 [E4]; "level"->"nizip" l+2 [E1]
    #   "Hello"->"Jipps" H+2 [E1]; "nop"->"pst" n+2 [E2]; "NOP"->"PST" [E2]
    #   "mno"->"ors" [E2]; "MNO"->"ORS" [E2]; "aop"->"cst" [E2]; "AOP"->"CST" [E2]
    #   "Xbc"->"\\fg" X+2 [E4]; "Abc"->"Cfg" [E4]; "Ybc"->"]fg" [E4]
    #   "yop"->"}st" [E6]; "Yop"->"]st" [E6]; "xop"->"|st" [E6]; "Xop"->"\\st" [E6]
    #   "wop"->"{st" [E6]; "Wop"->"[st" [E6]
    # - First char z or Z -> +4: "zebra"->"~ifve" z+4 [E6]; "zop"->"~st" [E2,E6]
    #   "Zebra"->"^ifve" [E1,E6]; "Zop"->"^st" [E2,E6]; "Zbc"->"^fg" [E4]
    # - First char non-letter -> +4: "0op"->"4st" [E2]; " op"->"$st" [E2]
    # - All non-first chars -> +4: "abc123"->"cfg567" [E1]; "aXc"->"c\\g" [E4]
    #   "aZcd"->"c^gh" Z+4 [E4]; "aMiXeD"->"cQm\\iH" [E5]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'z') or ('A' <= c <= 'Z')) and c not in 'zZ':
                sh = 2
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
