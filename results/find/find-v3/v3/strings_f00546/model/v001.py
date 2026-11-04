def predict(probe):
    # Prefix "lmKA" is prepended to every output [E1]
    # Everything after the prefix is the input reversed [E1]
    out = []
    for s in probe.get("inputs", []):
        out.append("lmKA" + s[::-1])
    return {"outputs": out}
