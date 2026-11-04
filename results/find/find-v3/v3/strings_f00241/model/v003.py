def predict(probe):
    # Identity on ordinary strings [E1, E2, E3, E4]
    # Every 'D' (uppercase only) becomes 'J', anywhere in the string [E6]
    #   E6: "D"->"J", "DD"->"JJ", "Dabc"->"Jabc", "aDc"->"aJc", "D D"->"J J", "DdD"->"JdJ"
    #   lowercase 'd' unchanged [E6: "d"->"d"]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J"))
    return {"outputs": out}
