def predict(probe):
    # Insert 'f' at index len//2, then append the original last char [E1, E2]
    # For empty string: insert 'f' at 0, then append last char -> but no last char;
    #   observed "ff" [E2], so append 'f' when empty.
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("ff")
            continue
        m = len(s) // 2
        out.append(s[:m] + "f" + s[m:] + s[-1])
    return {"outputs": out}
