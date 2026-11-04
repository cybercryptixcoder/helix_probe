def predict(probe):
    # Strip leading/trailing whitespace, then split on whitespace runs and
    # reverse word order if there are multiple words [E1, E2].
    # "one  two" -> "two one" shows multiple spaces collapse [E2].
    # "  padded words  " -> "words padded" shows strip + collapse [E2].
    # Single word unchanged [E1, E2].
    out = []
    for s in probe["inputs"]:
        words = s.split()
        if len(words) > 1:
            out.append(" ".join(words[::-1]))
        else:
            out.append(" ".join(words))
    return {"outputs": out}
