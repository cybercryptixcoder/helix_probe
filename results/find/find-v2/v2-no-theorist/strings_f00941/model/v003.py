def predict(probe):
    # Appends "ny" to every input [E1, E2, E3]
    # Leading spaces are stripped from the input before appending "ny" [E4: " lead"->"leadny", " x "->"x ny"]
    # Trailing spaces are preserved [E4: "trail "->"trail ny", "end "->"end ny"]
    # Internal whitespace preserved verbatim [E4: "two  spaces"->"two  spacesny", "a  b  c"->"a  b  cny"]
    # All-space input yields just "ny" [E2: "  "->"ny", E4: "   "->"ny"]
    # Other whitespace (tab, newline) preserved verbatim [E4: "tab\there"->"tab\thereny", "new\nline"->"new\nlineny"]
    out = []
    for x in probe["inputs"]:
        s = x.lstrip(" ")
        out.append(s + "ny")
    return {"outputs": out}
