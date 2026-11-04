def predict(probe):
    # Strip ALL leading spaces [E4: "  Hello"->"ello", "   Hello"->"ello", "  lead"->"lead", "  two spaces"->"two spaces"]
    # Then strip ALL leading H's [E4: "HHHello"->"ello", "HH"->"", "HHH"->"", "H Hello"->" ello"]
    # Then strip ALL trailing spaces [E4: "banana  "->"banana", " Hello "->"ello"]
    # Order matters: spaces first, then H's, then trailing spaces [E4: " H"->"" (space then H)]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip(" ")
        s = s.lstrip("H")
        s = s.rstrip(" ")
        out.append(s)
    return {"outputs": out}
