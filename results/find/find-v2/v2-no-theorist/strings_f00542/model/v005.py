def predict(probe):
    # Split on whitespace into tokens [E4,E17]
    # Output = reverse(first token) + " " + reverse(concat of remaining tokens) [E16,E18,E20]
    # Single token -> just reverse it [E9,E13,E17]
    # Empty/whitespace-only -> "" [E4]
    out = []
    for s in probe.get("inputs", []):
        try:
            w = s.split()
            if not w:
                out.append("")
            elif len(w) == 1:
                out.append(w[0][::-1])
            else:
                out.append(w[0][::-1] + " " + "".join(w[1:])[::-1])
        except Exception:
            out.append("")
    return {"outputs": out}
