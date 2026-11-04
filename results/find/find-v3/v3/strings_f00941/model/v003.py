def predict(probe):
    # f(x) = x.strip() + "ny" [E1, E2, E3, E4]
    #   - leading/trailing whitespace removed before appending "ny" [E4: " leading"->"leadingny", "  a"->"any"]
    #   - internal whitespace (spaces, tabs, newlines) preserved verbatim [E4: "a  b"->"a  bny", "a\tb"->"a\tbny"]
    #   - trailing spaces preserved when followed by non-space? No: "trailing "->"trailing ny" keeps one trailing space
    #     Actually strip() removes trailing space: "trailing " -> "trailing" + "ny" = "trailingny"? But observed "trailing ny".
    #     So only LEADING whitespace is stripped; trailing whitespace is kept [E4: "trailing "->"trailing ny", "a  "->"a  ny"]
    #   - whitespace-only -> "ny" [E2, E4: "   "->"ny"]
    #   - case, digits, symbols untouched [E1, E2]
    out = []
    for x in probe["inputs"]:
        if x.strip() == "":
            out.append("ny")
        else:
            out.append(x.lstrip() + "ny")
    return {"outputs": out}
