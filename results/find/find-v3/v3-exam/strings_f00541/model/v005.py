def predict(probe):
    # Strip ALL leading spaces [E4: "  Hello"->"ello", "   Hello"->"ello", "  lead"->"lead"]
    # Strip ALL leading H's [E4: "HHHello"->"ello", "HH"->"", "HHH"->"", "H Hello"->" ello"]
    # Strip ALL trailing spaces [E4: "banana  "->"banana"]
    # Order: spaces, then H's, then trailing spaces [E4: " H"->""]
    # H-strip applies anywhere in string, not just at start [E5: "function Hello World"->"function ello World"]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip(" ")
        s = s.lstrip("H")
        s = s.replace("H", "")  # ? H removed everywhere, not just leading
        s = s.rstrip(" ")
        out.append(s)
    return {"outputs": out}
