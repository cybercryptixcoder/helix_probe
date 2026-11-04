import math

def predict(probe):
    out = []
    for s in probe.get("inputs", []):
        if len(s) == 0:
            out.append("ERROR: IndexError")
        else:
            pos = (len(s) + 1) // 2  # ceil(len/2)
            out.append(s[:pos] + "5" + s[pos:] + s[-1])
    return {"outputs": out}
