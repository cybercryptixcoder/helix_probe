def predict(probe):
    # Reverse the string, then swap case of each character [E1]
    # "abc123" -> "321cba" (reverse only, digits unchanged)
    # "level" -> "Level" (reverse is same, then case swap: l->L)
    # " Zebralower" -> "Rewolarbez " (reverse, then case swap)
    # "Hello World function lazy" -> "Yzal noitcnuf dlrow olleh" (reverse, case swap)
    # "bananaUPPER" -> "Reppuananab" (reverse, case swap)
    # "Zebra" -> "Arbez" (reverse, case swap)
    out = []
    for s in probe.get("inputs", []):
        try:
            r = s[::-1]
            r = r.swapcase()
            out.append(r)
        except Exception:
            out.append("")
    return {"outputs": out}
