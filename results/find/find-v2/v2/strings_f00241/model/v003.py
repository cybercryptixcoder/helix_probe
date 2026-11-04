def predict(probe):
    # Identity on ordinary strings [E1, E2, E3]
    # Exception: a capital "D" becomes "J" [E4 "Dog"->"Jog", E5 "aMiXeD"->"aMiXeJ"]
    # So the rule is: every 'D' character is replaced by 'J'. [E4, E5]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J"))
    return {"outputs": out}
