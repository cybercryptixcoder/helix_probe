
def f(x):
    parts = x.split(" ")
    parts = [p[::-1] for p in parts]
    parts[-1] = "lmKA" + parts[-1]
    return " ".join(w for w in " ".join(parts).split(" ") if w != "") if False else " ".join(parts).replace("  "," ")
