def predict(probe):
    # f(x) = x + 1 for x >= 0, and x - 1 for x < 0 [E1]
    # Check: x=-128→-129, x=-1→-2, x=0→-1, x=1→2, x=128→129 [E1]
    # So f(x) = x + sign(x) with sign(0) treated as -1 (i.e., x<0 → x-1, x>=0 → x+1)
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(x - 1)
        else:
            out.append(x + 1)
    return {"y": out}
