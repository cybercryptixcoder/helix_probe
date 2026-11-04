def predict(probe):
    # Strip all leading whitespace (spaces, tabs, newlines) [E4, E6]
    # Append "ny" to the stripped input [E1, E2, E3, E5]
    # Trailing whitespace preserved verbatim [E4, E6]
    # Internal whitespace preserved verbatim [E4, E6]
    # All-whitespace input yields just "ny" [E2, E4, E6]
    out = []
    for x in probe["inputs"]:
        out.append(x.lstrip() + "ny")
    return {"outputs": out}
