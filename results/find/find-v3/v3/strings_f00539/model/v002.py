def predict(probe):
    # Dedup: keep first occurrence of each character (case-sensitive) [E1]
    # Then append "h" only if "h" not already present in the deduped string [E2]
    # Evidence: "h"->"h", "hh"->"h", "hi"->"hi", "ih"->"ih", "help"->"help",
    #           "hhelp"->"help", "ah"->"ah", "ha"->"ha", "Hello"->"Heloh", "a h"->"a h"
    # So the rule is: dedup, then add "h" if absent.
    out = []
    for s in probe["inputs"]:
        d = "".join(dict.fromkeys(s))
        if "h" not in d:
            d += "h"
        out.append(d)
    return {"outputs": out}
