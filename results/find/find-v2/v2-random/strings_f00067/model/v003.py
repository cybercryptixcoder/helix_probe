def predict(probe):
    # Split on whitespace, reverse each word, join with single spaces [E1 abc123->3321cba, E2 test case->tset eesac]
    # Word order preserved; only each word reversed [E1 Hello World function lazy -> olleH dlroW noitcnuf yzal]
    # Leading/multiple spaces collapse to single spaces [E4 "  apple banana function" -> "elppa ananab nnoitcnuf"]
    # If raw input does NOT end with a space, double first char of the reversed last word [E1 level->llevel, E3 world42->224dlrow]
    # If raw input ends with a space, no doubling [E2 "banana data banana " -> "ananab atad ananab", E3 "Example " -> "elpmaxE"]
    # Empty / all-space input -> empty output [?]
    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        words = s.split()
        if not words:
            outputs.append("")
            continue
        rev = [w[::-1] for w in words]
        if not s.endswith(" "):
            rev[-1] = rev[-1][0] + rev[-1]
        outputs.append(" ".join(rev))
    return {"outputs": outputs}
