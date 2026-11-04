def predict(probe):
    # Identity on ordinary strings [E1, E2, E3, E7]
    # Capital 'D' -> 'J' [E4, E5, E6]
    # Capital 'B' -> '' (deleted) [E8: "Bat"->"at", "Banana"->"anana"]
    # Other capitals unchanged [E8: Cat, Rat, Hat, Mat, Goat, Lamp, Apple, Cherry]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J").replace("B", ""))
    return {"outputs": out}
