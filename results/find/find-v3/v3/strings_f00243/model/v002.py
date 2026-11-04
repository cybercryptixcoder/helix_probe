def predict(probe):
    # Remove ALL whitespace characters (spaces, tabs, newlines, carriage returns, etc.) [E8]
    # Then insert 'Z' at index len//2 of the whitespace-free string [E1-E7]
    # E8: "a\tb"->"aZb", "a\nb"->"aZb", "a\tb\tc"->"aZbc", "\t"->"Z", "\n\n"->"Z",
    #     "a b\tc"->"aZbc", "  \t  "->"Z", "ab\tcd"->"abZcd", "a\r\nb"->"aZb", "x y\tz"->"xZyz"
    # All whitespace removed, not just spaces.
    out = []
    for x in probe["inputs"]:
        t = "".join(ch for ch in x if not ch.isspace())
        m = len(t) // 2
        out.append(t[:m] + "Z" + t[m:])
    return {"outputs": out}
